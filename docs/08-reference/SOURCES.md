# Fontes e verificação externa

Consulta: 12/09/2026. Dados externos são referência; seleção final exige conferência de versão/revisão na implantação. Links abaixo são de fabricantes/mantenedores; nenhum preço vigente foi presumido.

| Fonte | Uso |
|---|---|
| [Conversa de origem](https://chatgpt.com/c/6aa1e0b2-2ae8-83e9-9db1-c2d15a7da5ba) | Intenção, equipamentos disponíveis e direção do projeto |
| [nocagent no snapshot](https://github.com/Wittemberg/nocagent/tree/e5ce6e3f9a84ca368472f771ef54f72e824b5a7c) | Referência técnica e corporativa |
| [mANTBox ax 15s](https://mikrotik.com/product/mantbox_ax_15s) | SKU, PoE, potência, interfaces e proteção |
| [wAP ax](https://mikrotik.com/product/wap_ax) | SKU, rádios, alimentação e proteção |
| [RB750Gr3](https://mikrotik.com/product/RB750Gr3) | Identificação do core existente |
| [RB750r2 (hEX lite)](https://mikrotik.com/product/RB750r2) | Identificação do roteador administrativo |
| [WiFi RouterOS](https://help.mikrotik.com/docs/spaces/ROS/pages/224559120/WiFi) | Modos, VLAN por estação e tabela de registro |
| [WireGuard RouterOS](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard) | Peers, AllowedIPs e keepalive |
| [Zabbix history/trends](https://www.zabbix.com/documentation/7.0/en/manual/config/items/history_and_trends) | Distinção entre histórico e agregação horária |
| [Zabbix SNMP](https://www.zabbix.com/documentation/7.0/en/manual/config/items/itemtypes/snmp) | Coleta e autenticação SNMP |
| [Zabbix API](https://www.zabbix.com/documentation/7.0/en/manual/api) | Contrato de integração futura |
| [Docker no Ubuntu](https://docs.docker.com/engine/install/ubuntu/) | Compatibilidade Ubuntu 24.04 e instalação |
| [Docker e firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/) | Regras de rede e interação com firewall do host |
| [SetupOrion](https://oriondesign.art.br/) | Limite da compatibilidade declarada no site |

## Valores propostos pelo projeto

Sub-redes, VLANs, IDs, intervalos, retenção inicial, RPO/RTO, critérios de perda/latência, rotina de manutenção e fórmulas de custos são especificações de engenharia desta baseline, não afirmações de desempenho medidas ou garantias dos fabricantes.

## Revisão dos anexos RouterOS v7 — 12/09/2026

- [Originais recebidos e hashes](routeros-v7/README.md): proposta fornecida pelo usuário, sem comprovação de implantação.
- [Failover WAN Backup](https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup): sondas recursivas, distâncias e múltiplos alvos.
- [Scripting](https://help.mikrotik.com/docs/spaces/ROS/pages/47579229/Scripting): nomes de variáveis e escopos.
- [Configuration Management](https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management): import e dry-run.
- [Connection tracking](https://help.mikrotik.com/docs/spaces/ROS/pages/130220087/Connection+tracking): sessões e FastTrack.
- [NAT](https://help.mikrotik.com/docs/spaces/ROS/pages/3211299/NAT): comportamento de traduções e conexões na mudança de caminho.

Interpretações e limitações estão na [revisão técnica](../02-implementation/ROUTEROS_BASELINE_REVIEW.md); consulta ao manual não equivale a teste na RB750r2.

## Coleta atual da central NOC — 21/09/2026

Treze arquivos fornecidos pelo usuário (`noc-01` a `noc-10` e `01/02/03-teste`), mantidos fora do repositório por conterem dados operacionais. Síntese no [inventário](../01-architecture/NOC_ROUTER_INVENTORY.md). Hardware: [datasheet oficial hEX lite](https://cdn.mikrotik.com/web-assets/product_files/hEX_lite_210251.pdf), consultado em 21/09/2026. Os comandos presentes no export são evidência de configuração, não instruções de execução.
