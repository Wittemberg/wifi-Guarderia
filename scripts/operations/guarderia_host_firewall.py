#!/usr/bin/env python3
import subprocess,sys
RULESETS=[('raw','GV_HOST_PUBLIC','PREROUTING',['-i','eth0','-m','addrtype','--dst-type','LOCAL'],[
 ['-p','tcp','-m','multiport','--dports','111,2377,7946,10051','-j','DROP'],
 ['-p','udp','-m','multiport','--dports','111,7946,4789','-j','DROP']]),
 ('filter','GV_SSH_PUBLIC','INPUT',['-i','eth0','-p','tcp','--dport','5822'],[
 ['-m','conntrack','--ctstate','ESTABLISHED,RELATED','-j','RETURN'],['-j','DROP']])]
def call(binary,table,*args,check=True):
 p=subprocess.run([binary,'-w','5','-t',table,*args],text=True,capture_output=True)
 if check and p.returncode:raise RuntimeError(p.stderr)
 return p
mode=sys.argv[1];assert mode in ['apply','remove','status']
for binary in ['iptables','ip6tables']:
 for table,chain,parent,match,rules in RULESETS:
  exists=call(binary,table,'-S',chain,check=False).returncode==0
  jump=match+['-j',chain]
  if mode=='apply':
   if not exists:call(binary,table,'-N',chain)
   actual=call(binary,table,'-S',chain).stdout.splitlines()
   allowed=['-A '+chain+' '+' '.join(x) for x in rules]
   normalize=lambda x:x.replace('ESTABLISHED,RELATED','RELATED,ESTABLISHED')
   assert all(x.startswith('-N ') or normalize(x) in [normalize(y) for y in allowed] for x in actual),'Unexpected owned chain contents'
   for rule in rules:
    if call(binary,table,'-C',chain,*rule,check=False).returncode:call(binary,table,'-A',chain,*rule)
   if call(binary,table,'-C',parent,*jump,check=False).returncode:call(binary,table,'-I',parent,'1',*jump)
  elif mode=='remove' and exists:
   if call(binary,table,'-C',parent,*jump,check=False).returncode==0:call(binary,table,'-D',parent,*jump)
   call(binary,table,'-F',chain);call(binary,table,'-X',chain)
  present=call(binary,table,'-C',parent,*jump,check=False).returncode==0
  print(binary,table,chain,'present='+str(present))
  if mode=='status':
   assert present
   for rule in rules:assert call(binary,table,'-C',chain,*rule,check=False).returncode==0
