# Índice da documentação técnica

Entrada para acompanhamento: [estado consolidado das implementações](00-project/IMPLEMENTATION_STATUS.md).

Atualização de 16/09/2026: etapa VPS/stack e coleta interna concluída; [evidências e pendências](06-validation/VPS_PHASE_COMPLETION.md). Hub WireGuard e notebook também implantados, com SSH confirmado; [validação e limites](06-validation/NOTEBOOK_VPN_VALIDATION.md). Inventário da RB750r2 recebido em 21/09/2026; VPN WireGuard funcional confirmada pelo usuário em 22/09/2026. Instalação observada e homologação completa são estados distintos.

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
| [Inventário da VPS](01-architecture/VPS_INVENTORY.md) | Recursos e serviços observados em 15/09/2026, limitações e pendências |
| [Inventário da RB750r2 central NOC](01-architecture/NOC_ROUTER_INVENTORY.md) | Atualização 7.23.7 e recursos informados pelo usuário |
| [Energia e instalação](01-architecture/POWER_AND_INSTALLATION.md) | PoE, DC, autonomia e ambiente marítimo |

## 02 — Implementação

| Documento | Conteúdo |
|---|---|
| [Domínios e DNS](02-implementation/DOMAINS_AND_DNS.md) | Aliases planejados, acesso e validação pendente |
| [Preparação VPS](02-implementation/VPS_BOOTSTRAP.md) | Inventário, Ubuntu/Orion e sequência de implantação |
| [Stack](02-implementation/STACK_SPEC.md) | Serviços, persistência, redes, secrets e versões |
| [WireGuard](02-implementation/WIREGUARD.md) | Peers, AllowedIPs, rotas, SNAT e recuperação |
| [Provisionamento MikroTik](02-implementation/MIKROTIK_PROVISIONING.md) | Roteiro por equipamento e futuras configurações |
| [Configuração do monitoramento](02-implementation/MONITORING_SETUP.md) | Sequência de templates, coleta, dashboards e alertas |
| [Revisão RouterOS recebido](02-implementation/ROUTEROS_BASELINE_REVIEW.md) | Achados, divergências e condições para adaptar o template |
| [Dual-WAN central NOC](02-implementation/NOC_DUAL_WAN.md) | Proposta de failover, pré-requisitos e ensaios |

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
| [Conclusão VPS/stack](06-validation/VPS_PHASE_COMPLETION.md) | Etapa concluída, imagens observadas, evidências e pendências |
| [Homologação](06-validation/HOMOLOGATION.md) | Estado real dos testes e aceites |
| [Persistência e backups](06-validation/PERSISTENCE_BACKUP_AUDIT.md) | Auditoria, restauração isolada e migração preparada |
| [VPN do notebook](06-validation/NOTEBOOK_VPN_VALIDATION.md) | Cadastro, handshake, ping, SSH confirmado e limites |
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
| [Anexos RouterOS v7](08-reference/routeros-v7/README.md) | Originais preservados, hashes e limites de uso |

## Orientações do repositório

[README](../README.md), [AGENTS](../AGENTS.md), [.agents](../.agents/README.md), [baseline corporativa](../witteberg-development-standards/README.md), [contribuição](../CONTRIBUTING.md) e [changelog](../CHANGELOG.md).

[Coleta interna do Prometheus](03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md): correção dos alvos após instalação Orion.

- [Backup automático e restauração isolada](06-validation/BACKUP_AUTOMATION.md)

- [Plano executado: acesso administrativo da VPS pela VPN](04-security/VPS_ACCESS_PLAN.md)

- [Validação das restrições dos painéis](06-validation/VPS_ACCESS_VALIDATION.md): regras implantadas, testes locais, pendências externas e retorno.
- [Restrição de infraestrutura e SSH](06-validation/VPS_HOST_ACCESS_VALIDATION.md): restrições aplicadas e testes TCP IPv4/VPN aprovados; limites e retorno documentados.
- [Ensaio de reboot da VPS](06-validation/VPS_REBOOT_VALIDATION.md): pré-testes, verificador automático e recuperação.
- [Alertas externos de backup](06-validation/BACKUP_ALERTS.md): preparação, permissões e critérios de ativação.
