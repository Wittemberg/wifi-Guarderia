# Plano de execução

Nenhum prazo de implantação foi confirmado. As fases abaixo são sequenciais por dependência, com critérios de saída observáveis.

| Fase | Entrega | Dependência | Critério de saída | Estado em 17/09/2026 |
|---|---|---|---|---|
| F0 | Especificação e Git | Contexto e referência | DOC-01/02 revisados; commit publicado | Documentação preparada |
| F1 | Inventário VPS, RBs e levantamento local | F0 | HW-01/VPS-01 e pendências impeditivas resolvidas | Parcial: inventário VPS realizado e RB951G atualizada; console Proxmox confirmado; acesso/inventário de rede da RB951G, core e levantamento local pendentes |
| F2 | WireGuard e stack NOC | F1 | VPN-01/02; STACK-01; backup restaurável | Stack/coleta interna e VPN notebook ↔ VPS validadas no escopo registrado; volumes e restauração isolada S3 validados; reboot, restrições TCP IPv4 e alertas de backup validados; integração das RBs e homologação integral pendentes |
| F3 | Templates e alertas em bancada | F2 | MON-01/02/03; dados persistem após reboot | Pendente |
| F4 | Rádio e isolamento em bancada | F3 | RF-01; LAN-01; SEC-01/02/03 | Pendente |
| F5 | PoC embarcada 50/100 m | F4 e alimentação validada | RF-02/03/04; ENE-01 | Pendente |
| F6 | Kit de segurança e piloto prolongado | F5 | SECUR-01; VIDEO-01; OPS-02 | Pendente |
| F7 | Capacidade e modelo comercial | F6 | CAP-01; COM-01; riscos aceitos | Pendente |
| F8 | Lotes graduais até 20 barcos | F7 | Repetir onboarding e aceite por lote | Pendente |

## Próxima execução concreta

Preparar recuperação integral da VPS em ambiente separado, usando a chave externa: definir destino, sequência e critérios antes de restaurar. Backup isolado não equivale à reconstrução completa. Não repetir reboot ou testes de acesso já aprovados sem nova mudança/falha. [Estado consolidado](IMPLEMENTATION_STATUS.md).

A integração da RB951G depende de acesso e inventário de interfaces/LAN/rotas/WANs, backup e recuperação local. RB750Gr3 depois. Não anunciar redes não conferidas. [WireGuard](../02-implementation/WIREGUARD.md).

## Entregas operacionais concluídas no escopo testado

Stack/coleta interna, volumes Grafana/Prometheus, backup diário e restauração isolada S3, notebook VPN, restrições públicas TCP IPv4, reboot controlado e alertas SES/Telegram têm evidências próprias. A automação de alertas de backup não homologa templates e alertas de equipamentos da fase F3. [Validações](../06-validation/HOMOLOGATION.md).

## Critério para expansão

Comprar e instalar por lotes pequenos após resultado do piloto. A aprovação de um barco não homologa capacidade de vinte estações. Testar concorrência, ocupação do rádio, câmeras e falha de WAN.

## Governança

Separar especificado, implementado, medido e aceite humano. Não atribuir percentuais sem conjunto de entregas e pesos definidos. Recursos/isolamento de campo e recuperação integral continuam pendentes; F2 não está inteiramente homologada. Mudança operacional requer escopo, backup, recuperação e pós-teste.
