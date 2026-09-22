# Ensaio de persistência após reboot da VPS

Estado: reboot executado em 16/09/2026; novo boot e retorno dos serviços comprovados. Usuário confirmou retorno do SSH e informou acesso somente pela VPN. Testes externos TCP IPv4 e scripts VPN após o reboot aprovados conforme saídas do notebook; logins nos quatro consoles confirmados pelo usuário. Aceite funcional deste ensaio concluído. OPS-01 permanece parcial no escopo integral. O registro privado de agendamento foi salvo no diretório indicado por `/root/guarderia-evidencias/reboot-current.txt`.

## Situação anterior e preparação

VPS LXC; SSH, Docker, WireGuard, ambos os filtros e timer de backup ativos e habilitados. Doze serviços 1/1, três alvos Prometheus UP e TLS dos sete domínios válido pela VPN. Backup S3 backup-20260917T014109Z.gpg verificado por envio/download/hash; console Proxmox e nova sessão SSH pela VPN confirmados pelo usuário na etapa imediatamente anterior.

Falha preexistente: run-rpc_pipefs.mount. Ausência de NFS já observada; essa falha não foi corrigida neste ensaio e não deve ser atribuída automaticamente ao reboot. Mudança posterior do conjunto de unidades falhas exige avaliação própria.

Instalado guarderia-reboot-check.timer, habilitado para iniciar o verificador 45 segundos após o boot. Verificação antecipada com --dry-run passou: unidades, definições/volumes, filtros, rota VPN, TLS e coleta. O dry-run registrou boot_changed=false e não constitui resultado pós-reboot. O teste compara o identificador de boot com o anterior e grava post-reboot.json com horários, tentativas e erros; não altera regras nem reinicia aplicações para ocultar falhas. Pode aguardar a convergência dos serviços, limitado pelo timeout de dez minutos da unidade.

## Procedimento utilizado de execução e retorno

Agendar o reboot do sistema da VPS após salvar documentação e evidências. As sessões SSH e esta sessão de trabalho podem cair. Não reiniciar o host Proxmox nem outros contêineres. A autorização do usuário refere-se ao ensaio desta VPS.

No notebook, manter WireGuard conectado e aguardar a volta do SSH. Usar a identidade SSH indicada pelo usuário; preferência exata no registro privado notebook-access-preferences.json. Após reconexão, consultar o relatório no diretório indicado pelo marcador e o journal da unidade:

```bash
systemctl status guarderia-reboot-check.service --no-pager
journalctl -u guarderia-reboot-check.service -b --no-pager
```

Novo boot, serviços ativos, volume/labels preservados, três alvos UP, regras presentes e HTTPS local não bastam para confirmar a negação pela Internet. Repetir os scripts Windows dos painéis e infraestrutura nos modos Public e Vpn, e confirmar os quatro logins pelo navegador. O reboot é motivo concreto para repetir esses testes. Não repetir restauração de bancos sem necessidade.

## Recuperação se o acesso não retornar

Usar o console Proxmox desta VPS. Conferir boot, serviços e journal; não reinstalar a stack nem apagar volumes. Se necessário, iniciar apenas o componente que falhou após registrar a causa:

```bash
systemctl status ssh docker wg-quick@wg0 guarderia-panel-firewall guarderia-host-firewall --no-pager
journalctl -b -p err --no-pager
```

Se houver evidência de que os filtros bloquearam a recuperação, comandos preparados removem somente suas regras e reabrem os caminhos anteriores:

```bash
python3 /root/guarderia-ops/change_host_access.py rollback
python3 /root/guarderia-ops/change_panel_access.py rollback-firewall
```

A política Traefik tem retorno separado, conforme a validação dos painéis. Não executar rollback por padrão se a causa for VPN ou Docker não iniciado. Recuperação integral, chave externa, UDP e IPv6 externo permanecem ensaios separados.


## Retorno observado

Agendamento registrado em 17/09/2026 01:54:54 UTC, com atraso de 60 segundos. O boot_id consultado diretamente na VPS mudou em relação ao pré-teste. Não usar o boot_id do sandbox do agente para inferir outro reboot: ele difere do ambiente operacional; a conferência foi feita fora do sandbox.

O primeiro relatório automático, consultado nesta conversa, registrou sucesso em 01:56:59 UTC, com uptime de 50,72 s e tentativa 1. Isso representa o instante da verificação, não uma medição exata de indisponibilidade. Nova consulta direta em 01:58:52 UTC confirmou:

- Doze serviços 1/1 e três alvos Prometheus UP.
- SSH, Docker, WireGuard, os dois filtros e timer de backup ativos e habilitados.
- Labels e definições de montagens preservados nos serviços; isso não é uma comparação integral dos dados dos volumes.
- Regras dos filtros IPv4/IPv6 presentes, rota para o notebook preservada e sete domínios HTTPS respondendo pelo IP VPN.
- Mesma unidade run-rpc_pipefs.mount com falha, já registrada antes do reboot.

O usuário confirmou nova conexão SSH e informou que o acesso está disponível somente pela VPN. As sondagens dos dois scripts Windows nos modos Public/Vpn foram posteriormente recebidas e aprovadas, e os quatro logins confirmados pelo usuário. Os testes completos anteriores ao reboot não substituem essas verificações após a inicialização. Não houve restauração de bancos nem nova execução de backup neste pós-teste; o timer de backup voltou ativo.

Saída posterior do notebook recebida: ambos os scripts em modo Vpn passaram após o reboot. Sete domínios com e sem cabeçalhos forjados totalizaram 14 resultados OK=True para 10.250.0.1; TCP 5822 conectou e controle HTTPS retornou 200. Modo Public e logins no navegador foram posteriormente aprovados, conforme o fechamento abaixo. Não solicitar repetição do modo Vpn sem novo motivo.


Saída posterior do modo Public recebida: sete domínios retornaram HTTP 403 com e sem cabeçalhos forjados (14 respostas); nove portas TCP (3111, 8181, 9191, 9100, 111, 2377, 7946, 10051, 5822) não aceitaram conexão. Controle HTTPS público retornou 403. Somados ao modo Vpn já aprovado e ao pós-teste local, esses resultados comprovam persistência das restrições no escopo TCP IPv4 testado. Usuário confirmou os logins pós-reboot em Portainer, Grafana, Zabbix e Kuma, concluindo o aceite funcional deste ensaio. UDP, IPv6 externo, recuperação integral e demais critérios de OPS-01 continuam separados.
