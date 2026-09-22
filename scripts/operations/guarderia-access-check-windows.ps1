param([ValidateSet('Public','Vpn')][string]$Mode='Vpn')
$ErrorActionPreference='Stop'
$domains=@('portainer-guarderia.awecloudsolution.com','grafana-guarderia.awecloudsolution.com','zabbix-guarderia.awecloudsolution.com','status-guarderia.awecloudsolution.com','prometheus-guarderia.awecloudsolution.com','cadvisor-guarderia.awecloudsolution.com','node-guarderia.awecloudsolution.com')
$target=if($Mode -eq 'Public'){'204.157.108.99'}else{'10.250.0.1'}
$results=@()
foreach($domain in $domains){
 foreach($spoof in @($false,$true)){
  $curlArgs=@('--silent','--show-error','--noproxy','*','--connect-timeout','5','--max-time','15','--resolve',"${domain}:443:$target",'--output','NUL','--write-out','%{http_code} %{remote_ip}')
  if($spoof){$curlArgs+=@('-H','X-Forwarded-For: 10.250.0.10','-H','X-Real-IP: 10.250.0.10')}
  $curlArgs+="https://${domain}/?guarderia_access_check=windows_${Mode}"
  $response=& curl.exe @curlArgs
  $exitCode=$LASTEXITCODE
  $parts=($response -join '') -split ' '
  $ok=$exitCode -eq 0 -and $parts.Count -ge 2 -and $parts[1] -eq $target
  if($Mode -eq 'Public'){$ok=$ok -and $parts[0] -eq '403'}else{$ok=$ok -and $parts[0] -match '^(200|301|302|303|307|308|401)$'}
  $results+=[pscustomobject]@{Dominio=$domain;CabecalhoForjado=$spoof;HTTP=$parts[0];IP=$parts[1];OK=$ok}
 }
}
$results | Format-Table -AutoSize
$portResults=@()
if($Mode -eq 'Public'){
 foreach($port in @(3111,8181,9191,9100)){
  $client=New-Object Net.Sockets.TcpClient
  $connected=$false
  try {$task=$client.ConnectAsync($target,$port);$finished=$task.Wait(3000);$connected=$finished -and $client.Connected} catch {$connected=$false} finally {$client.Dispose()}
  $portResults+=[pscustomobject]@{Porta=$port;Conectou=$connected}
 }
 $portResults | Format-Table -AutoSize
 Write-Host 'Esperado: HTTP 403 nos sete dominios, inclusive com cabecalho forjado; Conectou=False nas quatro portas.'
 Write-Host 'Uma conexao TCP que falha nao identifica sozinha a causa. Reconecte a VPN e execute -Mode Vpn; confira login no navegador.'
}
if(@($results | Where-Object {-not $_.OK}).Count -gt 0 -or @($portResults | Where-Object {$_.Conectou}).Count -gt 0){exit 1}
