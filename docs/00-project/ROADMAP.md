# Plano de execução

Nenhum prazo de implantação foi confirmado. As fases abaixo são sequenciais por dependência, com critérios de saída observáveis.

| Fase | Entrega | Dependência | Critério de saída | Estado em 16/09/2026 |
|---|---|---|---|---|
| F0 | Especificação e Git | Contexto e referência | DOC-01/02 revisados; commit publicado | Documentação preparada |
| F1 | Inventário VPS, RBs e levantamento local | F0 | HW-01/VPS-01 e pendências impeditivas resolvidas | Parcial: inventário VPS realizado e RB951G atualizada; console Proxmox confirmado; acesso/inventário de rede da RB951G, core e levantamento local pendentes |
| F2 | WireGuard e stack NOC | F1 | VPN-01/02; STACK-01; backup restaurável | Stack/coleta interna e VPN notebook ↔ VPS validadas no escopo registrado; integração das RBs, segurança, persistência testada e restauração pendentes |
| F3 | Templates e alertas em bancada | F2 | MON-01/02/03; dados persistem após reboot | Pendente |
| F4 | Rádio e isolamento em bancada | F3 | RF-01; LAN-01; SEC-01/02/03 | Pendente |
| F5 | PoC embarcada 50/100 m | F4 e alimentação validada | RF-02/03/04; ENE-01 | Pendente |
| F6 | Kit de segurança e piloto prolongado | F5 | SECUR-01; VIDEO-01; OPS-02 | Pendente |
| F7 | Capacidade e modelo comercial | F6 | CAP-01; COM-01; riscos aceitos | Pendente |
| F8 | Lotes graduais até 20 barcos | F7 | Repetir onboarding e aceite por lote | Pendente |

## Próxima execução concreta

Etapa VPS/stack e coleta interna encerrada conforme [registro de conclusão](../06-validation/VPS_PHASE_COMPLETION.md). Hub e notebook conectados, com SSH confirmado conforme [validação](../06-validation/NOTEBOOK_VPN_VALIDATION.md). Suporte LXC e console já conferidos; não repetir instalação.

O usuário segue sem acesso à RB951G. Quando disponível, conferir interfaces, endereços, rotas e WANs; preparar backup/recuperação e configurar o trânsito VPS ↔ RB951G. Confirmar LAN real antes de anunciá-la; integrar RB750Gr3 depois. Seguir o [procedimento WireGuard](../02-implementation/WIREGUARD.md).

Enquanto aguarda acesso, podem ser planejadas/revisadas as pendências independentes da VPS: exposição pública e painéis via VPN, persistência de Grafana/Prometheus, backup/restauração, VIPs Swarm e abrangência do Node Exporter. Nenhuma delas foi executada nesta atualização. Mudanças operacionais exigem escopo, backup, recuperação e pós-teste. F2 segue parcial.

## Critério para expansão

Comprar e instalar por lotes pequenos após resultado do piloto. A aprovação de um barco não homologa capacidade de vinte estações. Testar concorrência e ocupação do rádio, incluindo acesso simultâneo às câmeras e falha de WAN.

## Governança

Separar três estados: especificado, implementado e homologado. O estado “operacional” só existe depois de implantação e teste real. Não atribuir percentuais sem conjunto de entregas e pesos definidos.
