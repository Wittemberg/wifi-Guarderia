#!/usr/bin/env python3
import json,subprocess,time,datetime,os,sys
from pathlib import Path
os.umask(0o077)
b=Path(Path('/root/guarderia-evidencias/reboot-current.txt').read_text())
before=json.loads((b/'preflight-private.json').read_text())
def r(*a):return subprocess.check_output(a,text=True,stderr=subprocess.STDOUT,timeout=25).strip()
def check():
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
 out={'utc':now,'boot_id':boot,'boot_changed':boot!=before['boot_id'],'uptime_seconds':float(Path('/proc/uptime').read_text().split()[0]),'checks':{},'errors':[]}
 def test(name,fn):
  try:out['checks'][name]=fn()
  except Exception as e:out['errors'].append(name+': '+str(e)[:300])
 def units():
  d={u:{'active':r('systemctl','is-active',u),'enabled':r('systemctl','is-enabled',u)} for u in before['units']}
  assert all(x['active']=='active' and x['enabled']=='enabled' for x in d.values());return d
 test('units',units)
 def services():
  s=r('docker','service','ls','--format','{{.Name}} {{.Replicas}}');assert len(s.splitlines())==12 and all(x.endswith(' 1/1') for x in s.splitlines());return s
 test('services',services)
 def targets():
  cid=r('docker','ps','-q','--filter','label=com.docker.swarm.service.name=monitor_prometheus')
  ts=json.loads(r('docker','exec',cid,'wget','-qO-','http://127.0.0.1:9090/api/v1/targets'))['data']['activeTargets']
  assert len(ts)==3 and all(t['health']=='up' for t in ts);return {'count':len(ts),'all_up':True}
 test('prometheus_targets',targets)
 def definitions():
  old=json.loads((b/'docker-services-private.txt').read_text());new=json.loads(r('docker','service','inspect',*[x['ID'] for x in old]));d={x['ID']:x for x in new}
  for x in old:
   c=d[x['ID']];assert x['Spec'].get('Labels')==c['Spec'].get('Labels');assert x['Spec']['TaskTemplate']['ContainerSpec'].get('Mounts')==c['Spec']['TaskTemplate']['ContainerSpec'].get('Mounts')
  return 'labels and mounts preserved for all services'
 test('definitions',definitions)
 def filters():
  host=r('python3','/root/guarderia-ops/guarderia_host_firewall.py','status');panel=r('python3','/root/guarderia-ops/guarderia_panel_firewall.py','status');assert all(json.loads(x)['jump_present'] for x in panel.splitlines());return {'host':host,'panel':panel}
 test('filters',filters)
 def vpn():
  route=r('ip','route','show','dev','wg0');assert '10.250.0.10' in route;return route
 test('vpn_route',vpn)
 def tls():
  results={}
  for name in ['portainer','grafana','zabbix','status','prometheus','cadvisor','node']:
   domain=name+'-guarderia.awecloudsolution.com';code=int(r('curl','--silent','--show-error','--noproxy','*','--max-time','8','--resolve',domain+':443:10.250.0.1','-o','/dev/null','-w','%{http_code}','https://'+domain+'/'))
   results[name]=code;assert code in [200,301,302,303,307,308,401]
  return results
 test('vpn_tls',tls)
 test('failed_units',lambda:r('systemctl','--failed','--no-pager'))
 out['ok']=not out['errors'] and (out['boot_changed'] or '--dry-run' in sys.argv)
 return out
if '--dry-run' in sys.argv:
 result=check();(b/'postcheck-dry-run.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));sys.exit(0 if result['ok'] else 1)
if Path('/proc/sys/kernel/random/boot_id').read_text().strip()==before['boot_id']:
 print('Awaiting a new boot; no post-reboot success recorded');sys.exit(0)
for attempt in range(24):
 result=check();result['attempt']=attempt+1
 target=b/'post-reboot.json';tmp=b/'post-reboot.tmp';tmp.write_text(json.dumps(result,indent=2));tmp.replace(target)
 if result['ok']:break
 time.sleep(10)
print(json.dumps(result,indent=2));sys.exit(0 if result['ok'] else 1)
