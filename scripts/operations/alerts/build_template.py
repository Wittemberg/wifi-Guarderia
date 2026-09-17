"""Gera CloudFormation revisavel, sem token nem identidade pessoal embutida."""
import json
from pathlib import Path
P=Path(__file__).parent
sub=lambda s:{'Fn::Sub':s}
ref=lambda s:{'Ref':s}
get=lambda s,a:{'Fn::GetAtt':[s,a]}
t={'AWSTemplateFormatVersion':'2010-09-09','Description':'Guarderia external backup and heartbeat alerts','Parameters':{'Bucket':{'Type':'String'},'Prefix':{'Type':'String','Default':'guarderia/vps/'},'Sender':{'Type':'String'},'Recipient':{'Type':'String'},'TelegramParameter':{'Type':'String','Default':'/guarderia/alerts/telegram'},'ScheduleState':{'Type':'String','Default':'DISABLED','AllowedValues':['ENABLED','DISABLED']}},'Resources':{}}
r=t['Resources']
r['Role']={'Type':'AWS::IAM::Role','Properties':{'AssumeRolePolicyDocument':{'Version':'2012-10-17','Statement':[{'Effect':'Allow','Principal':{'Service':'lambda.amazonaws.com'},'Action':'sts:AssumeRole'}]},'Policies':[{'PolicyName':'guarderia-alerts-only','PolicyDocument':{'Version':'2012-10-17','Statement':[
 {'Effect':'Allow','Action':['s3:ListBucket'],'Resource':sub('arn:${AWS::Partition}:s3:::${Bucket}')},
 {'Effect':'Allow','Action':['s3:GetObject'],'Resource':[sub('arn:${AWS::Partition}:s3:::${Bucket}/${Prefix}monitor/heartbeat.json'),sub('arn:${AWS::Partition}:s3:::${Bucket}/${Prefix}monitor/notification-state.json'),sub('arn:${AWS::Partition}:s3:::${Bucket}/${Prefix}monitor/notification-test-state.json')]},
 {'Effect':'Allow','Action':['s3:PutObject'],'Resource':[sub('arn:${AWS::Partition}:s3:::${Bucket}/${Prefix}monitor/notification-state.json'),sub('arn:${AWS::Partition}:s3:::${Bucket}/${Prefix}monitor/notification-test-state.json')]},
 {'Effect':'Allow','Action':['ses:SendEmail'],'Resource':[sub('arn:${AWS::Partition}:ses:${AWS::Region}:${AWS::AccountId}:identity/${Sender}'),sub('arn:${AWS::Partition}:ses:${AWS::Region}:${AWS::AccountId}:identity/${Recipient}')],'Condition':{'StringEquals':{'ses:FromAddress':ref('Sender')},'ForAllValues:StringEquals':{'ses:Recipients':[ref('Recipient')]}}},
 {'Effect':'Allow','Action':['ssm:GetParameter'],'Resource':sub('arn:${AWS::Partition}:ssm:${AWS::Region}:${AWS::AccountId}:parameter${TelegramParameter}')},
 {'Effect':'Allow','Action':['logs:CreateLogStream','logs:PutLogEvents'],'Resource':sub('arn:${AWS::Partition}:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/guarderia-backup-watchdog:*')}
 ]}}]}}
r['LogGroup']={'Type':'AWS::Logs::LogGroup','Properties':{'LogGroupName':'/aws/lambda/guarderia-backup-watchdog','RetentionInDays':14}}
r['Function']={'Type':'AWS::Lambda::Function','DependsOn':['LogGroup'],'Properties':{'FunctionName':'guarderia-backup-watchdog','Runtime':'python3.12','Handler':'index.handler','Role':get('Role','Arn'),'Timeout':60,'MemorySize':128,'Code':{'ZipFile':(P/'monitor.py').read_text()},'Environment':{'Variables':{'BUCKET':ref('Bucket'),'PREFIX':ref('Prefix'),'SENDER':ref('Sender'),'RECIPIENT':ref('Recipient'),'TELEGRAM_PARAMETER':ref('TelegramParameter')}}}}
r['Rule']={'Type':'AWS::Events::Rule','Properties':{'ScheduleExpression':'rate(5 minutes)','State':ref('ScheduleState'),'Targets':[{'Arn':get('Function','Arn'),'Id':'GuarderiaWatchdog','RetryPolicy':{'MaximumEventAgeInSeconds':300,'MaximumRetryAttempts':1}}]}}
r['Permission']={'Type':'AWS::Lambda::Permission','Properties':{'Action':'lambda:InvokeFunction','FunctionName':ref('Function'),'Principal':'events.amazonaws.com','SourceArn':get('Rule','Arn')}}
t['Outputs']={'FunctionName':{'Value':ref('Function')},'RuleName':{'Value':ref('Rule')}}
print(json.dumps(t,indent=2))
