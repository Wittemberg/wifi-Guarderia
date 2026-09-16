# WiFi Guarderia Vitória

**Estado em 16/09/2026:** instalação da VPS/stack NOC e coleta interna concluídas; hub WireGuard e notebook de recuperação conectados. Handshake e ping observados na VPS; acesso SSH pela VPN confirmado pelo usuário. Veja o [fechamento da stack](docs/06-validation/VPS_PHASE_COMPLETION.md) e a [validação do notebook](docs/06-validation/NOTEBOOK_VPN_VALIDATION.md).

**Próximo marco:** integrar a RB951G da central NOC quando o usuário tiver acesso ao equipamento. Acesso e inventário de rede da RB ainda indisponíveis. Core, segurança, persistência testada, restauração e campo seguem pendentes; F2 não está inteiramente homologada. Este repositório reúne documentação sanitizada; configurações reais e backups ficam fora do Git.

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
| Administração na central NOC | RB951G-2HnD atualizada: RouterOS e RouterBOOT 7.23.5; aguarda acesso/inventário de rede |
| Central | VPS existente, Ubuntu 24.04, IPv4 público |
| VPN | WireGuard no host da VPS e notebook implantados; RBs pendentes |
| Monitoramento | Zabbix/PostgreSQL, Grafana, Kuma e Prometheus/exporters instalados em Docker Swarm/Portainer |

Um rádio por barco é a hipótese a validar. Rotação, obstruções, maresia, energia e capacidade compartilhada são critérios de decisão, não detalhes posteriores.

**Central NOC:** a RB951G-2HnD foi atualizada; a VPS já está preparada. O usuário ainda não tem acesso à RB para inventário e configuração. O inventário informado pelo usuário registra RouterOS **7.23.5 (long-term)** e firmware atual/disponível **7.23.5**. A configuração e a homologação da VPN permanecem pendentes. Consulte o [registro técnico da RB951G](docs/01-architecture/NOC_ROUTER_INVENTORY.md).

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

## Próxima etapa — integração da central NOC

Notebook 10.250.0.10 ↔ VPS 10.250.0.1 com SSH em TCP 5822 validado. Endpoint usado pelo notebook: `204.157.108.99:51820` (UDP); alias DNS documentado: `vpn-guarderia.awecloudsolution.com:51820`.

Quando houver acesso à RB951G, conferir LAN/rotas, backup e recuperação para integrar seu peer; RB750Gr3 e coleta de campo depois. A restrição dos painéis públicos ainda precisa de revisão e teste próprios. Consulte [plano WireGuard](docs/02-implementation/WIREGUARD.md) e [pendências](docs/00-project/RISKS_AND_OPEN_ITEMS.md).
