# WiFi Guarderia Vitória

[Estado completo das implementações e pendências reais](docs/00-project/IMPLEMENTATION_STATUS.md). Publicação e versões rastreadas pelo histórico Git.

**Direção confirmada em 29/09/2026:** cada barco terá modem 4G e chip próprios. A distribuição de Internet por antenas na costa foi retirada devido à dificuldade de posicionamento e passagem de infraestrutura. A operação poderá fornecer os chips com gestão individual contratada; Vivo é a candidata provável. [Conectividade e gestão de linhas](docs/02-implementation/CELLULAR_CONNECTIVITY.md).

**Estado operacional preservado:** instalação da VPS/stack NOC e coleta interna concluídas; hub WireGuard, notebook de recuperação e RB750r2 da central NOC conectados. A funcionalidade da VPN da RB750r2 foi confirmada pelo usuário em 22/09/2026. Handshake/ping e SSH do notebook pela VPN têm evidência própria. Veja o [fechamento da stack](docs/06-validation/VPS_PHASE_COMPLETION.md) e a [validação do notebook](docs/06-validation/NOTEBOOK_VPN_VALIDATION.md).

**Próximo passo viável na VPS:** acompanhar os backups e planejar os ensaios restantes de recuperação integral; reboot, acesso VPN e restrições públicas TCP IPv4 já validados, conforme a [validação de acesso](docs/06-validation/VPS_ACCESS_VALIDATION.md). A VPN WireGuard da RB750r2 foi confirmada funcional pelo usuário em 22/09/2026. Rotas de LAN, coleta, failover e recuperação da RB continuam pendentes de evidência específica. Volumes Grafana/Prometheus migrados e restauração isolada a partir do S3 ensaiada; recuperação integral, kits 4G, segurança e campo seguem pendentes; F2 não está inteiramente homologada. Este repositório reúne documentação sanitizada; configurações reais e backups ficam fora do Git.

## Comece por aqui

1. Leia o [contexto consolidado](docs/00-project/CONTEXT.md) e os [requisitos rastreáveis](docs/00-project/REQUIREMENTS.md).
2. Consulte a [arquitetura](docs/01-architecture/ARCHITECTURE.md), o [endereçamento](docs/01-architecture/NETWORK_PLAN.md) e as [decisões](docs/01-architecture/DECISIONS.md).
3. Prepare a [VPS](docs/02-implementation/VPS_BOOTSTRAP.md), conforme a [especificação da stack](docs/02-implementation/STACK_SPEC.md).
4. Implante e valide a [coleta](docs/03-monitoring/METRICS.md) antes da [PoC](docs/06-validation/POC_PLAN.md).
5. Registre os resultados na [homologação](docs/06-validation/HOMOLOGATION.md).

## Direção atual

| Componente | Direção |
|---|---|
| Internet por barco | Modem 4G e SIM próprios; modelo/plano e cobertura a homologar |
| Chips e banda | Fornecimento pela operação é opção confirmada; gestão individual depende do contrato |
| Operadora | Vivo provável, sem escolha definitiva ou contratação |
| LAN embarcada | Roteador e WiFi/Ethernet local; integrado ao modem ou separado conforme seleção |
| Distribuição na margem | Retirada; sem core ou base de rádio obrigatórios |
| RB750Gr3 disponível | Reaproveitamento a avaliar, sem papel de core compartilhado |
| Central NOC | RB750r2 administrativa em uso; VPN confirmada em 22/09/2026 |
| VPS e monitoramento | Hub e stack existentes; coleta de campo ainda pendente |
| VPN de campo | Um peer por barco, iniciado via 4G; proposta sem implantação |

Internet sai diretamente pela linha de cada barco. NOC/VPS gerenciam e monitoram; vídeo grava localmente, com consulta sob demanda e consumo contabilizado. Cobertura embarcada, autonomia, franquia e reconexão são critérios da nova PoC. [Arquitetura](docs/01-architecture/ARCHITECTURE.md) e [plano de testes](docs/06-validation/POC_PLAN.md).

**Central NOC:** gateway administrativo existente, com inventário em 21/09 e VPN confirmada em 22/09. O [registro de alcance reverso](docs/06-validation/NOC_EDGE_VPN_VALIDATION.md) tem escopo específico; isolamento e failover não são presumidos. Não confundir essa administração com a central terrestre de distribuição retirada.

Os anexos RouterOS v7 recebidos foram [revisados](docs/02-implementation/ROUTEROS_BASELINE_REVIEW.md) e incorporados como [proposta de redundância WAN da central NOC](docs/02-implementation/NOC_DUAL_WAN.md). O template original exige adaptação e testes antes de importação; a existência de dois links ainda precisa ser confirmada.

## Investimento inicial para a PoC

O escopo inclui métricas de bateria, fumaça e bomba de porão por barco, com acionamento remoto da bomba quando viável. Sistemas geralmente 12 V e bombas variadas, conforme o usuário. A [pesquisa de dispositivos IoT](docs/01-architecture/IOT_MONITORING_RESEARCH.md) compara precisão, consumo, preços e integração com o NOC; compra, implantação e homologação permanecem pendentes.

O aporte estimado anteriormente em R$ 3.000,00 pertencia à PoC de enlace terrestre. O orçamento 4G precisa de nova cotação de modem/roteador, SIM/plano, energia, instalação e consumo dos testes; não há novo valor aprovado. [Modelo de custos por barco](docs/07-service/COSTS_AND_COMMERCIAL_MODEL.md).

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

## Acesso administrativo validado e integração futura da central NOC

Notebook 10.250.0.10 ↔ VPS 10.250.0.1 com SSH em TCP 5822 validado. Endpoint usado pelo notebook: `204.157.108.99:51820` (UDP); alias DNS documentado: `vpn-guarderia.awecloudsolution.com:51820`.

Preservar a VPN da RB750r2 já confirmada. Preparar backup/recuperação, seleção do kit e peers individuais dos barcos antes da coleta de campo. Os sete painéis receberam restrições por origem e quatro portas diretas receberam filtro; teste externo IPv4 aprovado conforme saída enviada pelo usuário; logins pós-mudança nos quatro consoles confirmados pelo usuário. Consulte [plano WireGuard](docs/02-implementation/WIREGUARD.md) e [pendências](docs/00-project/RISKS_AND_OPEN_ITEMS.md).

## Backup e persistência — atualização de 16/09/2026

Volumes de Grafana/Prometheus migrados e manifestos reconciliados. Backup local criptografado e restauração isolada validados; automação diária instalada. Envio diário ao AWS S3 ativado após download/hash e restauração isolada validados. O usuário configurou expiração S3 em sete dias; a previsão de expiração foi observada no backup e no recibo. A política local mantém 7 diários/4 semanais/3 mensais. Exclusão efetiva e recuperação integral ainda não homologadas. [Resultados e limites](docs/06-validation/BACKUP_AUTOMATION.md).

Alertas externos de backup por SES e Telegram implantados e ativos; incidentes sintéticos e recuperação recebidos nos dois canais. [Operação e limites](docs/06-validation/BACKUP_ALERTS.md).
