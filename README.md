# WiFi Guarderia Vitória

Projeto de conectividade e segurança náutica para 10–20 barcos fundeados a aproximadamente 50–100 metros da margem, com infraestrutura compartilhada e operação por mensalidade.

**Estado em 21/09/2026:** gateway da central NOC em uso, com configuração básica e coletas analisadas; VPS, VPN, monitoramento e homologação de campo pendentes. Este repositório não contém uma stack implantada nem configurações prontas para aplicação em equipamentos.

## Comece por aqui

1. Leia o [contexto consolidado](docs/00-project/CONTEXT.md) e os [requisitos rastreáveis](docs/00-project/REQUIREMENTS.md).
2. Consulte a [arquitetura](docs/01-architecture/ARCHITECTURE.md), o [endereçamento](docs/01-architecture/NETWORK_PLAN.md) e as [decisões](docs/01-architecture/DECISIONS.md).
3. Prepare a [VPS](docs/02-implementation/VPS_BOOTSTRAP.md), conforme a [especificação da stack](docs/02-implementation/STACK_SPEC.md).
4. Implante e valide a [coleta](docs/03-monitoring/METRICS.md) antes da [PoC](docs/06-validation/POC_PLAN.md).
5. Registre os resultados na [homologação](docs/06-validation/HOMOLOGATION.md).

## Direção atual

| Componente | Direção |
|---|---|
| Internet da guarderia | Provedor local; CGNAT provável |
| Core | MikroTik RB750Gr3 já disponível |
| Margem | mANTBox ax 15s, prevista para a PoC |
| Barco | wAP ax: cliente 5 GHz e AP local 2,4 GHz |
| Administração na central NOC | RB750r2 (hEX lite) atualizada: RouterOS e RouterBOOT 7.23.7; gateway em uso; VPN pendente |
| Central | VPS existente, Ubuntu 24.04, IPv4 público |
| VPN | WireGuard no host da VPS; proposta de engenharia |
| Monitoramento | Zabbix + PostgreSQL + Grafana + Uptime Kuma em Docker/Portainer |

Um rádio por barco é a hipótese a validar. Rotação, obstruções, maresia, energia e capacidade compartilhada são critérios de decisão, não detalhes posteriores.

**Central NOC:** RB750r2 (hEX lite), revisão r3, com RouterOS/RouterBOOT **7.23.7**, WAN1 estática, DHCP/DNS na LAN e NAT. WAN2 reservada; WireGuard ainda não configurado. As amostras recebidas mostram resposta ICMP ao gateway e a destinos externos. Consulte o [inventário e análise da configuração atual](docs/01-architecture/NOC_ROUTER_INVENTORY.md).

Os anexos RouterOS v7 recebidos foram [revisados](docs/02-implementation/ROUTEROS_BASELINE_REVIEW.md) e incorporados como [proposta de redundância WAN da central NOC](docs/02-implementation/NOC_DUAL_WAN.md). O template original exige adaptação e testes antes de importação; a existência de dois links ainda precisa ser confirmada.

## Investimento inicial para a PoC

Após consultas e análises de preços de mercado, estima-se a necessidade de um **aporte financeiro de aproximadamente R$ 3.000,00** para viabilizar a prova de conceito (PoC), destinado à aquisição dos equipamentos básicos necessários para iniciar os testes.

## Documentação e governança

- [Índice completo](docs/README.md)
- [Plano de execução](docs/00-project/ROADMAP.md)
- [Pendências e riscos](docs/00-project/RISKS_AND_OPEN_ITEMS.md)
- [Referência técnica nocagent](docs/08-reference/NOCAGENT_REVIEW.md)
- [Baseline corporativa Witteberg](witteberg-development-standards/README.md)
- [Instruções para agentes](AGENTS.md)
- [Histórico de alterações](CHANGELOG.md)
- [Como contribuir](CONTRIBUTING.md)

Repositório oficial: [Wittemberg/wifi-Guarderia](https://github.com/Wittemberg/wifi-Guarderia). A pasta de trabalho local é a raiz deste checkout. Segredos e evidências identificáveis ficam fora do Git, conforme a [política de segurança](docs/04-security/SECURITY.md).

## Licenciamento

A licença deste projeto ainda deve ser definida pelo titular. Nenhuma licença de software livre é presumida. O `nocagent` é referência de engenharia; seu código, marca, credenciais e infraestrutura não foram incorporados. Consulte a [proveniência](docs/08-reference/NOCAGENT_REVIEW.md).
