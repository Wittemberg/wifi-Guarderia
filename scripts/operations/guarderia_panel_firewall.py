#!/usr/bin/env python3
"""Filtro proprio antes do DNAT: quatro portas de painel, somente entrada eth0."""
import subprocess,sys,json
CHAIN='GV_PANEL_PUBLIC'
JUMP=['-i','eth0','-m','addrtype','--dst-type','LOCAL','-j',CHAIN]
RULE=['-p','tcp','-m','multiport','--dports','3111,8181,9191,9100','-j','DROP']
def cmd(binary,*args,check=True):
 p=subprocess.run([binary,'-w','5','-t','raw',*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if check and p.returncode:raise RuntimeError(binary+' firewall operation failed')
 return p
mode=sys.argv[1] if len(sys.argv)>1 else 'status'
assert mode in ['apply','remove','status']
for binary in ['iptables','ip6tables']:
 exists=cmd(binary,'-S',CHAIN,check=False).returncode==0
 if mode=='apply':
  if not exists:cmd(binary,'-N',CHAIN)
  actual=cmd(binary,'-S',CHAIN).stdout.splitlines()
  allowed='-A '+CHAIN+' '+' '.join(RULE)
  assert all(line.startswith('-N ') or line==allowed for line in actual),'Unexpected rules in owned chain'
  if cmd(binary,'-C',CHAIN,*RULE,check=False).returncode:cmd(binary,'-A',CHAIN,*RULE)
  if cmd(binary,'-C','PREROUTING',*JUMP,check=False).returncode:cmd(binary,'-I','PREROUTING','1',*JUMP)
 elif mode=='remove' and exists:
  if cmd(binary,'-C','PREROUTING',*JUMP,check=False).returncode==0:cmd(binary,'-D','PREROUTING',*JUMP)
  cmd(binary,'-F',CHAIN);cmd(binary,'-X',CHAIN)
 print(json.dumps({'family':binary,'mode':mode,'jump_present':cmd(binary,'-C','PREROUTING',*JUMP,check=False).returncode==0}))
