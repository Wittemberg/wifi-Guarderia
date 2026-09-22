# Validação das restrições dos painéis da VPS

Estado em 16/09/2026, 22h06 de São Paulo (17/09/2026, 01h06 UTC): restrições implantadas; validação externa IPv4 e HTTPS pós-mudança aprovados conforme saída enviada pelo usuário; logins pós-mudança nos quatro consoles confirmados pelo usuário. SEC-03/04 permanecem parciais. Escopo autorizado pelo usuário ao iniciar o plano e confirmar SSH, HTTPS e logins pela VPN.

## Pré-condições confirmadas

Usuário confirmou nova sessão SSH pela VPN e acesso de recuperação. O Windows apresentou HTTP 200/302/307, TLS válido e destino 10.250.0.1 para os sete nomes; depois confirmou os quatro consoles no navegador. O arquivo hosts estava somente leitura: o script remove temporariamente esse atributo, mantém backup e restaura o atributo original. Permissões e proteções do Windows não foram desativadas. Esses testes antecederam as restrições.

## Mudança aplicada

| Caminho | Política aplicada |
|---|---|
| Sete routers HTTPS: Portainer, Grafana, Zabbix, Kuma, Prometheus, cAdvisor e Node Exporter | IPAllowList por router, referência explícita ao provider Swarm; notebook e endereço VPN da VPS em /32, mais IPv4 público da própria VPS em /32 |
| Prometheus pelo caminho já usado pelo datasource Grafana | Exceção adicional somente neste router para o gateway local Docker em /32; não distingue os contêineres que compartilham esse NAT |
| TCP 3111, 8181, 9191 e 9100 pela interface pública | DROP em cadeia própria da tabela raw, antes do DNAT, IPv4 e IPv6, limitado a destinos locais |
| Persistência | Labels dos serviços, seis manifestos locais/Portainer reconciliados e serviço systemd guarderia-panel-firewall habilitado |

Não foi adicionada confiança em X-Forwarded-For nem liberada toda a rede overlay. O primeiro teste mostrou que o tráfego Grafana→domínio público chega como gateway Docker, não como IP público da VPS; a exceção ficou limitada ao Prometheus. Essa exceção mantém acesso por outros contêineres com o mesmo NAT e deve ser considerada na futura segregação interna. O teste inicial imediato do Grafana foi repetido após o intervalo de atualização do provider Swarm; o retorno foi aplicado enquanto a causa era verificada.

As publicações Swarm das quatro portas continuam existentes; a restrição está no filtro de entrada pública. SSH 5822, WireGuard 51820/UDP, 80/443, política padrão e tráfego de coleta não foram alterados. Porta 80 permanece disponível para o desafio HTTP ACME. Não houve teste de renovação de certificados nesta etapa.

## Resultados medidos

- Os sete routers aceitaram o caminho VPN da VPS e negaram uma origem overlay não autorizada com HTTP 403, inclusive com X-Forwarded-For e X-Real-IP forjados para o notebook.
- A mesma origem, usando o caminho público com NAT local, foi negada nos seis routers e aceita no Prometheus conforme a exceção prevista.
- Consulta real `up` ao domínio Prometheus a partir do namespace de rede do Grafana retornou sucesso e três alvos com valor 1.
- Doze serviços 1/1; os IDs dos contêineres permaneceram iguais ao inventário anterior. Nenhum redeploy integral foi executado.
- SSH, Docker, WireGuard e serviço de filtro ativos; filtro habilitado no systemd e regras IPv4/IPv6 conferidas no kernel.
- Origem WireGuard do notebook foi observada no access log antes da alteração. O teste de origem overlay é simulação interna, não sondagem da Internet.

Inventário anterior, candidatos, planos de labels, resultados por serviço e pós-teste estão no diretório privado indicado por `/root/guarderia-evidencias/access-current.txt`; não versionar esses arquivos. O backup criptografado passou a incluir também a unidade systemd do filtro. Novo ciclo concluído em 17/09/2026 01:08:02 UTC: backup-20260917T010621Z.gpg gerado, enviado ao S3 e baixado com hash verificado; systemd Result=success/ExecMainStatus=0, doze serviços 1/1 e três alvos UP após o ciclo.

## Resultado do notebook após a mudança

Evidência: saída PowerShell enviada pelo usuário nesta conversa, após a orientação de desconectar e reconectar a VPN. Horário exato da execução não consta na saída; não é uma medição independente do assistente.

| Caminho | Resultado enviado |
|---|---|
| IP público IPv4, sete domínios, sem cabeçalho forjado | 7/7 HTTP 403, destino 204.157.108.99, OK=True |
| IP público IPv4, sete domínios, cabeçalhos forjados | 7/7 HTTP 403, mesmo destino, OK=True |
| Portas públicas TCP 3111, 8181, 9191 e 9100 | 4/4 Conectou=False |
| VPN, sete domínios, com e sem cabeçalhos forjados | 14/14 OK=True, destino 10.250.0.1; HTTP 200/302/307 e verificação TLS mantida |

Esses resultados validam bloqueio externo IPv4 e acesso HTTPS pelo caminho VPN no escopo testado. A ausência de conexão TCP é compatível com o filtro observado no kernel; isoladamente não identifica a causa. A saída HTTP não comprova autenticação no navegador. Em resposta posterior, o usuário confirmou os logins em Portainer, Grafana, Zabbix e Kuma após reconectar a VPN. Aceite funcional desta etapa concluído; não equivale a ensaio de reboot nem revisão integral da segurança.

## Verificações pendentes

Para repetir o ensaio já aprovado, executar `guarderia-access-check-windows.ps1 -Mode Public` no notebook sem VPN: esperar 403 nos sete domínios, inclusive cabeçalhos forjados, e ausência de conexão nas quatro portas. Reconectar VPN, executar `-Mode Vpn` e confirmar novamente login nos quatro consoles. O script usa resolução explícita, mantém verificação TLS e não altera hosts. Falha TCP isolada não identifica a causa; correlacionar com acesso HTTPS público e regras efetivas.

Não há IPv6 global observado na VPS; regras IPv6 existem, mas ensaio pela Internet IPv6 permanece condicionado a conectividade real. Persistência após reboot foi posteriormente aprovada no [ensaio próprio](VPS_REBOOT_VALIDATION.md); Swarm, rpcbind, Zabbix 10051 e novas conexões SSH públicas receberam restrições e teste TCP IPv4 na [etapa de infraestrutura](VPS_HOST_ACCESS_VALIDATION.md). Renovação ACME, revisão de credenciais e recuperação integral permanecem pendentes; o conjunto não homologa toda a segurança da VPS.

## Retorno operacional

No terminal da VPS ou console de recuperação, usar os scripts privados preparados:

```bash
python3 /root/guarderia-ops/change_panel_access.py rollback-firewall
python3 /root/guarderia-ops/change_panel_access.py rollback
python3 /root/guarderia-ops/change_panel_access.py rollback-manifests
```

O primeiro remove somente o filtro próprio; o segundo restaura labels anteriores; o terceiro restaura os manifestos. Podem ser usados separadamente conforme o componente com problema. A reversão dos labels pode ser limitada passando o nome do serviço após `rollback`. Aguardar atualização do provider Traefik e repetir testes. O retorno reabre os caminhos anteriores; não executar como manutenção rotineira. Os scripts recusam sobrescrever labels/manifestos modificados por terceiros desde o plano. Para restaurar em outra VPS, os caminhos dos manifestos precisam ser reconciliados com o ambiente recuperado.

No Windows, `guarderia-vpn-windows.ps1 -Mode Disable`, elevado, remove apenas o bloco gerenciado e salva backup; fazer isso impede o acesso pelos nomes enquanto a política permanecer restrita.
