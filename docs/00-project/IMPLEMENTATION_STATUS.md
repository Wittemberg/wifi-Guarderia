# Estado consolidado das implementações

Revisão documental atualizada em 22/09/2026. Consolida as evidências e confirmações recebidas; medições têm data e escopo próprios. Último pós-teste completo da stack registrado: 17/09/2026 03:09:54 UTC, com doze serviços 1/1 e três alvos Prometheus UP. Em 22/09/2026, a VPN de borda da central NOC e a rota reversa até a LAN foram implantadas e testadas.

## Implantado e validado no escopo registrado

| Entrega | Estado e evidência |
|---|---|
| Stack NOC na VPS | Docker Swarm, Traefik, Portainer, Grafana, Prometheus/exporters, Zabbix/PostgreSQL e Kuma operacionais. [Instalação histórica](../06-validation/VPS_PHASE_COMPLETION.md) |
| Coleta interna | Três alvos Prometheus UP; coleta RF/equipamentos ainda não homologada. [Coleta](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md) |
| Persistência Grafana/Prometheus | Volumes nomeados migrados, recriação validada, manifestos locais/Portainer reconciliados. [Persistência e backup](../06-validation/BACKUP_AUTOMATION.md) |
| Backup e restauração isolada | Backup criptografado diário, envio/download/hash S3 e restauração isolada de aplicações/PG14/PG15 ensaiados. Último conjunto documentado: backup-20260917T030811Z.gpg. [Resultados](../06-validation/BACKUP_AUTOMATION.md) |
| Retenção e chave | Local 7 diários/4 semanais/3 mensais; S3 sete dias informado pelo usuário e expiração observada em dois objetos. Chave copiada para fora da VPS pelo usuário; conteúdo externo não testado. [Limites](../06-validation/BACKUP_AUTOMATION.md) |
| VPN do notebook | WireGuard, rota específica, SSH e sete domínios HTTPS validados; quatro logins confirmados pelo usuário. [Notebook](../06-validation/NOTEBOOK_VPN_VALIDATION.md), [painéis](../06-validation/VPS_ACCESS_VALIDATION.md) |
| VPN de borda NOC | RB750r2 `10.250.0.2` conectada ao hub; LAN `192.168.15.0/24` alcança VPS e Portainer. Rota reversa VPS → LAN persistida; NVR `192.168.15.110` respondeu 3/3 após reinicialização. [Implementação](../02-implementation/MIKROTIK_WIREGUARD_EDGE.md), [validação](../06-validation/NOC_EDGE_VPN_VALIDATION.md) |
| Restrição pública | Sete domínios HTTP 403 pelo IP público, inclusive cabeçalhos forjados; nove portas TCP sem conexão externa. SSH/HTTPS pela VPN preservados. [Painéis](../06-validation/VPS_ACCESS_VALIDATION.md), [infraestrutura](../06-validation/VPS_HOST_ACCESS_VALIDATION.md) |
| Reboot controlado | Novo boot observado, serviços/coleta/filtros/rota/TLS preservados; testes externos e logins repetidos e aprovados. Aceite funcional concluído. [Ensaio](../06-validation/VPS_REBOOT_VALIDATION.md) |
| Alertas externos | Lambda/EventBridge na AWS e heartbeat local ativos a cada cinco minutos. Falha, ausência de sinal por 15 min e backup sem verificação por 26 h; recuperação por SES/Telegram. Testes e recebimento nos dois canais confirmados. [Operação](../06-validation/BACKUP_ALERTS.md) |

## Pendências reais

- Recuperação integral da VPS em ambiente separado, usando a chave externa; RPO/RTO são metas, não resultados homologados. Restauração TLS real e aplicação Zabbix conectada ao banco restaurado ainda não ensaiadas.
- Exclusão efetiva dos objetos S3 e revisão completa do lifecycle; versionamento observado como desabilitado. A retenção longa local não sobrevive à perda da VPS.
- UDP externo e IPv6 externo não homologados; não há IPv6 global observado. Revogação/privilégios, renovação ACME, segregação interna e segurança de campo continuam em validação.
- Diagnóstico dos VIPs Swarm, abrangência das métricas do Node Exporter e falha preexistente run-rpc_pipefs.mount. Não atribuir essa falha ao reboot.
- Monitor dos alertas depende da AWS; não há segundo monitor independente da AWS. Custos e política administrativa de implantação merecem revisão própria.
- Integração da RB750r2 da central NOC foi concluída no escopo de VPN de borda. Integração da RB750Gr3/core, templates/coleta de equipamentos, RF, energia, isolamento de barcos e PoC de campo continuam pendentes. WAN2 e dual-WAN permanecem propostas não homologadas.

F2, BAK-01, OPS-01 e SEC-03/04 integrais permanecem parciais por critérios fora dos ensaios concluídos. Esse estado não deve voltar a marcar reboot, alertas ou restrições TCP já testadas como pendentes. A [homologação](../06-validation/HOMOLOGATION.md) mantém a rastreabilidade dos critérios.

## Próximo passo

Preparar a integração da RB750Gr3/core e a recuperação integral da VPS em ambiente separado. Mudanças em `wg0` devem preservar console fora de banda: reiniciar a interface pelo próprio túnel interrompe a sessão administrativa. [Roadmap](ROADMAP.md), [riscos](RISKS_AND_OPEN_ITEMS.md) e [validação da VPN NOC](../06-validation/NOC_EDGE_VPN_VALIDATION.md).

## Leitura dos documentos

Este documento é a entrada para o estado atual. Relatórios históricos de instalação, cadastro do notebook e auditoria inicial preservam observações daquela etapa e apontam para esta consolidação. Procedimentos e propostas RouterOS/campo continuam propostas onde não há evidência de execução. Segredos, endereços pessoais de contato e saídas privadas não são fontes versionadas.

## Atualização da central NOC — 22/09/2026

[Inventário e configuração atual](../01-architecture/NOC_ROUTER_INVENTORY.md) analisados em treze anexos. Navegação de cliente pelo gateway foi confirmada em 21/09/2026. Em 22/09/2026, WireGuard na RB750r2, LAN → VPS, Portainer e rota VPS → LAN foram validados; o NVR `192.168.15.110` respondeu 3/3 por ICMP. Failover WAN, outros equipamentos/protocolos e carga permanecem não homologados.
