# Coleta interna do Prometheus

Evolução consolidada em 17/09/2026: volumes/S3, restrições TCP IPv4, reboot e alertas externos concluídos no escopo testado. [Estado vigente e limites](../00-project/IMPLEMENTATION_STATUS.md). As etapas de equipamentos ainda não executadas permanecem propostas.

Data: 16/09/2026. Correção autorizada pelo usuário após instalação da stack pelo Setup Orion. Escopo: alvos do Prometheus, validação e recarga, sem mudança de firewall, rede Swarm ou domínios públicos.

## Configuração aplicada

Fonte persistente no host: `/opt/monitor-orion/prometheus/prometheus.yml`, montada em `/etc/prometheus/prometheus.yml`. Mantidos job `prometheus`, intervalo de 15 s, timeout de 10 s e caminho `/metrics` para preservar filtros existentes.

| Componente | Alvo interno |
|---|---|
| Prometheus | `tasks.monitor_prometheus:9090` |
| cAdvisor | `tasks.monitor_cadvisor:8080` |
| Node Exporter | `tasks.monitor_node-exporter:9100` |

A coleta usa HTTP na rede interna. Os domínios públicos permanecem para acesso web; a coleta não depende mais de sua resolução pública ou certificados.

Os aliases de serviço `prometheus`, `cadvisor` e `node-exporter` resolveram para IPs virtuais, mas recusaram conexões nas portas internas. Os nomes `tasks.monitor_*` responderam diretamente nas tarefas. A causa dos IPs virtuais permanece pendente de diagnóstico; esta correção não homologa a rede Swarm inteira.

## Aplicação e recuperação

Backup protegido fora do Git em `prometheus-20260916T033456Z.yml.bak` preserva a configuração original. O arquivo `prometheus-20260916T033608Z.yml.bak` preserva a etapa intermediária com aliases de serviço. Ambos estão no diretório privado de evidências da VPS.

Configuração candidata e arquivo ativo passaram em `promtool check config`. O arquivo bind-mounted foi escrito preservando o inode; recarga por SIGHUP, sem reiniciar a stack. Para retorno, restaurar o backup original no mesmo arquivo, validar com promtool e enviar SIGHUP ao container ativo; repetir a consulta de alvos.

Os três serviços têm uma réplica nesta implantação. Antes de escalar, adotar descoberta de todas as tarefas e revisar labels/series; um hostname em alvo estático não comprova coleta de todas as réplicas. Regeneração da configuração pelo Orion deve preservar estes alvos.

## Limites

Coleta UP não valida a abrangência das métricas do host pelo Node Exporter, persistência do Grafana/Prometheus, restrições externas, VPN ou telemetria RF. O resultado de coleta não deve ser usado como evidência desses pontos. Posteriormente, a persistência de Grafana/Prometheus e a restauração isolada S3 receberam [validação própria](../06-validation/BACKUP_AUTOMATION.md); abrangência do host e campo seguem pendentes; restrições TCP IPv4 foram posteriormente validadas em ensaio separado, conforme o estado consolidado.

## Resultado medido

API `/api/v1/targets` consultada após a recarga: os três alvos internos apresentaram `health=up` e `lastError` vazio. Últimas coletas observadas: 16/09/2026 03:36:31–34 UTC (00:36:31–34 America/Sao_Paulo).
