# Registro de homologação

Data da baseline: 12/09/2026. Estados independentes: especificação, implementação, teste e aceite humano. Nenhuma caixa é marcada por presunção.

| Teste | Cobertura | Estado real nesta entrega | Evidência/resultado |
|---|---|---|---|
| DOC-01 | Estrutura, links, Git e publicação | Revisão local concluída | [Verificações](DOCUMENTATION_REVIEW.md); commit/publicação pelo histórico Git |
| DOC-02 | Referência nocagent e padrões | Análise documental realizada | [Revisão](../08-reference/NOCAGENT_REVIEW.md) |
| HW-01 | Inventário e compatibilidade elétrica/firmware | Parcial: inventário RB951G recebido do usuário; atualização concluída | [RB951G central NOC](../01-architecture/NOC_ROUTER_INVENTORY.md); demais equipamentos e testes pendentes |
| VPS-01 | Inventário e caminho de instalação | Parcial: inventário e instalação inicial concluídos em 16/09/2026 | [Conclusão](VPS_PHASE_COMPLETION.md); console, suporte VPN e versão/hash Orion pendentes |
| STACK-01 | Stack, versões, rede e persistência | Parcial: instalação e coleta interna concluídas | 12 serviços 1/1 e três alvos UP; autenticação, persistência, exposição e manifesto de manutenção pendentes; [evidências](VPS_PHASE_COMPLETION.md) |
| VPN-01 | Hub e CGNAT | Não executado | Aguardar laboratório |
| VPN-02 | Rotas, retorno e coleta container | Não executado | Aguardar laboratório |
| VPN-03 | Falhas/recuperação e independência da central NOC | Não executado | Aguardar laboratório |
| MON-01 | Coleta real e comparação direta | Não executado | Aguardar equipamentos |
| MON-02 | Sem dados, credencial e campos não suportados | Não executado | Aguardar stack |
| MON-03 | Diagnóstico por camada | Não executado | Aguardar stack/rede |
| RF-01 | Rádio dual-band e trânsito em bancada | Não executado | Aguardar rádios |
| RF-02 | 50/100 m por orientação | Não executado | Aguardar campo |
| RF-03 | Rotação completa | Não executado | Aguardar campo |
| RF-04 | Carga e estabilidade | Não executado | Aguardar campo |
| RF-05 | 24 h e 7 dias | Não executado | Aguardar campo |
| LAN-01 | DHCP/DNS/serviços simultâneos | Não executado | Aguardar laboratório |
| SEC-01 | Bloqueio entre barcos | Não executado | Dois clientes ou bancada equivalente |
| SEC-02 | Spoof, VLAN, L2 e IPv6 | Não executado | Aguardar laboratório |
| SEC-03 | Exposição externa e firewall Docker | Não executado | Aguardar ambiente |
| SEC-04 | Credenciais, privilégios e TLS | Não executado | Aguardar ambiente |
| ENE-01 | Consumo, proteção e autonomia | Não executado | Aguardar kit e inspeção |
| BAK-01 | Restauração e RPO/RTO | Não executado | Aguardar implantação |
| OPS-01 | Reboot/redeploy e rollback | Não executado | Aguardar ambiente |
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

## Verificação complementar — 16/09/2026

Coleta interna Prometheus: três alvos UP e sem erro na API, com últimas coletas em 03:36:31–34 UTC, após validação promtool e SIGHUP. Ver [procedimento e limites](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md). Resultado restrito à coleta dos exporters e do próprio Prometheus; não aprova MON-01/02/03, STACK-01 ou aceite humano.
