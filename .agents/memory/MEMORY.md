# Memória do projeto

Atualizada em 17/09/2026. Fonte do estado vigente: [implementações](../../docs/00-project/IMPLEMENTATION_STATUS.md). Os números abaixo são resultados datados, não nova consulta. Não guardar credenciais ou resultados presumidos.

## Contexto e confirmações do usuário

WiFi Guarderia Vitória: hipótese de 10–20 barcos a 50–100 m; preparar NOC antes da PoC. RB750Gr3 disponível e RB951G-2HnD da central NOC atualizada para RouterOS/RouterBOOT 7.23.5; acesso/inventário de rede da RB951G ainda indisponível. Dual-WAN é proposta e segundo link não confirmado. RF, energia, capacidade, câmeras/alarme, custos e contrato continuam em validação.

Pasta local e repositório oficial Wittemberg/wifi-Guarderia preservados. nocagent e padrões Witteberg são referências, sem runtime AG Kit instalado. Usuário autoriza trabalho operacional por etapa; autorização não implica commit/push ou divulgação de segredos.

## Estado operacional consolidado

- Stack NOC em Swarm instalada e operacional; doze serviços 1/1 e três alvos Prometheus UP no pós-teste de 17/09/2026 03:09:54 UTC. Coleta usa DNS das tarefas; VIPs ainda exigem diagnóstico. Abrangência do Node Exporter não homologada.
- Grafana/Prometheus migrados para volumes nomeados guarderia_grafana_data e guarderia_prometheus_data; recriação validada e manifestos locais/Portainer reconciliados. Zero dashboards observados no inventário Grafana; não inventar painéis configurados.
- Backup AES-256 local/S3 diário às 03h15 de São Paulo, atraso aleatório de até cinco minutos; download/hash e restauração isolada S3 ensaiados. PG15/Zabbix com 207 tabelas públicas no ensaio. Último conjunto documentado: backup-20260917T030811Z.gpg. Chave externa copiada pelo usuário, ainda não usada em restauração.
- Retenção local 7 diários/4 semanais/3 mensais; S3 sete dias configurados pelo usuário e expiração observada em dois objetos. Exclusão efetiva/escopo integral não conferidos; versionamento observado desabilitado. Não alterar lifecycle por inferência.
- WireGuard hub 10.250.0.1/32 e notebook 10.250.0.10/32 ativos. SSH TCP 5822 e sete nomes HTTPS pela VPN, quatro logins e console Proxmox confirmados. RBs ainda não integradas.
- Sete routers Traefik restritos por origem; quatro portas de painéis e portas TCP/UDP de infraestrutura filtradas. Exceção gateway NAT Docker /32 somente no Prometheus para o datasource existente. Testes públicos TCP IPv4 de nove portas e sete nomes, inclusive cabeçalhos forjados, aprovados. Sessões SSH públicas anteriores foram preservadas durante a transição; novas conexões exigem VPN no caminho testado.
- Reboot controlado concluído: boot_id operacional mudou, pós-testes automáticos passaram, usuário repetiu testes externos e logins. Não solicitar repetição sem nova causa. O boot_id do sandbox difere do operacional; consultar fora do sandbox para validar reboot. Falha run-rpc_pipefs.mount já existia antes.
- Alertas SES/Telegram ativos: stack guarderia-backup-alerts, Lambda guarderia-backup-watchdog, EventBridge e heartbeat a cada cinco minutos. Ausência de sinal por 15 min e registro de verificação S3 com 26 h, além de falhas, geram alerta; recuperação por canal. Dez testes locais, testes integrados e recebimento nos dois canais confirmados; primeira execução automática saudável observada.

## Operação e recuperação

Evidências privadas por marcadores em guarderia-evidencias: access-current.txt (painéis), host-access-current.txt (infraestrutura), reboot-current.txt e alerts-current.txt. Retornos e limites nos respectivos registros de validação. Timers transitórios de reversão de acesso foram cancelados após confirmação; não presumir que ainda estão ativos.

Token Telegram em arquivo privado /root/.config/guarderia-alerts/telegram.json modo 600 e SSM SecureString /guarderia/alerts/telegram. Destinatários e identidade AWS apenas em configuração privada. Nunca pedir chave/token pelo chat. Política administrativa de implantação foi adicionada pelo usuário; não removê-la nem ampliá-la sem escopo próprio.

Preferência persistente: notebook Windows; sempre incluir -i com o caminho exato registrado em /root/guarderia-evidencias/notebook-access-preferences.json nos comandos SSH/SCP enviados ao usuário. Isso é caminho da identidade, não conteúdo da chave. Registro privado notebook-access-preferences.json. Para documentação sanitizada, não publicar comandos incompletos sem a identidade.

## Próximo passo e limites

Preparar recuperação integral em ambiente separado com chave externa e critérios de aceite. Reboot e alertas já concluídos não são próximas etapas pendentes. UDP externo, IPv6 externo, renovação ACME, revisão de privilégios, recuperação TLS/bancos integral, exclusão S3, diagnóstico de VIPs/Node Exporter e integração de equipamentos ainda pendentes. Não homologar F2/BAK-01/OPS-01/SEC-03/04 inteiros apenas pelos ensaios parciais.

Preservar arquivos e alterações existentes; segredos fora do Git. Não anunciar LAN de RB não conferida, antena 360°, SNR/CCQ não suportado, isolamento apenas por sub-rede, telemetria de campo ou percentuais sem evidência. Ver [requisitos](../../docs/00-project/REQUIREMENTS.md) e [riscos](../../docs/00-project/RISKS_AND_OPEN_ITEMS.md).
