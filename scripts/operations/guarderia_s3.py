#!/usr/bin/env python3
"""Upload de arquivos GPG já verificados; nenhuma chave de recuperação é enviada."""
import argparse,datetime,hashlib,json,os,subprocess,tempfile
from pathlib import Path
ROOT=Path('/root/guarderia-backups')
CONFIG=Path('/root/guarderia-ops/s3-config.json')
AWS='/root/.local/bin/aws'
os.umask(0o077)

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def call(config,*args):
 env={**os.environ,'AWS_EC2_METADATA_DISABLED':'true','AWS_PAGER':''}
 p=subprocess.run([AWS,'--profile',config['profile'],'--region',config['region'],'--no-cli-pager','--output','json',*args],
                  stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=1800)
 if p.returncode:
  (ROOT/'s3-error-private.txt').write_bytes(p.stderr)
  raise RuntimeError('AWS command failed; diagnostic in /root/guarderia-backups/s3-error-private.txt')
 return json.loads(p.stdout) if p.stdout.strip() else {}

def upload(archive):
 cfg=json.loads(CONFIG.read_text());bucket=cfg['bucket'];prefix=cfg['prefix']
 assert prefix and not prefix.startswith('/') and prefix.endswith('/')
 assert archive.parent.resolve()==(ROOT/'archives').resolve() and archive.suffix=='.gpg'
 receipt=json.loads(archive.with_suffix('.json').read_text())
 assert receipt['verified'] and digest(archive)==receipt['sha256']
 location=call(cfg,'s3api','get-bucket-location','--bucket',bucket).get('LocationConstraint') or 'us-east-1'
 assert location==cfg['region'],'Unexpected bucket region'
 block=call(cfg,'s3api','get-public-access-block','--bucket',bucket)['PublicAccessBlockConfiguration']
 assert all(block.get(k) for k in ['BlockPublicAcls','IgnorePublicAcls','BlockPublicPolicy','RestrictPublicBuckets']), 'Bucket public access block requires review'
 version=call(cfg,'s3api','get-bucket-versioning','--bucket',bucket).get('Status','Disabled')
 key=prefix+archive.name;uri='s3://'+bucket+'/'+key
 # Unique dated keys; no sync --delete and no recovery key upload.
 call(cfg,'s3','cp',str(archive),uri,'--only-show-errors','--sse','AES256',
      '--metadata',json.dumps({'sha256':receipt['sha256']}))
 with tempfile.TemporaryDirectory(prefix='.s3-check-',dir=ROOT) as td:
  downloaded=Path(td)/archive.name
  call(cfg,'s3','cp',uri,str(downloaded),'--only-show-errors')
  assert digest(downloaded)==receipt['sha256'],'Downloaded backup checksum mismatch'
 call(cfg,'s3','cp',str(archive.with_suffix('.json')),'s3://'+bucket+'/'+prefix+archive.with_suffix('.json').name,
      '--only-show-errors','--sse','AES256')
 result={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':archive.name,
         'uri':uri,'sha256':receipt['sha256'],'download_verified':True,'versioning':version,
         'recovery_key_offsite':('confirmed by user; external copy not tested' if (ROOT/'key-custody.json').exists() else 'pending user escrow'),'bucket_lifecycle':'not modified'}
 temp=ROOT/'s3-last.json.tmp';temp.write_text(json.dumps(result,indent=2));os.replace(temp,ROOT/'s3-last.json')
 status=json.loads((ROOT/'status.json').read_text());status['offsite']=True;status['offsite_archive']=archive.name
 temp=ROOT/'status.json.tmp';temp.write_text(json.dumps(status,indent=2));os.replace(temp,ROOT/'status.json')
 print(json.dumps(result,indent=2))

def restore_from_s3():
 import importlib.util,fcntl
 cfg=json.loads(CONFIG.read_text());remote=json.loads((ROOT/'s3-last.json').read_text())
 with (ROOT/'operation.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  with tempfile.TemporaryDirectory(prefix='.s3-restore-',dir=ROOT) as td:
   downloaded=Path(td)/remote['archive']
   call(cfg,'s3','cp',remote['uri'],str(downloaded),'--only-show-errors')
   assert digest(downloaded)==remote['sha256']
   spec=importlib.util.spec_from_file_location('guarderia_backup','/root/guarderia-ops/backup.py')
   module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
   module.restore_test(downloaded)
   report=json.loads((ROOT/'restore-last.json').read_text())
   report.update(offsite_recovery=True,source_uri=remote['uri'],external_key_recovery_tested=False)
   module.write(ROOT/'restore-last.json',report)
   remote['component_restore_from_s3']=True
   module.write(ROOT/'s3-last.json',remote)

def enable_daily():
 remote=json.loads((ROOT/'s3-last.json').read_text())
 assert remote.get('component_restore_from_s3') and remote['download_verified']
 cfg=json.loads(CONFIG.read_text());cfg['enabled']=True
 temp=CONFIG.with_suffix('.tmp');temp.write_text(json.dumps(cfg,indent=2));os.replace(temp,CONFIG)
 print('Daily S3 upload enabled after verified download and isolated restore')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--archive',type=Path)
 parser.add_argument('--restore-test',action='store_true');parser.add_argument('--enable-daily',action='store_true')
 args=parser.parse_args()
 if args.restore_test:restore_from_s3()
 elif args.enable_daily:enable_daily()
 else:
  archive=args.archive or Path(json.loads((ROOT/'status.json').read_text())['archive'])
  upload(archive)
