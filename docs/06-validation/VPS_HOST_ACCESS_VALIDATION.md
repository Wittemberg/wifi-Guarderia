# Restrição das portas de infraestrutura da VPS

Estado: filtros mantidos em 16/09/2026 após confirmação pelo usuário de nova sessão SSH pela VPN e console Proxmox. Reversão automática cancelada enquanto os filtros ainda estavam ativos. Teste externo TCP IPv4 aprovado conforme saída enviada pelo usuário; acesso SSH e HTTPS pela VPN também aprovado. Aceite concluído neste escopo, sem homologar UDP, IPv6 externo ou reboot. A restrição anterior dos sete painéis já tem aceite próprio em [validação dos painéis](VPS_ACCESS_VALIDATION.md).

## Autorização e inventário

Usuário autorizou a revisão das portas restantes após concluir a etapa dos painéis. Inventário somente leitura registrou um nó Swarm Ready/Active/Leader, doze serviços 1/1, ausência de montagem NFS, rpcbind registrando somente portmapper e nenhuma dependência NFS observada. Zabbix tem apenas o host Zabbix server cadastrado, interface agent em loopback:10050; nenhum equipamento de campo cadastrado foi observado. Isso não homologa a coleta Zabbix nem exclui consumidores que não apareceram na amostra.

Foram observadas conexões externas em rpcbind e sessões SSH públicas. Seus endereços foram mantidos somente nas evidências privadas. Configurações e regras anteriores estão no diretório indicado por `/root/guarderia-evidencias/host-access-current.txt`, separado da evidência da etapa dos painéis. Backup S3 anterior verificado; scripts de aplicação e retorno preparados antes da mudança. Console e SSH VPN foram confirmados na etapa anterior, e nova sessão após a restrição é exigida para cancelar a reversão.

## Política aplicada

| Caminho | Restrição |
|---|---|
| Entrada pública eth0 TCP 111, 2377, 7946, 10051 | DROP antes do DNAT, tabela raw, somente destinos locais |
| Entrada pública eth0 UDP 111, 7946, 4789 | DROP nas mesmas condições |
| Entrada pública eth0 TCP 5822 | Filtro INPUT próprio; preserva ESTABLISHED/RELATED e bloqueia demais estados |
| Entrada wg0, tráfego interno e loopback | Não abrangidos pelos novos filtros |

Regras equivalentes IPv4/IPv6; não há IPv6 global observado, portanto não anunciar ensaio externo IPv6. RPC e listeners Swarm continuam em execução: a mudança limita entrada pela interface pública. SSH não foi reiniciado nem teve contas/chaves alteradas. Sessões SSH públicas anteriores permanecem permitidas até encerrarem; isso não significa liberação de novas sessões. WireGuard UDP 51820, HTTP/HTTPS e fluxos de saída foram preservados.

Filtro persistido em guarderia-host-firewall.service. A unidade foi incluída na rotina de backup, junto à unidade dos painéis. Na aplicação inicial, uma tarefa transitória reverteria a mudança após 15 minutos; ela foi cancelada após confirmação da nova sessão VPN. Não há reversão temporizada ativa dessa etapa. O reboot foi posteriormente executado e aprovado em ensaio separado.

## Verificações realizadas e pendências

Regras efetivas das duas famílias conferidas, reaplicação idempotente aprovada. Pós-teste de 17/09/2026 01:40:11 UTC registrou doze serviços 1/1, contêineres preservados, SSH/Docker/WireGuard ativos e consulta ao Prometheus a partir da rede do Grafana com três alvos UP. Isso não é prova externa do bloqueio.

Nova sessão SSH pela VPN e console confirmados pelo usuário; reversão cancelada com sucesso. Para repetir o ensaio já aprovado, executar o script guarderia-infrastructure-check-windows.ps1 no notebook: modo Public com VPN desligada espera ausência de conexão TCP em 111/2377/7946/10051/5822 e HTTP 403 no Portainer como controle de conectividade; modo Vpn espera TCP 5822 e HTTP 200 no Portainer. O teste não comprova UDP. Registrar o resultado do usuário separado das consultas locais. Reboot e retorno do Docker foram posteriormente validados no [ensaio próprio](VPS_REBOOT_VALIDATION.md). UDP externo, IPv6 externo e equipamentos futuros permanecem pendentes.

Para novos nós Swarm ou agentes/proxies Zabbix, planejar trânsito privado autorizado antes de cadastrá-los. A exceção de NAT local do Prometheus e a segregação entre contêineres permanecem assunto da etapa anterior.

## Aceite externo TCP e acesso pela VPN

O usuário enviou a saída do script Windows após a instrução de desconectar e reconectar a VPN. O horário exato do ensaio não consta na saída; os resultados abaixo são evidência fornecida pelo usuário, não sondagem independente do assistente.

| Verificação | Resultado |
|---|---|
| IP público, TCP 111, 2377, 7946, 10051 e 5822 | Cinco conexões recusadas ou sem conclusão no prazo; Conectou=False e OK=True |
| Controle HTTPS público no Portainer | HTTP 403; OK=True |
| VPN, TCP 5822 em 10.250.0.1 | Conectou=True; OK=True |
| Controle HTTPS pela VPN no Portainer | HTTP 200; OK=True |

Com o inventário e as regras efetivas registrados, esses resultados aprovam o escopo TCP IPv4 testado e a preservação do acesso VPN. A saída não distingue timeout de recusa, nem comprova negação UDP. O login SSH real e o console Proxmox já haviam sido confirmados pelo usuário após a mudança. Não repetir os testes sem alteração ou falha que justifique nova execução.

## Retorno

No terminal da VPS ou console Proxmox:

```bash
python3 /root/guarderia-ops/change_host_access.py rollback
```

Esse comando desabilita o serviço e remove apenas as cadeias novas. Reabre as portas de infraestrutura e novas conexões SSH públicas; não remove as restrições dos painéis. Para manter a mudança após confirmação documentada de nova sessão VPN, o operador usa `change_host_access.py confirm`, que verifica a evidência de confirmação e as regras, e cancela o timer. Não cancelar apenas porque os testes locais passaram.

Backup posterior aos filtros: backup-20260917T014109Z.gpg gerado, enviado e baixado do S3 com hash verificado. Pós-teste de 17/09/2026 01:42:50 UTC: systemd Result=success/ExecMainStatus=0, doze serviços 1/1 e três alvos UP. Esse ciclo não substitui a confirmação humana de acesso, recebida posteriormente; a reversão foi então cancelada.
