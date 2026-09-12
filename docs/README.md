# Índice da documentação técnica

Baseline 0.1.0 — 12/09/2026. O projeto está especificado, ainda não implantado. A distinção entre decisões, propostas e evidências é mantida em cada domínio.

## 00 — Projeto

| Documento | Conteúdo |
|---|---|
| [Contexto consolidado](00-project/CONTEXT.md) | Origem, requisitos do usuário e evolução das escolhas |
| [Requisitos](00-project/REQUIREMENTS.md) | IDs, prioridade, origem e testes de aceite |
| [Roadmap](00-project/ROADMAP.md) | Fases, dependências e critérios de saída |
| [Riscos e pendências](00-project/RISKS_AND_OPEN_ITEMS.md) | Informações necessárias e gates de execução |

## 01 — Arquitetura e infraestrutura

| Documento | Conteúdo |
|---|---|
| [Arquitetura](01-architecture/ARCHITECTURE.md) | Topologia, fluxos e responsabilidades |
| [Plano de rede](01-architecture/NETWORK_PLAN.md) | IPAM para 20 barcos, VLANs, portas, rotas e NAT |
| [Decisões](01-architecture/DECISIONS.md) | ADRs, alternativas e consequências |
| [Hardware e RF](01-architecture/HARDWARE_AND_RF.md) | Modelos, perfil RF, levantamento e materiais |
| [Energia e instalação](01-architecture/POWER_AND_INSTALLATION.md) | PoE, DC, autonomia e ambiente marítimo |

## 02 — Implementação

| Documento | Conteúdo |
|---|---|
| [Preparação VPS](02-implementation/VPS_BOOTSTRAP.md) | Inventário, Ubuntu/Orion e sequência de implantação |
| [Stack](02-implementation/STACK_SPEC.md) | Serviços, persistência, redes, secrets e versões |
| [WireGuard](02-implementation/WIREGUARD.md) | Peers, AllowedIPs, rotas, SNAT e recuperação |
| [Provisionamento MikroTik](02-implementation/MIKROTIK_PROVISIONING.md) | Roteiro por equipamento e futuras configurações |
| [Configuração do monitoramento](02-implementation/MONITORING_SETUP.md) | Sequência de templates, coleta, dashboards e alertas |

## 03 — Monitoramento

| Documento | Conteúdo |
|---|---|
| [Métricas](03-monitoring/METRICS.md) | Fontes, unidades, frequência e qualidade |
| [Alertas e painéis](03-monitoring/ALERTS_AND_DASHBOARDS.md) | Limiares iniciais, dependências e notificação |
| [Capacidade e retenção](03-monitoring/CAPACITY_AND_RETENTION.md) | Taxa de amostras, disco e carga RF/WAN |

## 04 — Segurança

[Segurança e dados](04-security/SECURITY.md): fluxos permitidos, papéis, TLS, segredos, isolamento, ameaças e testes.

## 05 — Operação

| Documento | Conteúdo |
|---|---|
| [Backup e restauração](05-operations/BACKUP_RESTORE.md) | RPO/RTO, cópias e ensaio de recuperação |
| [Runbooks](05-operations/RUNBOOKS.md) | Diagnóstico, mudanças e resposta a incidentes |
| [Onboarding e manutenção](05-operations/ONBOARDING_AND_MAINTENANCE.md) | Cadastro, inspeção e rotina operacional |

## 06 — Validação

| Documento | Conteúdo |
|---|---|
| [Plano PoC](06-validation/POC_PLAN.md) | Bancada, 50/100 m, rotação, carga e critérios |
| [Homologação](06-validation/HOMOLOGATION.md) | Estado real dos testes e aceites |
| [Modelos de evidência](06-validation/EVIDENCE_TEMPLATES.md) | Registros de sessão, medição e mudança |
| [Revisão documental](06-validation/DOCUMENTATION_REVIEW.md) | Verificações desta primeira entrega |

## 07 — Serviço e evolução

| Documento | Conteúdo |
|---|---|
| [Kits e responsabilidades](07-service/SECURITY_KITS_AND_SERVICE.md) | Alarme, câmeras e vigilância |
| [Custos e mensalidade](07-service/COSTS_AND_COMMERCIAL_MODEL.md) | CAPEX/OPEX e cenários para 10/15/20 |
| [Integração NOC-Agent](07-service/NOCAGENT_INTEGRATION.md) | Contrato futuro de leitura e ações governadas |

## 08 — Referências

| Documento | Conteúdo |
|---|---|
| [Análise nocagent](08-reference/NOCAGENT_REVIEW.md) | Fontes, adoção e divergências encontradas |
| [Inventário do snapshot](08-reference/REFERENCE_INVENTORY.md) | Caminhos e hashes da árvore consultada |
| [Fontes externas](08-reference/SOURCES.md) | Links dos fabricantes e mantenedores |

## Orientações do repositório

[README](../README.md), [AGENTS](../AGENTS.md), [.agents](../.agents/README.md), [baseline corporativa](../witteberg-development-standards/README.md), [contribuição](../CONTRIBUTING.md) e [changelog](../CHANGELOG.md).
