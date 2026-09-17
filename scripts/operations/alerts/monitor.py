"""Avaliador externo; nenhum token ou resposta privada deve ser registrado em log."""
import datetime,json,os,urllib.request

def timestamp(value):
 try:return datetime.datetime.fromisoformat(value.replace('Z','+00:00')).timestamp()
 except (ValueError,TypeError,AttributeError):return None

def evaluate(heartbeat,last_modified,now):
 if last_modified is None or now-last_modified>=900:return ['heartbeat_ausente_15min']
 reasons=[]
 running=heartbeat.get('backup_active_state') in ['activating','active']
 if not running and (not heartbeat.get('last_attempt_ok') or heartbeat.get('backup_service_result')!='success'):reasons.append('falha_backup')
 if not running and not heartbeat.get('offsite_current'):reasons.append('copia_s3_atual_nao_verificada')
 verified=timestamp(heartbeat.get('last_verified_remote_at'))
 if verified is None or verified>now+300 or now-verified>=26*3600:reasons.append('backup_s3_sem_verificacao_26h')
 return reasons

def get_json(s3,bucket,key):
 try:
  obj=s3.get_object(Bucket=bucket,Key=key)
  return json.loads(obj['Body'].read()),obj['LastModified'].timestamp()
 except s3.exceptions.NoSuchKey:return {},None

def send_ses(client,message):
 client.send_email(FromEmailAddress=os.environ['SENDER'],Destination={'ToAddresses':[os.environ['RECIPIENT']]},Content={'Simple':{'Subject':{'Data':'[Guarderia] Estado do backup e heartbeat','Charset':'UTF-8'},'Body':{'Text':{'Data':message,'Charset':'UTF-8'}}}})

def send_telegram(ssm,message):
 secret=json.loads(ssm.get_parameter(Name=os.environ['TELEGRAM_PARAMETER'],WithDecryption=True)['Parameter']['Value'])
 req=urllib.request.Request('https://api.telegram.org/bot'+secret['token']+'/sendMessage',data=json.dumps({'chat_id':secret['chat_id'],'text':message}).encode(),headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=10) as response:result=json.load(response)
  if not result.get('ok'):raise RuntimeError('rejected')
 except Exception:raise RuntimeError('Telegram delivery failed; secret details omitted') from None

def handler(event,context):
 import boto3
 now=datetime.datetime.now(datetime.timezone.utc).timestamp();bucket=os.environ['BUCKET'];prefix=os.environ['PREFIX']
 s3=boto3.client('s3');test_case=event.get('test_case')
 if test_case not in [None,'failure','missing','overdue','recovery']:raise ValueError('Unknown test case')
 state_key=prefix+('monitor/notification-test-state.json' if test_case else 'monitor/notification-state.json')
 hb,modified=get_json(s3,bucket,prefix+'monitor/heartbeat.json');previous,_=get_json(s3,bucket,state_key)
 if test_case:
  hb={'backup_active_state':'inactive','backup_service_result':'success','last_attempt_ok':True,'offsite_current':True,'last_verified_remote_at':datetime.datetime.fromtimestamp(now,datetime.timezone.utc).isoformat()};modified=now
  if test_case=='failure':hb.update(last_attempt_ok=False,offsite_current=False)
  if test_case=='missing':modified=now-901
  if test_case=='overdue':hb['last_verified_remote_at']='2020-01-01T00:00:00+00:00'
 reasons=evaluate(hb,modified,now);signature=','.join(reasons) or 'ok'
 # Remember each channel independently: a Telegram failure must not repeat a successful email.
 channels=previous.get('channels',{});errors=[]
 message=('ALERTA Guarderia: '+', '.join(reasons) if reasons else 'RECUPERADO Guarderia: heartbeat recente e backup S3 verificado.')
 if 'heartbeat_ausente_15min' in reasons:message+=' VPS, conectividade, credenciais ou publicador podem estar indisponiveis; causa ainda nao determinada.'
 if test_case:message='[TESTE CONTROLADO - nao indica incidente real] '+message
 message+='\nUTC: '+datetime.datetime.fromtimestamp(now,datetime.timezone.utc).isoformat()
 senders={'email':lambda:send_ses(boto3.client('sesv2'),message),'telegram':lambda:send_telegram(boto3.client('ssm'),message)}
 for channel,send in senders.items():
  old=channels.get(channel,{})
  # Do not send recovery to a channel that never received an incident.
  due=(bool(reasons) and (old.get('signature')!=signature or now-old.get('sent_at',0)>=21600)) or (not reasons and old.get('signature') not in [None,'ok'])
  if not due:continue
  try:send();channels[channel]={'signature':signature,'sent_at':now}
  except Exception as exc:
   detail=getattr(exc,'response',{}).get('Error',{})
   errors.append(channel+': '+detail.get('Code','delivery_failed')+(' '+detail.get('Message','') if channel=='email' else ''))
 s3.put_object(Bucket=bucket,Key=state_key,Body=json.dumps({'checked_at':now,'signature':signature,'channels':channels}).encode(),ContentType='application/json',ServerSideEncryption='AES256')
 if errors:raise RuntimeError('Notification channel failure: '+','.join(errors))
 return {'status':signature,'channels_tracked':sorted(channels)}
