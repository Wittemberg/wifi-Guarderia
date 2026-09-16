# Análise técnica do projeto de referência

Fonte: [Wittemberg/nocagent](https://github.com/Wittemberg/nocagent). Branch consultada: `main`. Snapshot local de leitura no commit **e5ce6e3f9a84ca368472f771ef54f72e824b5a7c**, em 12/09/2026. Nenhuma alteração foi feita no repositório de referência.

## Método e alcance

Inventário da árvore versionada, leitura detalhada dos documentos centrais, regras/memória/estrutura `.agents`, conteúdo dos padrões Witteberg e documentos de arquitetura, implementação, segurança, governança e operação relevantes. Confronto adicional com `core/src/drivers/mikrotik.js`, `core/src/drivers/zabbix.js` e `docker-compose.yml` para não tratar intenção documental como comportamento implementado.

Não foi executada a aplicação `nocagent`, nem auditada sua produção ou provado o estado de todas as funcionalidades anunciadas. Skills genéricas de jogos/mobile/SEO e campanhas comerciais foram inventariadas, sem adoção. O [inventário de referência](REFERENCE_INVENTORY.md) permite localizar os arquivos no snapshot.

## Fontes principais e aplicação

Todos os caminhos da tabela são relativos ao commit acima.

| Caminho na referência | Leitura aplicada à Guarderia |
|---|---|
| `.agents/README.md`, `rules/core-protocol.md`, `rules/universal-rules.md` | Contexto progressivo, regras locais e verificação; sem instalar runtime |
| `.agents/memory/MEMORY.md`, `tech-decisions.md`, `project-conventions.md` | Memória persistente e separação de decisões do usuário |
| `.agents/agent/documentation-writer.md`, `skills/documentation-templates/SKILL.md` | Índice, documentos por propósito, ADRs e changelog |
| `witteberg-development-standards/README.md` | Baseline corporativa declarada |
| `engineering/SECURITY-BASELINE.md` dentro dos padrões | Segredos externos, papéis e logs sanitizados |
| `engineering/PERSISTENCE-RELIABILITY.md` | Restart não perde configuração e identidades |
| `engineering/QUALITY-NON-REGRESSION.md` | Mudança mínima e teste real para hardware |
| `patterns/LOCAL-AGENTS.md`, `patterns/ERROR-HANDLING.md` | Reconexão, diagnóstico e estados distintos |
| `frontend/*`, `components/*`, `checklists/*`, `templates/*` dentro dos padrões | Apresentação, feedback, release e aceite |
| `docs/00-project/PROJECT_OVERVIEW.md`, `development-control/README.md` | Separar especificação, implementação e homologação |
| `docs/01-architecture/adr/ADR-001-agent-outbound.md` | Conexão iniciada atrás de CGNAT, adaptada a WireGuard |
| `docs/01-architecture/adr/ADR-013-idempotency-locks.md` | Mudanças futuras com idempotência e trava |
| `docs/01-architecture/adr/ADR-015-ai-not-runtime-dependency.md` | NOC independente de IA |
| `docs/01-architecture/adr/ADR-019-inventory-trust-and-reconciliation.md` | Inventário com origem e verificação |
| `docs/01-architecture/adr/ADR-020-network-device-driver-abstraction.md` | Capacidade explícita e recurso não suportado |
| `docs/01-architecture/adr/ADR-021-wan-change-safety-and-rollback.md` | Backup, pré/pós-teste e recuperação do caminho de gerência |
| `docs/02-implementation/03_CONFIG_AMBIENTES_E_PADROES.md` | Configuração explícita, UTC e erros identificáveis |
| `docs/02-implementation/04_MODELO_DE_DADOS.md` | IDs e escopo; sem copiar banco de produto |
| `docs/02-implementation/08_ACTION_FRAMEWORK.md`, `09_POLICY_ENGINE_APPROVALS_LOCKS.md` | Contrato futuro de ação e restrições |
| `docs/02-implementation/11_OBSERVABILIDADE.md`, `17_ALERTAS_INCIDENTES_NOTIFICACOES.md` | Observar o coletor e correlacionar incidentes |
| `docs/02-implementation/18_DEPLOY_PORTAINER_CICD.md`, `19_TESTES_SEGURANCA_QA.md` | Versões fixas, redes privadas e ensaio de falhas |
| `docs/02-implementation/27_NETWORK_DEVICE_MONITORING_AND_GOVERNED_WAN_ACTIONS.md` | Telemetria por capacidade e mudança governada |
| `docs/02-implementation/PLATFORM_BACKUP_RECOVERY.md` | Backup da própria central; procedimentos corrigidos |
| `docs/04-security/RBAC.md`, `THREAT_MODEL.md` | Isolamento e ameaças concretas |
| `docs/06-product/UI_TERMINOLOGY_AND_STATUS_STANDARD.md` | Linguagem PT-BR e estado sem dados |

Links de auditoria: [árvore do snapshot](https://github.com/Wittemberg/nocagent/tree/e5ce6e3f9a84ca368472f771ef54f72e824b5a7c), [padrões Witteberg](https://github.com/Wittemberg/nocagent/tree/e5ce6e3f9a84ca368472f771ef54f72e824b5a7c/witteberg-development-standards), [.agents](https://github.com/Wittemberg/nocagent/tree/e5ce6e3f9a84ca368472f771ef54f72e824b5a7c/.agents), [docs](https://github.com/Wittemberg/nocagent/tree/e5ce6e3f9a84ca368472f771ef54f72e824b5a7c/docs).

## Divergências que impedem cópia automática

1. A referência contém documentação de InfraOps AI mais abrangente que a árvore de implementação observada e documentos que anunciam etapas concluídas. Isso não comprova homologação da Guarderia nem de cada funcionalidade da referência.
2. `docs/05-operations/INSTALLATION.md`, `DEPLOYMENT.md`, `MONITORING.md`, `BACKUP_RESTORE.md` e `TROUBLESHOOTING.md` são esboços. Foram substituídos por procedimentos próprios completos nesta especificação.
3. O driver MikroTik consultado configura `rejectUnauthorized: false`. A Guarderia exige verificação TLS e conta de coleta mínima.
4. O mesmo driver atribui `lastLossPercent` 0 ou 100 conforme uma sondagem TCP. A Guarderia separa porta acessível, RTT TCP e perda ICMP medida em janela com contagem de pacotes.
5. O driver Zabbix consultado usa padrões de autenticação/login que precisam de revisão por versão. Não será copiado como integração homologada.
6. O procedimento de backup consultado mistura caminhos temporários do container e do host. A Guarderia exige transferência explícita e teste de restauração.
7. A stack de referência usa rede/serviços/domínio existentes e tags `latest`; o projeto novo não presume essa infraestrutura. Atualização de 16/09/2026: Swarm instalado pelo usuário; imagens/digests registrados no fechamento da etapa VPS. Revisão de versões e manifesto de manutenção pendente.
8. O plano de InfraOps usa Prometheus para séries próprias. Isso não proíbe o banco PostgreSQL suportado pelo Zabbix armazenar seus dados; são arquiteturas diferentes. Não duplicar armazenamento sem necessidade.

Esses achados são limitados ao snapshot e aos arquivos citados; não constituem auditoria completa da aplicação ou de sua produção.

## Adoção seletiva

O diretório local `witteberg-development-standards` é uma síntese adaptada, com atribuição, não uma cópia integral do pacote original. `.agents` também é uma adaptação documental. Não foram incorporados hooks, MCPs, credenciais, imagens, scripts de implantação ou integrações comerciais da referência. A licença do projeto Guarderia continua a definir pelo titular.
