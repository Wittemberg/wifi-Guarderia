# Auditoria de persistência e primeiro ensaio de restauração

Registro histórico: observações e pendências abaixo correspondem à etapa original. Migração, S3, restrições de acesso, reboot e alertas foram posteriormente executados; consultar o [estado consolidado vigente](../00-project/IMPLEMENTATION_STATUS.md) antes de tratar uma pendência deste registro como atual.

**Atualização posterior:** migração e automação local executadas; veja [resultados atuais](BACKUP_AUTOMATION.md). As seções abaixo preservam o estado da auditoria inicial, anterior à migração.

Data: 16/09/2026. Escopo autorizado pelo usuário: iniciar revisão de persistência, preparar backups e testar restauração sem depender da RB951G. Auditoria, backups locais e ensaios isolados executados; migração dos volumes de produção ainda não aplicada.

## Inventário observado

| Serviço/dado | Armazenamento atual | Resultado e ação |
|---|---|---|
| Grafana 13.2.2 | SQLite em /var/lib/grafana, sem volume nesse caminho | Risco de perda ao substituir a tarefa; criar guarderia_grafana_data após cópia consistente |
| Configuração/provisioning Grafana | Binds em /opt/monitor-orion/grafana | Copiados em backup privado; preservar no manifesto |
| Prometheus | /prometheus em volume anônimo não fixado no serviço | Cerca de 103 MB na consulta; migrar para guarderia_prometheus_data preservando histórico |
| Configuração Prometheus | Bind do prometheus.yml em /opt/monitor-orion | Backup feito; coleta interna atual deve ser preservada |
| PostgreSQL 15 do Zabbix | zabbix_postgres_data | Volume nomeado; dump lógico e restauração executados |
| PostgreSQL 14 separado | postgres_data | Volume nomeado; dump lógico e restauração executados |
| Uptime Kuma | uptimekuma em /app/data | SQLite; backup consistente e inicialização/reinício da cópia testados |
| Portainer | portainer_data em /data | Volume nomeado; backup consistente do banco Portainer ainda pendente |
| Traefik/certificados | volume_swarm_certificates | Volume nomeado; backup consistente do conteúdo e restauração TLS ainda pendentes |
| Zabbix server | Volumes anônimos para export e snmptraps | Uso/retenção precisam ser definidos; estado principal do Zabbix está no PostgreSQL |
| cAdvisor/Node Exporter | Coletores, sem banco próprio de séries | Séries ficam no Prometheus; parâmetros capturados no inventário privado |
| WireGuard | /etc/wireguard no host | Configuração atual incluída no backup privado; não ativada em ambiente duplicado |

Volumes locais nomeados não são cópias de segurança nem asseguram recuperação em outro host. Prometheus observado com retenção de 15 dias e API administrativa desabilitada. Não habilitamos essa API para obter snapshot, pois ela também oferece operações mutáveis e exige revisão de acesso. Não foi produzida cópia integral consistente da TSDB nesta etapa.

## Backups produzidos

Diretório privado identificado por `persistence-20260916T212839Z`, fora do Git. Inclui inventário completo de serviços/containers, configurações de monitoramento, manifestos YAML locais, WireGuard atual, bancos SQLite e arquivos auxiliares de Grafana/Kuma, dumps PostgreSQL e objetos globais. Arquivos e diretórios restritos; os dados não foram enviados a terceiros.

O manifesto final lista 17 arquivos de backup, totalizando 99.846.435 bytes, com SHA-256 recalculado e conferido. Cópias de inventário, resultados e diretórios de restauração são adicionais. Não há cifragem off-site, agendamento ou política de rotação implantados. Dados restaurados para testes continuam privados na VPS; containers temporários foram removidos.

Grafana/Kuma foram copiados pela API de backup online do SQLite, com bancos finais checkpointados, fechados e verificados. Isso evita tratar uma cópia simples do arquivo ativo como backup consistente. Arquivos auxiliares foram arquivados separadamente; não se presume snapshot atômico entre banco, plugins e índices derivados. Para a migração de produção, preparar uma cópia final com escritas suspensas.

PostgreSQL: pg_dump em formato custom por banco e pg_dumpall --globals-only, usando os clientes das imagens instaladas. Saídas binárias gravadas sem PTY, credenciais e nomes reais preservados no registro privado. Restaurados objetos globais e bancos com parada em erro, preservando proprietários e permissões. Os snapshots dos diferentes bancos não são simultâneos.

## Ensaios executados

| Ensaio | Resultado | Limite |
|---|---|---|
| PostgreSQL 15/Zabbix | Dois bancos restaurados; banco Zabbix com 207 tabelas públicas, banco de manutenção sem tabelas públicas | Aplicação Zabbix não foi ligada à cópia; sem comparação exaustiva de linhas |
| PostgreSQL 14 | Banco restaurado sem tabelas públicas | Não representa carga de uma aplicação futura |
| Grafana | Backup com integrity_check OK, 92 tabelas; cópia iniciou e reiniciou com /api/health indicando database=ok | Sem login humano, envio de alertas ou consulta externa a datasources |
| Kuma | Backup com integrity_check OK, 23 tabelas; cópia iniciou e reiniciou respondendo HTTP 200 | Sem login humano, testes de notificações ou alcance de monitores |
| Verificação de arquivos | 17 hashes SHA-256 conferidos após finalizar os bancos SQLite | Hash verifica integridade, não substitui ensaio funcional |

Containers de teste usaram as mesmas imagens locais por ID, network=none, nenhuma porta publicada, limite de 1 CPU/512 MiB e diretórios próprios. Nenhum volume de dados de produção foi ligado com escrita aos testes. Grafana usou configuração/provisioning de produção em modo somente leitura; seu banco era a cópia isolada. Reinícios ocorreram apenas nas cópias.

Tempos observados dos ensaios: PostgreSQL 15, 16,786 s; PostgreSQL 14, 6,475 s; inicialização/reinício/verificação de Grafana, 14,214 s; Kuma, 13,239 s. Não são RTO integral: não incluem reconstrução da VPS, recuperação off-site, autenticação ou validação completa dos serviços.

## Pós-teste da produção

Consulta de 16/09/2026 às 22:07:39 UTC (19:07:39 America/Sao_Paulo): 12 serviços Swarm 1/1, SSH/Docker/WireGuard ativos; API Prometheus com três alvos UP e lastError vazio. Nenhum container temporário de restauração restante. Não houve alteração de configuração dos serviços de produção, firewall, VPN ou rotas.

## Correção preparada para aprovação

Manifesto privado `monitor-persistence-candidate-private.yaml` validado por docker stack config. Diferença pretendida: acrescentar os volumes externos guarderia_grafana_data em /var/lib/grafana e guarderia_prometheus_data em /prometheus. O arquivo é candidato de manutenção, não foi aplicado. A validação sintática não comprova ausência de diferenças entre o YAML original do Orion e o serviço ativo; por isso a aplicação deve limitar-se às montagens dos dois serviços, preservando imagens atuais por digest, redes, labels e binds efetivos.

Plano concreto para uma janela de manutenção dos dois serviços:

1. Revalidar tarefas, imagens, espaço livre, backup e configuração atual; preservar SSH/console e confirmar ausência de edição administrativa durante a cópia final.
2. Criar os dois volumes nomeados vazios. Preservar o volume anônimo original do Prometheus e todos os backups; não executar prune.
3. Suspender brevemente as escritas do Grafana, capturar todo /var/lib/grafana incluindo arquivos de journal, e retomar a tarefa em caso de falha da cópia. Recuperar/verificar o SQLite da cópia antes da troca. Nunca remover a tarefa original antes de preservar seu filesystem gravável.
4. Preparar o novo volume Grafana com banco, plugins e arquivos auxiliares, preservando dono/permissões. Validar a cópia isolada. Alterar apenas a montagem do serviço com a imagem atual fixada; verificar saúde e acesso antes de avançar.
5. Parar controladamente apenas o Prometheus, preservando seu volume original. Copiar TSDB completa, incluindo WAL/head, para backup e novo volume; validar a cópia com a imagem atual em ambiente isolado. Acrescentar montagem explícita e iniciar o serviço.
6. Conferir histórico e três alvos UP, integridade do banco Grafana, dashboards/datasources, acesso web e persistência após recriação controlada de cada tarefa. Registrar a lacuna de coleta e os tempos reais; não estimar disponibilidade a partir da porta.
7. Atualizar o manifesto de manutenção e a definição usada no Portainer/Orion para evitar que um redeploy remova as montagens; conferir todas as diferenças antes de qualquer deploy integral da stack.

Impacto previsto: indisponibilidade temporária do Grafana e interrupção da coleta Prometheus durante suas respectivas cópias/trocas; duração ainda não medida. Zabbix, Kuma, SSH e WireGuard não precisam ser reiniciados.

Retorno: Prometheus volta a usar explicitamente seu volume original e a imagem/configuração anteriores. Grafana deve usar volume recuperado da cópia final; docker service rollback sozinho não recupera filesystem de uma tarefa efêmera já removida. Se a cópia ou o pós-teste falhar, não descartar originais nem avançar para o próximo serviço. Retorno da migração de produção ainda não ensaiado.

## Estado e próximos requisitos

BAK-01 passa a parcial: restauração de bancos e cópias Grafana/Kuma ensaiadas, mas recuperação integral, backup TSDB/Portainer/certificados, destino off-site, credenciais de recuperação e RPO/RTO continuam pendentes. OPS-01 e STACK-01 não estão homologados: reiniciar uma cópia isolada não comprova persistência das tarefas de produção. REQ-11/19 permanecem em validação. RB951G segue inacessível ao usuário, sem impedir esta etapa.

## Fontes do procedimento

[Backup PostgreSQL](https://www.postgresql.org/docs/15/backup-dump.html), [API de backup online SQLite](https://www.sqlite.org/backup.html), [backup Grafana](https://grafana.com/docs/grafana/latest/administration/back-up-grafana/) e [armazenamento Prometheus](https://prometheus.io/docs/prometheus/latest/storage/). A orientação de parar Grafana para cópia simples de SQLite não foi aplicada como cópia online; usamos a API transacional SQLite e verificamos a inicialização da cópia. A manutenção final continua exigindo controle de escritas.

Referências locais: [backup/restauração](../05-operations/BACKUP_RESTORE.md), [homologação](HOMOLOGATION.md) e [roadmap](../00-project/ROADMAP.md).
