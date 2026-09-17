param([ValidateSet('Public','Vpn')][string]$Mode='Public')
$ErrorActionPreference='Stop'
$target=if($Mode -eq 'Public'){'204.157.108.99'}else{'10.250.0.1'}
$ports=if($Mode -eq 'Public'){@(111,2377,7946,10051,5822)}else{@(5822)}
$results=@()
foreach($port in $ports){
 $client=New-Object Net.Sockets.TcpClient
 $connected=$false
 try {$task=$client.ConnectAsync($target,$port);$finished=$task.Wait(3000);$connected=$finished -and $client.Connected} catch {$connected=$false} finally {$client.Dispose()}
 $expected=$Mode -eq 'Vpn'
 $results+=[pscustomobject]@{IP=$target;Porta=$port;Conectou=$connected;OK=($connected -eq $expected)}
}
$results | Format-Table -AutoSize
$domain='portainer-guarderia.awecloudsolution.com'
$curlArgs=@('--silent','--show-error','--noproxy','*','--connect-timeout','5','--max-time','15','--resolve',"${domain}:443:$target",'--output','NUL','--write-out','%{http_code}',"https://${domain}/?guarderia_access_check=infrastructure_${Mode}")
$code=& curl.exe @curlArgs
$curlExit=$LASTEXITCODE
$httpOK=$curlExit -eq 0 -and (($Mode -eq 'Public' -and $code -eq '403') -or ($Mode -eq 'Vpn' -and $code -eq '200'))
Write-Host "Controle HTTPS: $code; OK=$httpOK"
Write-Host 'Este teste cobre TCP. UDP e IPv6 externo nao sao homologados por esta saida.'
if(-not $httpOK -or @($results | Where-Object {-not $_.OK}).Count -gt 0){exit 1}
