# Registro de homologação

Baseline de critérios: 12/09/2026; estado consolidado em 17/09/2026. Estados independentes: especificação, implementação, teste e aceite humano. Nenhuma caixa é marcada por presunção.

| Teste | Cobertura | Estado real nesta entrega | Evidência/resultado |
|---|---|---|---|
| DOC-01 | Estrutura, links, Git e publicação | Revisão local concluída | [Verificações](DOCUMENTATION_REVIEW.md); commit/publicação pelo histórico Git |
| DOC-02 | Referência nocagent e padrões | Análise documental realizada | [Revisão](../08-reference/NOCAGENT_REVIEW.md) |
| HW-01 | Inventário e compatibilidade elétrica/firmware | Parcial: inventário RB951G recebido do usuário; atualização concluída | [RB951G central NOC](../01-architecture/NOC_ROUTER_INVENTORY.md); demais equipamentos e testes pendentes |
| VPS-01 | Inventário e caminho de instalação | Parcial: inventário e instalação inicial concluídos em 16/09/2026 | [Conclusão](VPS_PHASE_COMPLETION.md); console confirmado e suporte WireGuard validado; recursos garantidos e versão/hash Orion pendentes |
| STACK-01 | Stack, versões, rede e persistência | Parcial: instalação e coleta interna concluídas | 12 serviços 1/1 e três alvos UP; volumes Grafana/Prometheus e manifestos reconciliados; logins e restrições TCP IPv4 confirmados após reboot; compatibilidade integral e recuperação completa pendentes. [Estado](../00-project/IMPLEMENTATION_STATUS.md) |
| VPN-01 | Hub e CGNAT | Parcial: hub/notebook conectados | Handshake, ping e SSH; RBs e ensaios CGNAT pendentes; [registro](NOTEBOOK_VPN_VALIDATION.md) |
| VPN-02 | Rotas, retorno e coleta container | Parcial: rota e retorno notebook ↔ VPS | LANs, trânsito entre peers e coleta container pendentes; [registro](NOTEBOOK_VPN_VALIDATION.md) |
| VPN-03 | Falhas/recuperação e independência da central NOC | Não executado | Aguardar laboratório |
| MON-01 | Coleta real e comparação direta | Não executado | Aguardar equipamentos |
| MON-02 | Sem dados, credencial e campos não suportados | Não executado | Preparar ensaios de perda de coleta e credenciais |
| MON-03 | Diagnóstico por camada | Não executado | Preparar ensaios por camada e integrar equipamentos |
| RF-01 | Rádio dual-band e trânsito em bancada | Não executado | Aguardar rádios |
| RF-02 | 50/100 m por orientação | Não executado | Aguardar campo |
| RF-03 | Rotação completa | Não executado | Aguardar campo |
| RF-04 | Carga e estabilidade | Não executado | Aguardar campo |
| RF-05 | 24 h e 7 dias | Não executado | Aguardar campo |
| LAN-01 | DHCP/DNS/serviços simultâneos | Não executado | Aguardar laboratório |
| SEC-01 | Bloqueio entre barcos | Não executado | Dois clientes ou bancada equivalente |
| SEC-02 | Spoof, VLAN, L2 e IPv6 | Não executado | Aguardar laboratório |
| SEC-03 | Exposição externa e firewall Docker | Parcial | Sete routers restritos e quatro portas filtradas; simulação interna e teste externo IPv4 negaram acesso, inclusive cabeçalhos forjados; nove portas TCP sem conexão pública e sete nomes 403, repetidos após reboot. UDP/IPv6 externo e revisão integral pendentes. [Evidências](VPS_REBOOT_VALIDATION.md) |
| SEC-04 | Credenciais, privilégios e TLS | Parcial | TLS dos sete domínios pela VPN validado antes e depois da mudança; usuário confirmou os quatro logins pós-mudança. Revisão de privilégios/revogação e demais critérios pendentes |
| ENE-01 | Consumo, proteção e autonomia | Não executado | Aguardar kit e inspeção |
| BAK-01 | Restauração e RPO/RTO | Parcial: backup criptografado, envio diário e restauração isolada a partir do S3 validados | [Automação](BACKUP_AUTOMATION.md); Expiração S3 de sete dias configurada pelo usuário e prevista em dois objetos; exclusão efetiva, revisão do lifecycle/versionamento, chave externa, TLS restaurado e recuperação integral pendentes |
| OPS-01 | Reboot/redeploy e rollback | Parcial: recriação e reboot controlado validados | [Reboot](VPS_REBOOT_VALIDATION.md): serviços, coleta, montagens, filtros, testes externos e logins aprovados. Recuperação/rollback integral e equipamentos de campo pendentes |
| OPS-02 | Checklist físico e manutenção | Não executado | Aguardar visita |
| SECUR-01 | Alarme e responsabilidades | Não executado | Modelos/serviço pendentes |
| VIDEO-01 | Gravação e consulta remota | Não executado | Modelos pendentes |
| CAP-01 | Capacidade para crescimento | Não executado | Requer medições |
| COM-01 | Viabilidade econômica | Não executado | Requer cotações e custos |
| INT-01 | Integração futura NOC-Agent | Fora da implantação inicial | Somente contrato planejado |
| DOC-03 | Anexos RouterOS: integridade e análise estática | Revisão documental realizada | [Achados](../02-implementation/ROUTEROS_BASELINE_REVIEW.md); não valida import |
| ROS-01 | Adaptação e import dry-run | Não executado | [Plano dual-WAN](../02-implementation/NOC_DUAL_WAN.md) |
| WAN-01 | Preferência WAN1 e sondas por caminho | Não executado | [Plano dual-WAN](../02-implementation/NOC_DUAL_WAN.md) |
| WAN-02 | Queda física e retorno WAN1 | Não executado | [Plano dual-WAN](../02-implementation/NOC_DUAL_WAN.md) |
| WAN-03 | Falha parcial/total de sondas com Ethernet ativa | Não executado | [Plano dual-WAN](../02-implementation/NOC_DUAL_WAN.md) |
| WAN-04 | Duas WANs indisponíveis, defaults inativas | Não executado | [Plano dual-WAN](../02-implementation/NOC_DUAL_WAN.md) |
| WAN-05 | Recuperação isolada de cada WAN | Não executado | [Plano dual-WAN](../02-implementation/NOC_DUAL_WAN.md) |
| WAN-06 | WireGuard e sessões após troca WAN | Não executado | [Plano dual-WAN](../02-implementation/NOC_DUAL_WAN.md) |
| WAN-07 | Reboot e intermitência | Não executado | [Plano dual-WAN](../02-implementation/NOC_DUAL_WAN.md) |

## Testes negativos obrigatórios

SEC-01: barco A não alcança LAN, WAN/gerência ou serviços de B; administração autorizada alcança ambos. SEC-02: tentativa de usar endereço de B, quadros com tags indevidas, caminho direto entre estações e IPv6 não abre acesso. SEC-03: sondagem externa autorizada verifica ausência de banco, SNMP, API/WinBox e Portainer públicos, incluindo após restart Docker. SEC-04: coletor não altera configuração; credencial revogada e certificado inválido são recusados.

## Registro de cada execução

Usar [modelo de evidência](EVIDENCE_TEMPLATES.md). Preencher responsável, data, versões, requisito, resultado e localização privada. Aceite humano deve ter autor e data; teste automatizado não o substitui. Restrições devem apontar teste e impacto concretos.

## Evidências atuais por escopo

- [Backup e persistência](BACKUP_AUTOMATION.md): migração/recriação, backup criptografado/S3 e restauração isolada aprovados; recuperação integral e chave externa ainda não ensaiadas.
- [Painéis](VPS_ACCESS_VALIDATION.md) e [infraestrutura](VPS_HOST_ACCESS_VALIDATION.md): restrições aplicadas, teste externo TCP IPv4 e acesso VPN aprovados.
- [Reboot](VPS_REBOOT_VALIDATION.md): novo boot observado, pós-testes automáticos e testes externos repetidos, quatro logins confirmados. Aceite funcional desse ensaio concluído.
- [Alertas de backup](BACKUP_ALERTS.md): monitor externo ativo, dez testes locais e ensaios sintéticos integrados aprovados; e-mail/Telegram e recuperação recebidos pelo usuário. Isso não substitui MON-01/02/03 de equipamentos de campo.

Doze serviços 1/1 e três alvos UP no último pós-teste completo registrado, 17/09/2026 03:09:54 UTC; não é consulta contínua. Critérios integrais continuam parciais pelos limites dos ensaios, não por etapas já concluídas. RBs, RF, energia e isolamento de campo ainda dependem de acesso/bancada. [Estado consolidado](../00-project/IMPLEMENTATION_STATUS.md).
