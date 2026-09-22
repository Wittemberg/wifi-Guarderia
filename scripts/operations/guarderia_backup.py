#!/usr/bin/env python3
"""Backup privado do NOC. Executar como root; nunca publicar arquivos gerados."""
import argparse, base64, datetime as dt, fcntl, hashlib, json, os, secrets
import shutil, signal, sqlite3, subprocess, sys, tarfile, tempfile, time
from pathlib import Path

ROOT = Path('/root/guarderia-backups')
KEY = ROOT / 'recovery.key'
APPS = {'monitor_grafana': '/var/lib/grafana', 'monitor_prometheus': '/prometheus',
        'uptimekuma_uptimekuma': '/app/data', 'portainer_portainer': '/data',
        'traefik_traefik': '/etc/traefik/letsencrypt'}
PG = ['postgres_postgres', 'zabbix_zabbix-db']
os.umask(0o077)


def run(*args, output=None, timeout=300, data=None):
    result = subprocess.run(args, input=data, stdout=subprocess.PIPE if output is None else output,
                            stderr=subprocess.PIPE, timeout=timeout)
    if result.returncode:
        # Keep diagnostic output private; it may contain database identifiers.
        (ROOT / 'last-command-error-private.txt').write_bytes(result.stderr)
        raise RuntimeError(f'{args[0]} failed with code {result.returncode}')
    return result.stdout.decode().strip() if output is None else None


def js(*args): return json.loads(run(*args))
def write(path, obj):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2)); os.replace(tmp, path)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


def current(name):
    ids = run('docker', 'ps', '-q', '--filter', 'label=com.docker.swarm.service.name=' + name).split()
    if len(ids) != 1: raise RuntimeError(name + ': expected one active container')
    return js('docker', 'inspect', ids[0])[0]


def gpg(*args, output=None):
    return run('gpg', '--homedir', str(ROOT / 'gnupg'), '--batch', '--yes', '--pinentry-mode',
               'loopback', '--passphrase-file', str(KEY), *args, output=output, timeout=1800)


def verify(archive, destination=None):
    """Authenticate encrypted payload, then verify every archived file against its manifest."""
    with tempfile.TemporaryDirectory(prefix='.verify-', dir=ROOT) as td:
        clear = Path(td) / 'payload.tar.gz'
        with clear.open('wb') as out: gpg('--decrypt', str(archive), output=out)
        with tarfile.open(clear, 'r:gz') as tar:
            manifest = json.load(tar.extractfile('manifest.json'))
            members = tar.getmembers()
            expected = {x['path']: x for x in manifest}
            if len(expected) != len(manifest): raise RuntimeError('Duplicate manifest entry')
            seen = set()
            for member in members:
                if member.name in seen or not member.isfile(): raise RuntimeError('Invalid archive member')
                seen.add(member.name)
                if member.name == 'manifest.json': continue
                if member.name not in expected: raise RuntimeError('Unexpected archive member')
                h = hashlib.sha256()
                with tar.extractfile(member) as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''): h.update(chunk)
                item = expected[member.name]
                if h.hexdigest() != item['sha256'] or member.size != item['bytes']:
                    raise RuntimeError('Backup checksum mismatch')
            if seen != set(expected) | {'manifest.json'}: raise RuntimeError('Incomplete archive')
            if destination: tar.extractall(destination, filter='data')
        return len(manifest)


def retention():
    valid = []
    for p in (ROOT / 'archives').glob('backup-*.gpg'):
        receipt = p.with_suffix('.json')
        if receipt.exists():
            info = json.loads(receipt.read_text())
            if info.get('verified'): valid.append((dt.datetime.fromisoformat(info['timestamp']), p))
    keep = set()
    for key, count in [(lambda d: d.date(), 7), (lambda d: d.isocalendar()[:2], 4),
                       (lambda d: (d.year, d.month), 3)]:
        buckets = set()
        for stamp, path in sorted(valid, reverse=True):
            bucket = key(stamp)
            if bucket not in buckets and len(buckets) < count:
                keep.add(path); buckets.add(bucket)
    for _, path in valid:
        if path not in keep:
            path.unlink(); path.with_suffix('.json').unlink()


def backup():
    started = time.monotonic(); stamp = dt.datetime.now(dt.timezone.utc)
    if shutil.disk_usage(ROOT).free < 2 * 1024**3: raise RuntimeError('Less than 2 GiB free')
    stage = Path(tempfile.mkdtemp(prefix='.incomplete-', dir=ROOT))
    inventory = {name: current(name) for name in [*APPS, *PG]}
    write(stage / 'containers-private.json', inventory)
    write(stage / 'services-private.json', js('docker', 'service', 'inspect',
                                             *run('docker', 'service', 'ls', '-q').split()))
    pauses = {}
    for name, target in APPS.items():
        c = inventory[name]
        source = next(m['Source'] for m in c['Mounts'] if m['Destination'] == target)
        began = time.monotonic()
        run('docker', 'pause', c['Id'])
        try:
            run('tar', '--numeric-owner', '-cpf', str(stage / (name + '.tar')),
                '-C', source, '.', timeout=45)
        finally: run('docker', 'unpause', c['Id'])
        pauses[name] = round(time.monotonic() - began, 3)
        print(name + ': consistent volume snapshot', flush=True)
    for name in PG:
        c = inventory[name]; env = dict(e.split('=', 1) for e in c['Config']['Env'])
        user = env.get('POSTGRES_USER', 'postgres'); folder = stage / name; folder.mkdir()
        databases = run('docker', 'exec', c['Id'], 'psql', '-U', user, '-d', 'postgres', '-At', '-c',
                        'SELECT datname FROM pg_database WHERE datallowconn AND NOT datistemplate ORDER BY datname').splitlines()
        with (folder / 'globals.sql').open('wb') as out:
            run('docker', 'exec', c['Id'], 'pg_dumpall', '-U', user, '--globals-only', output=out)
        mapping = []
        for i, db in enumerate(databases):
            file = f'db-{i}.dump'
            with (folder / file).open('wb') as out:
                run('docker', 'exec', c['Id'], 'pg_dump', '-U', user, '-Fc', '-d', db, output=out)
            mapping.append({'db': db, 'file': file})
        write(folder / 'mapping-private.json', mapping)
        print(name + ': logical dumps complete', flush=True)
    with tarfile.open(stage / 'configuration-private.tar', 'w') as tar:
        paths = [Path('/opt/monitor-orion'), Path('/etc/wireguard'), Path('/root/guarderia-ops'),
                 *Path('/root').glob('*.yaml'), *Path('/etc/systemd/system').glob('guarderia-backup*'),
                 *Path('/etc/systemd/system').glob('guarderia-panel-firewall.service'),
                 *Path('/etc/systemd/system').glob('guarderia-host-firewall.service'),
                 *Path('/etc/systemd/system').glob('guarderia-reboot-check.*'),
                 *Path('/etc/systemd/system').glob('guarderia-heartbeat.*')]
        for p in paths:
            if p.exists(): tar.add(p, arcname=str(p).lstrip('/'))
    # Passive inventory: no network/firewall mutations.
    for name, command in {'routes': ['ip', 'route', 'show', 'table', 'all'],
                          'rules': ['ip', 'rule', 'show'], 'firewall-v4': ['iptables-save'],
                          'firewall-v6': ['ip6tables-save']}.items():
        with (stage / (name + '-private.txt')).open('wb') as out: run(*command, output=out)
    manifest = [{'path': str(p.relative_to(stage)), 'bytes': p.stat().st_size, 'sha256': digest(p)}
                for p in sorted(stage.rglob('*')) if p.is_file()]
    write(stage / 'manifest.json', manifest)
    payload = stage / 'payload.tar.gz'
    with tarfile.open(payload, 'w:gz') as tar:
        for item in manifest: tar.add(stage / item['path'], arcname=item['path'])
        tar.add(stage / 'manifest.json', arcname='manifest.json')
    partial = stage / 'encrypted.gpg'
    gpg('--cipher-algo', 'AES256', '--compress-algo', 'none', '--output', str(partial),
        '--symmetric', str(payload))
    count = verify(partial)
    final = ROOT / 'archives' / ('backup-' + stamp.strftime('%Y%m%dT%H%M%SZ') + '.gpg')
    os.replace(partial, final)
    receipt = {'timestamp': stamp.isoformat(), 'verified': True, 'files': count,
               'bytes': final.stat().st_size, 'sha256': digest(final), 'pause_seconds': pauses,
               'duration_seconds': round(time.monotonic() - started, 3), 'offsite': False}
    write(final.with_suffix('.json'), receipt)
    write(ROOT / 'status.json', {'last_attempt_ok': True, 'last_success': stamp.isoformat(),
                                'archive': str(final), 'offsite': False})
    shutil.rmtree(stage); retention()
    print(json.dumps(receipt, indent=2), flush=True)
    return final


def health(testname, port, path):
    for _ in range(60):
        try:
            c = js('docker', 'inspect', testname)[0]
            if not c['State']['Running']: raise RuntimeError('not running')
            return run('nsenter', '-t', str(c['State']['Pid']), '-n', 'curl', '--fail', '--silent',
                       '--max-time', '3', f'http://127.0.0.1:{port}{path}', timeout=5)
        except (RuntimeError, subprocess.TimeoutExpired): time.sleep(1)
    raise RuntimeError(testname + ': isolated health check timed out')


def restore_test(archive):
    started = time.monotonic()
    folder = Path(tempfile.mkdtemp(prefix='restore-', dir=ROOT)); verify(archive, folder)
    inventory = json.loads((folder / 'containers-private.json').read_text()); results = []
    config = folder / 'config'; config.mkdir()
    with tarfile.open(folder / 'configuration-private.tar') as tar: tar.extractall(config, filter='data')
    for name, target in APPS.items():
        data = folder / (name + '-data'); data.mkdir()
        with tarfile.open(folder / (name + '.tar')) as tar: tar.extractall(data, filter='data')
        if name == 'traefik_traefik':
            certs = 0
            for p in data.rglob('*.json'):
                obj = json.loads(p.read_text())
                for resolver in obj.values():
                    if not isinstance(resolver, dict): continue
                    for cert in resolver.get('Certificates', []):
                        pem = base64.b64decode(cert['certificate']); key = base64.b64decode(cert['key'])
                        public = run('openssl', 'x509', '-pubkey', '-noout', data=pem)
                        assert public == run('openssl', 'pkey', '-pubout', data=key)
                        run('openssl', 'x509', '-checkend', '0', '-noout', data=pem); certs += 1
            assert certs > 0, 'No certificates restored'
            results.append({'service': name, 'certificate_key_pairs_valid': certs,
                            'tls_endpoint_restore': 'not tested'})
            continue
        uid = 472 if name == 'monitor_grafana' else 65534 if name == 'monitor_prometheus' else 0
        for p in [data, *data.rglob('*')]:
            if not p.is_symlink(): os.chown(p, uid, 0)
        os.chmod(data, 0o750)
        testname = 'guarderia-backup-test-' + name.replace('_', '-')
        command = ['docker', 'run', '-d', '--pull', 'never', '--name', testname, '--network', 'none',
                   '--cpus', '1', '--memory', '768m', '--mount', f'type=bind,src={data},dst={target}']
        if name in ['monitor_grafana', 'monitor_prometheus']:
            for mount in inventory[name]['Mounts']:
                if mount['Type'] == 'bind':
                    source = config / mount['Source'].lstrip('/')
                    assert source.exists()
                    command += ['--mount', f'type=bind,src={source},dst={mount["Destination"]},readonly']
        command.append(inventory[name]['Image'])
        if name == 'portainer_portainer': command += ['--http-enabled']
        try:
            run(*command)
            port, path = {'monitor_grafana': (3000, '/api/health'), 'monitor_prometheus': (9090, '/-/ready'),
                          'uptimekuma_uptimekuma': (3001, '/'), 'portainer_portainer': (9000, '/api/status')}[name]
            for cycle in range(2):
                if cycle: run('docker', 'restart', testname)
                response = health(testname, port, path)
                if name == 'monitor_grafana': assert json.loads(response)['database'] == 'ok'
            if name == 'monitor_prometheus':
                response = json.loads(health(testname, 9090, '/api/v1/query?query=prometheus_tsdb_head_series'))
                # Source metric is present in the copied TSDB; network none cannot collect production.
                assert response['status'] == 'success'
                series = json.loads(health(testname, 9090, '/api/v1/status/tsdb'))['data']['headStats']['numSeries']
                assert series > 0
            if name in ['monitor_grafana', 'uptimekuma_uptimekuma']:
                dbname = 'grafana.db' if name == 'monitor_grafana' else 'kuma.db'
                with sqlite3.connect('file:' + str(data / dbname) + '?mode=ro', uri=True) as db:
                    assert db.execute('pragma integrity_check').fetchone()[0] == 'ok'
            results.append({'service': name, 'startup': 'ok', 'restart': 'ok',
                            'scope': 'isolated copy; no login or real notifications'})
            print(name + ': isolated startup/restart OK', flush=True)
        finally:
            with (folder / (name + '-private.log')).open('wb') as out:
                subprocess.run(['docker', 'logs', testname], stdout=out, stderr=subprocess.STDOUT)
            subprocess.run(['docker', 'rm', '-f', testname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for name in PG:
        c = inventory[name]; source = folder / name; data = folder / (name + '-data'); data.mkdir()
        testname = 'guarderia-backup-test-' + name.replace('_', '-')
        try:
            run('docker', 'run', '-d', '--pull', 'never', '--name', testname, '--network', 'none',
                '--cpus', '1', '--memory', '768m', '-e', 'POSTGRES_USER=restore_audit_admin',
                '-e', 'POSTGRES_HOST_AUTH_METHOD=trust', '--mount', f'type=bind,src={data},dst=/var/lib/postgresql/data',
                '--mount', f'type=bind,src={source},dst=/backup,readonly', c['Image'])
            for _ in range(60):
                try: run('docker', 'exec', testname, 'pg_isready', '-h', '127.0.0.1', '-U', 'restore_audit_admin', '-d', 'postgres'); break
                except RuntimeError: time.sleep(1)
            else: raise RuntimeError('Isolated PostgreSQL startup timed out')
            with (source / 'restore-private.log').open('wb') as out:
                run('docker', 'exec', testname, 'psql', '-U', 'restore_audit_admin', '-d', 'postgres',
                    '-v', 'ON_ERROR_STOP=1', '-f', '/backup/globals.sql', output=out)
                mapping = json.loads((source / 'mapping-private.json').read_text())
                for item in mapping:
                    run('docker', 'exec', testname, 'pg_restore', '-U', 'restore_audit_admin', '-d', 'template1',
                        '--clean', '--if-exists', '--create', '--exit-on-error', '/backup/' + item['file'], output=out)
            tables = [int(run('docker', 'exec', testname, 'psql', '-U', 'restore_audit_admin', '-d', item['db'],
                             '-At', '-c', "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")) for item in mapping]
            results.append({'service': name, 'restored_databases': len(mapping), 'public_tables': tables})
            print(name + ': isolated database restore OK', flush=True)
        finally:
            subprocess.run(['docker', 'rm', '-f', testname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    report = {'archive': archive.name, 'results': results, 'seconds': round(time.monotonic() - started, 3),
              'full_vps_recovery': False, 'offsite_recovery': False}
    write(ROOT / 'restore-last.json', report)
    print(json.dumps(report, indent=2), flush=True)
    # Keep small logs/report; remove only this test's extracted private copies after success.
    shutil.rmtree(folder)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('action', choices=['backup', 'verify', 'restore-test', 'status'])
    parser.add_argument('--archive', type=Path); args = parser.parse_args()
    ROOT.mkdir(mode=0o700, exist_ok=True)
    with (ROOT / 'operation.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.action == 'status':
            status = json.loads((ROOT / 'status.json').read_text())
            age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(status['last_success'])).total_seconds()
            print(json.dumps({**status, 'age_hours': round(age / 3600, 2)}))
            return 0 if status['last_attempt_ok'] and age < 26 * 3600 else 2
        (ROOT / 'archives').mkdir(mode=0o700, exist_ok=True)
        (ROOT / 'gnupg').mkdir(mode=0o700, exist_ok=True)
        if not KEY.exists():
            if list((ROOT / 'archives').glob('*.gpg')): raise RuntimeError('Recovery key missing; refusing replacement')
            with KEY.open('x') as key: key.write(secrets.token_urlsafe(48) + '\n')
        if args.action == 'backup':
            archive = backup()
            config = Path('/root/guarderia-ops/s3-config.json')
            if config.exists() and json.loads(config.read_text()).get('enabled'):
                run('/usr/bin/python3', '/root/guarderia-ops/s3_backup.py', '--archive', str(archive), timeout=3600)
                print('S3 upload and downloaded SHA-256 verification complete', flush=True)
        else:
            archive = args.archive or Path(json.loads((ROOT / 'status.json').read_text())['archive'])
            if args.action == 'verify': print('Verified files:', verify(archive))
            else: restore_test(archive)
    return 0


if __name__ == '__main__':
    def interrupted(signum, frame): raise RuntimeError('Interrupted by signal ' + str(signum))
    signal.signal(signal.SIGTERM, interrupted)
    try: sys.exit(main())
    except Exception as exc:
        if len(sys.argv) > 1 and sys.argv[1] == 'backup' and ROOT.exists():
            status_path = ROOT / 'status.json'
            state = json.loads(status_path.read_text()) if status_path.exists() else {}
            state.update(last_attempt_ok=False, last_error_type=type(exc).__name__,
                         last_attempt=dt.datetime.now(dt.timezone.utc).isoformat())
            write(status_path, state)
        print(f'Backup operation failed: {exc}', file=sys.stderr); sys.exit(1)
