# Estado consolidado das implementações

Revisão documental de 17/09/2026. Consolida as evidências e confirmações recebidas; não representa nova sondagem operacional. Último pós-teste completo registrado: 17/09/2026 03:09:54 UTC, com doze serviços 1/1 e três alvos Prometheus UP. Documentação revisada; publicação rastreada pelo histórico Git. Esta revisão não executou nova implantação.

## Implantado e validado no escopo registrado

| Entrega | Estado e evidência |
|---|---|
| Stack NOC na VPS | Docker Swarm, Traefik, Portainer, Grafana, Prometheus/exporters, Zabbix/PostgreSQL e Kuma operacionais. [Instalação histórica](../06-validation/VPS_PHASE_COMPLETION.md) |
| Coleta interna | Três alvos Prometheus UP; coleta RF/equipamentos ainda não homologada. [Coleta](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md) |
| Persistência Grafana/Prometheus | Volumes nomeados migrados, recriação validada, manifestos locais/Portainer reconciliados. [Persistência e backup](../06-validation/BACKUP_AUTOMATION.md) |
| Backup e restauração isolada | Backup criptografado diário, envio/download/hash S3 e restauração isolada de aplicações/PG14/PG15 ensaiados. Último conjunto documentado: backup-20260917T030811Z.gpg. [Resultados](../06-validation/BACKUP_AUTOMATION.md) |
| Retenção e chave | Local 7 diários/4 semanais/3 mensais; S3 sete dias informado pelo usuário e expiração observada em dois objetos. Chave copiada para fora da VPS pelo usuário; conteúdo externo não testado. [Limites](../06-validation/BACKUP_AUTOMATION.md) |
| VPN do notebook | WireGuard, rota específica, SSH e sete domínios HTTPS validados; quatro logins confirmados pelo usuário. [Notebook](../06-validation/NOTEBOOK_VPN_VALIDATION.md), [painéis](../06-validation/VPS_ACCESS_VALIDATION.md) |
| Restrição pública | Sete domínios HTTP 403 pelo IP público, inclusive cabeçalhos forjados; nove portas TCP sem conexão externa. SSH/HTTPS pela VPN preservados. [Painéis](../06-validation/VPS_ACCESS_VALIDATION.md), [infraestrutura](../06-validation/VPS_HOST_ACCESS_VALIDATION.md) |
| Reboot controlado | Novo boot observado, serviços/coleta/filtros/rota/TLS preservados; testes externos e logins repetidos e aprovados. Aceite funcional concluído. [Ensaio](../06-validation/VPS_REBOOT_VALIDATION.md) |
| Alertas externos | Lambda/EventBridge na AWS e heartbeat local ativos a cada cinco minutos. Falha, ausência de sinal por 15 min e backup sem verificação por 26 h; recuperação por SES/Telegram. Testes e recebimento nos dois canais confirmados. [Operação](../06-validation/BACKUP_ALERTS.md) |

## Pendências reais

- Recuperação integral da VPS em ambiente separado, usando a chave externa; RPO/RTO são metas, não resultados homologados. Restauração TLS real e aplicação Zabbix conectada ao banco restaurado ainda não ensaiadas.
- Exclusão efetiva dos objetos S3 e revisão completa do lifecycle; versionamento observado como desabilitado. A retenção longa local não sobrevive à perda da VPS.
- UDP externo e IPv6 externo não homologados; não há IPv6 global observado. Revogação/privilégios, renovação ACME, segregação interna e segurança de campo continuam em validação.
- Diagnóstico dos VIPs Swarm, abrangência das métricas do Node Exporter e falha preexistente run-rpc_pipefs.mount. Não atribuir essa falha ao reboot.
- Monitor dos alertas depende da AWS; não há segundo monitor independente da AWS. Custos e política administrativa de implantação merecem revisão própria.
- Integração das RBs, templates/coleta de equipamentos, RF, energia, isolamento de barcos e PoC de campo ainda pendentes. RB750r2 r3 em RouterOS/RouterBOOT 7.23.7 inventariada em 21/09/2026: gateway básico ativo, WAN2 reservada, sem WireGuard; isso não equivale à integração.

F2, BAK-01, OPS-01 e SEC-03/04 integrais permanecem parciais por critérios fora dos ensaios concluídos. Esse estado não deve voltar a marcar reboot, alertas ou restrições TCP já testadas como pendentes. A [homologação](../06-validation/HOMOLOGATION.md) mantém a rastreabilidade dos critérios.

## Próximo passo

Preparar a recuperação integral em ambiente separado: destino, sequência de restauração, chave externa e critérios de aceite. Não reiniciar novamente a produção nem repetir testes aprovados sem alteração/falha que justifique. Com o inventário da RB750r2 recebido, preparar integração incremental e recuperação local antes do core. [Roadmap](ROADMAP.md) e [riscos](RISKS_AND_OPEN_ITEMS.md).

## Leitura dos documentos

Este documento é a entrada para o estado atual. Relatórios históricos de instalação, cadastro do notebook e auditoria inicial preservam observações daquela etapa e apontam para esta consolidação. Procedimentos e propostas RouterOS/campo continuam propostas onde não há evidência de execução. Segredos, endereços pessoais de contato e saídas privadas não são fontes versionadas.

## Atualização da central NOC — 21/09/2026

[Inventário e configuração atual](../01-architecture/NOC_ROUTER_INVENTORY.md) analisados em treze anexos. Três amostras ICMP 5/5 recebidas; DNS de cliente, VPN da RB e failover permanecem não homologados. Resultados anteriores da VPS preservados; não foi executado novo teste operacional nesta revisão.
