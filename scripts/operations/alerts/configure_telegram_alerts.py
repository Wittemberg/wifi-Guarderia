#!/usr/bin/env python3
"""Configura um bot dedicado sem expor o token em argumentos, logs ou historico."""
import getpass,json,os,secrets,sys,urllib.request,urllib.error
from pathlib import Path
os.umask(0o077)
root=Path('/root/.config/guarderia-alerts');root.mkdir(parents=True,exist_ok=True);root.chmod(0o700)
def api(token,method,payload=None):
 request=urllib.request.Request('https://api.telegram.org/bot'+token+'/'+method,data=json.dumps(payload or {}).encode(),headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(request,timeout=20) as response:d=json.load(response)
 except Exception:raise RuntimeError('Falha ao consultar Telegram. Confira token e conexao; detalhes com token foram ocultados.') from None
 if not d.get('ok'):raise RuntimeError('Telegram recusou a operacao; token e resposta privados nao serao exibidos.')
 return d['result']
def main():
 dest=root/'telegram.json'
 if dest.exists():raise RuntimeError('Configuracao Telegram ja existe; preservar antes de substituir.')
 token=getpass.getpass('Cole o token do BotFather (entrada oculta): ').strip()
 me=api(token,'getMe');webhook=api(token,'getWebhookInfo')
 if webhook.get('url'):raise RuntimeError('Este bot tem webhook configurado. Use um bot dedicado; nada foi alterado.')
 nonce='guarderia_'+secrets.token_hex(8)
 print('No Telegram, abra @'+me['username']+' e envie em conversa PRIVADA:')
 print('/start '+nonce)
 input('Depois de enviar, pressione Enter aqui: ')
 updates=api(token,'getUpdates',{'limit':100,'timeout':0})
 matches=[x['message']['chat'] for x in updates if x.get('message',{}).get('text')=='/start '+nonce and x['message']['chat'].get('type')=='private']
 ids={x['id'] for x in matches}
 if len(ids)!=1:raise RuntimeError('Nao foi encontrada uma unica conversa com o codigo. Execute novamente e envie o novo codigo.')
 chat_id=next(iter(ids))
 data={'token':token,'chat_id':chat_id,'bot_username':me['username']}
 fd=os.open(dest,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 with os.fdopen(fd,'w') as f:json.dump(data,f)
 print('Configuracao salva com permissao 600. Nenhuma mensagem de alerta foi enviada ainda.')
if __name__=='__main__':
 try:main()
 except Exception as e:print('ERRO: '+str(e));sys.exit(1)
