# Plano de execução

Nenhum prazo de implantação foi confirmado. As fases abaixo são sequenciais por dependência, com critérios de saída observáveis.

| Fase | Entrega | Dependência | Critério de saída | Estado inicial |
|---|---|---|---|---|
| F0 | Especificação e Git | Contexto e referência | DOC-01/02 revisados; commit publicado | Documentação preparada |
| F1 | Inventário VPS, RBs e levantamento local | F0 | HW-01/VPS-01 e pendências impeditivas resolvidas | Parcial: RB750r2 atualizada e inventariada pelo usuário; demais itens pendentes |
| F2 | WireGuard e stack NOC | F1 | VPN-01/02; STACK-01; backup restaurável | Pendente |
| F3 | Templates e alertas em bancada | F2 | MON-01/02/03; dados persistem após reboot | Pendente |
| F4 | Rádio e isolamento em bancada | F3 | RF-01; LAN-01; SEC-01/02/03 | Pendente |
| F5 | PoC embarcada 50/100 m | F4 e alimentação validada | RF-02/03/04; ENE-01 | Pendente |
| F6 | Kit de segurança e piloto prolongado | F5 | SECUR-01; VIDEO-01; OPS-02 | Pendente |
| F7 | Capacidade e modelo comercial | F6 | CAP-01; COM-01; riscos aceitos | Pendente |
| F8 | Lotes graduais até 20 barcos | F7 | Repetir onboarding e aceite por lote | Pendente |

## Próxima execução concreta

Inventariar e preparar a VPS: SO, CPU/RAM, disco, IPs, Docker, modo Compose/Swarm, Portainer, redes, volumes e serviços existentes. A RB750r2 da central NOC está atualizada e em uso como gateway; a integração VPN será incremental após a VPS, preservando LAN, DHCP e NAT existentes. Conferir ainda RouterOS e modelo da RB750Gr3 e resolver os itens restantes de `OPEN-01` a `OPEN-05` antes de produzir scripts aplicáveis.

## Critério para expansão

Comprar e instalar por lotes pequenos após resultado do piloto. A aprovação de um barco não homologa capacidade de vinte estações. Testar concorrência e ocupação do rádio, incluindo acesso simultâneo às câmeras e falha de WAN.

## Governança

Separar três estados: especificado, implementado e homologado. O estado “operacional” só existe depois de implantação e teste real. Não atribuir percentuais sem conjunto de entregas e pesos definidos.
