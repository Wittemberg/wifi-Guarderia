#!/usr/bin/env python3
"""Publica somente estado operacional, sem credenciais, logs ou conteudo dos backups."""
import datetime,json,os,subprocess,tempfile
from pathlib import Path
os.umask(0o077)
ROOT=Path('/root/guarderia-backups')
def read(name):
 try:return json.loads((ROOT/name).read_text())
 except (OSError,ValueError):return {}
def snapshot():
 state=read('status.json');remote=read('s3-last.json')
 p=subprocess.run(['systemctl','show','guarderia-backup.service','-p','ActiveState','-p','Result'],capture_output=True,text=True,timeout=10)
 props=dict(x.split('=',1) for x in p.stdout.splitlines() if '=' in x)
 return {'schema':1,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'backup_active_state':props.get('ActiveState','unknown'),'backup_service_result':props.get('Result','unknown'),'last_attempt_ok':state.get('last_attempt_ok',False),'last_success':state.get('last_success'),'offsite_current':bool(state.get('offsite') and state.get('offsite_archive')==remote.get('archive')),'last_verified_remote_at':remote.get('timestamp') if remote.get('download_verified') else None,'last_verified_archive':remote.get('archive') if remote.get('download_verified') else None}
def main():
 cfg=json.loads(Path('/root/guarderia-ops/s3-config.json').read_text());data=snapshot()
 with tempfile.TemporaryDirectory(prefix='guarderia-heartbeat-') as td:
  p=Path(td)/'heartbeat.json';p.write_text(json.dumps(data))
  result=subprocess.run(['/root/.local/bin/aws','--profile',cfg['profile'],'--region',cfg['region'],'--no-cli-pager','s3api','put-object','--bucket',cfg['bucket'],'--key',cfg['prefix']+'monitor/heartbeat.json','--body',str(p),'--server-side-encryption','AES256','--content-type','application/json'],capture_output=True,text=True,timeout=45)
  if result.returncode:raise RuntimeError('Nao foi possivel publicar heartbeat no S3; detalhes privados omitidos')
 print('Heartbeat publicado; isto nao confirma operacao do monitor externo.')
if __name__=='__main__':main()
