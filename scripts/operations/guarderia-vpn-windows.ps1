param([ValidateSet('Enable','Disable','Test')][string]$Mode='Test')
$ErrorActionPreference='Stop'
$domains=@('portainer-guarderia.awecloudsolution.com','grafana-guarderia.awecloudsolution.com','zabbix-guarderia.awecloudsolution.com','status-guarderia.awecloudsolution.com','prometheus-guarderia.awecloudsolution.com','cadvisor-guarderia.awecloudsolution.com','node-guarderia.awecloudsolution.com')
$hostsFile=Join-Path $env:WINDIR 'System32\drivers\etc\hosts'
$begin='# BEGIN GUARDERIA VPN'
$end='# END GUARDERIA VPN'
if($Mode -ne 'Test') {
 $admin=([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
 if(-not $admin){throw 'Abra o PowerShell como Administrador para alterar hosts.'}
 $original=[IO.File]::ReadAllText($hostsFile)
 $begins=[regex]::Matches($original,'(?m)^# BEGIN GUARDERIA VPN\r?$').Count
 $ends=[regex]::Matches($original,'(?m)^# END GUARDERIA VPN\r?$').Count
 if($begins -ne $ends -or $begins -gt 1){throw 'Bloco Guarderia inconsistente; conferir hosts antes de alterar.'}
 $clean=[regex]::Replace($original,'(?ms)^# BEGIN GUARDERIA VPN\r?\n.*?^# END GUARDERIA VPN(?:\r?\n)?','')
 if($Mode -eq 'Enable') {
  foreach($line in ($clean -split '\r?\n')) {
   $active=($line -split '#',2)[0].Trim()
   if(-not $active){continue}
   $tokens=$active -split '\s+'
   foreach($domain in $domains){if($tokens -contains $domain){throw "Ja existe entrada para $domain fora do bloco. Conferir manualmente."}}
  }
  $lines=@($begin)+@($domains | ForEach-Object {"10.250.0.1`t$_"})+@($end)
  $updated=$clean.TrimEnd("`r","`n")+"`r`n"+($lines -join "`r`n")+"`r`n"
 } else {$updated=$clean}
 $backup=$hostsFile+'.guarderia-'+(Get-Date -Format 'yyyyMMdd-HHmmss-fff')+'.bak'
 [IO.File]::Copy($hostsFile,$backup,$false)
 $attributes=[IO.File]::GetAttributes($hostsFile)
 $wasReadOnly=($attributes -band [IO.FileAttributes]::ReadOnly) -ne 0
 try {
  if($wasReadOnly){
   Write-Host 'Removendo temporariamente o atributo somente leitura do hosts.'
   [IO.File]::SetAttributes($hostsFile,($attributes -band (-bnot [IO.FileAttributes]::ReadOnly)))
  }
  [IO.File]::WriteAllText($hostsFile,$updated,(New-Object Text.UTF8Encoding($false)))
 } catch {
  Write-Host "Backup preservado: $backup"
  Write-Host "Atributos originais: $attributes"
  Write-Host 'Permissoes atuais do arquivo:'
  & icacls.exe $hostsFile
  Write-Host 'Se o acesso continuar negado, envie esta saida. Nao altere permissoes nem desative protecoes.'
  Write-Host 'Para testar HTTPS pela VPN sem editar hosts, execute este script com -Mode Test.'
  throw
 } finally {
  if($wasReadOnly){[IO.File]::SetAttributes($hostsFile,$attributes)}
 }
 & ipconfig.exe /flushdns | Out-Null
 Write-Host "Hosts atualizado. Backup: $backup"
}
$results=@()
foreach($domain in $domains) {
 $curlArgs=@('--silent','--show-error','--noproxy','*','--connect-timeout','5','--max-time','15','--output','NUL','--write-out','%{http_code} %{remote_ip}')
 if($Mode -eq 'Test'){$curlArgs+=@('--resolve',"${domain}:443:10.250.0.1")}
 $curlArgs+="https://${domain}/?guarderia_access_check=notebook_windows"
 $response=& curl.exe @curlArgs
 $code=$LASTEXITCODE
 $parts=($response -join '') -split ' '
 $ok=($code -eq 0 -and $parts[0] -match '^(200|301|302|303|307|308|401)$' -and $parts[1] -eq '10.250.0.1')
 $results+=[pscustomobject]@{Dominio=$domain;HTTP=$parts[0];IP=$parts[1];VPN_TLS_OK=$ok}
}
$results | Format-Table -AutoSize
Write-Host 'O teste HTTP/TLS nao substitui login no navegador. Abra os quatro consoles e confira seu acesso.'
if($Mode -eq 'Disable'){Write-Host 'Bloco removido. Com a gerencia restrita, o acesso publico aos consoles deve falhar.'}
if($Mode -ne 'Disable' -and @($results | Where-Object {-not $_.VPN_TLS_OK}).Count -gt 0){exit 1}
