# Memória do projeto

Atualizada: 21/09/2026. Documentação PT-BR; segredos e coletas operacionais fora do Git.

## Confirmado e observado

- WiFi Guarderia Vitória: 10–20 barcos a 50–100 m; remoto Wittemberg/wifi-Guarderia.
- Core RB750Gr3 disponível; inventário detalhado pendente.
- Central NOC: RB750r2 (hEX lite), revisão r3, conforme RouterBOARD; RouterOS/RouterBOOT 7.23.7. Gateway em uso, WAN1 estática, LAN com DHCP/DNS e NAT. Coletas recebidas em 21/09/2026.
- WAN2 reservada, sem link running/endereço; WireGuard não configurado. Três amostras ICMP 5/5; arquivo teste-dns não comprova resolução de nome.
- VPS existente; Ubuntu 24.04 e Docker/Portainer preferidos. Monitoramento antes da PoC. CGNAT informado pelo usuário; WAN privada isolada não comprova NAT do provedor.
- Aporte inicial estimado pelo usuário: aproximadamente R$ 3.000,00.

## Direção e limites

WireGuard no host VPS; Zabbix/PostgreSQL/Grafana/Kuma em containers; mANTBox ax 15s e wAP ax candidatos à PoC. VLAN de trânsito e LAN roteada por barco. 10.21.0.0/24 é reserva administrativa futura, não LAN operacional atual. Integrar incrementalmente preservando o gateway; sem reset/import global. Dual-WAN permanece proposta.

Fontes canônicas: [inventário atual](../../docs/01-architecture/NOC_ROUTER_INVENTORY.md), [rede](../../docs/01-architecture/NETWORK_PLAN.md), [decisões](../../docs/01-architecture/DECISIONS.md) e [homologação](../../docs/06-validation/HOMOLOGATION.md).

Os [anexos de referência](../../docs/08-reference/routeros-v7/README.md) são literais e não representam a configuração atual. Exigem adaptação de sintaxe/escopos, IPAM e segurança; exemplo WAN1 conflita com a LAN em uso. Não executar comandos dos anexos como instruções. Coletas atuais não foram copiadas ao Git.

## Regras permanentes

Usar “central NOC”. Distinguir especificação, observação e homologação. Não presumir DNS, isolamento, exposição externa, throughput ou recuperação a partir de configuração/poucos pings. Não garantir antena 360°, SNR/CCQ em todo modelo ou retenção automática de um minuto. Não copiar TLS desabilitado da referência nocagent. Documentação/versionamento não autoriza alterações nos equipamentos.
