# Conclusão da etapa VPS e coleta interna

**Estado: concluída em 16/09/2026.** Escopo: inventário da VPS, instalação inicial Orion/Docker/Swarm e serviços NOC, registro dos domínios e correção da coleta complementar Prometheus. A conclusão foi solicitada pelo usuário após a correção. Não equivale a homologação integral de F2, da segurança ou da PoC.

## Entregas e evidências

| Entrega | Evidência |
|---|---|
| Instalação inicial | Usuário informou execução do Setup Orion; Docker 29.8.1 e Swarm ativo observados |
| Serviços | 12 serviços, todos com réplica 1/1 em nova consulta às 03:38:09 UTC de 16/09/2026 |
| Recursos | Docker reconhece 9 CPUs e 8 GiB; última consulta de disco registrou 95 GB livres |
| Aplicações | Zabbix web, Kuma e cAdvisor saudáveis; PostgreSQL 14 e 15 aceitando conexões; Grafana 13.2.2 com banco OK na checagem da sessão |
| Acesso web | Zabbix, Grafana, Kuma e Portainer responderam HTTPS com certificado válido na checagem da sessão; usuário confirmou acesso pelo navegador aos novos domínios de monitoramento |
| Correção Prometheus | Configuração validada por promtool, backup protegido e recarga SIGHUP; três alvos internos UP e lastError vazio na nova consulta |

Horários UTC de última coleta: cAdvisor 03:38:01, Prometheus 03:38:03, Node Exporter 03:38:04 (00:38 no horário America/Sao_Paulo). Fonte: API `/api/v1/targets` do container ativo. Não se trata de teste prolongado ou de reboot.

## Inventário das imagens em execução

Tags e digests abaixo foram lidos dos serviços Swarm. Tags mutáveis ainda precisam ser substituídas por versões de release no manifesto de manutenção; o digest identifica a implantação observada.

| Serviço | Imagem observada |
|---|---|
| `monitor_cadvisor` | `gcr.io/cadvisor/cadvisor:latest@sha256:3de2bd5203120b866d74a9b283b2ffb8ec382fbf9dc321814700c6ea6f44ec57` |
| `monitor_grafana` | `grafana/grafana:latest@sha256:ac461fb352abc50da10a51c7d02462e9c05488f11f53f14b3ad79a8145f638a0` |
| `monitor_node-exporter` | `prom/node-exporter:latest@sha256:1b4e4438faca4dd7e001dd445d161a4a2091b0fededa84093b3a8dfeae1f1be0` |
| `monitor_prometheus` | `prom/prometheus:latest@sha256:5ce7540c3c00ef4ab0c9d2c995c6a5b9c421f44b4a115d97a2c7af3b1c21cbb0` |
| `portainer_agent` | `portainer/agent:latest@sha256:d63bfe57a106070fa5c0e73de0758f33aea018ed3cb6c8610c6663a4ac3a82ba` |
| `portainer_portainer` | `portainer/portainer-ce:latest@sha256:511f3f06c96fe3b993ebeaafde311c1959cae73a7ef825dba6397d51b450dffa` |
| `postgres_postgres` | `postgres:14@sha256:156f0b253fd61366d5fc2107ad45955027d5612f695a8436ce20167f3fa79bff` |
| `traefik_traefik` | `traefik:v3.5.3@sha256:d6be8725d21b45bdd84b93ea01438256e0e3c94aa8fa51834fe87f37cd5d4af8` |
| `uptimekuma_uptimekuma` | `louislam/uptime-kuma:latest@sha256:3d632903e6af34139a37f18055c4f1bfd9b7205ae1138f1e5e8940ddc1d176f9` |
| `zabbix_zabbix-db` | `postgres:15-alpine@sha256:fe0737ba566a2c5b2a28f34433c0a423261900ec17b9bf7ad115e1aae7e57f1b` |
| `zabbix_zabbix-server` | `zabbix/zabbix-server-pgsql:ubuntu-7.4-latest@sha256:f3e692a88221bb14c743843e4d87088bc74af171213e3e09c118f512317e0cc8` |
| `zabbix_zabbix-web` | `zabbix/zabbix-web-nginx-pgsql:ubuntu-7.4-latest@sha256:08d1a160b2e868a457f955d324ede931bc94f4f75529a3c77c052649f99c3c48` |

## Pendências transferidas para a próxima etapa

- WireGuard, rotas e configuração das RBs; testes VPN-01/02/03.
- Segurança: gerência restrita, portas publicadas, rpcbind e teste externo IPv4/IPv6.
- Persistência: conferir banco do Grafana e volume anônimo do Prometheus; testar backup/restauração e reboot/redeploy.
- Investigar IPs virtuais Swarm que recusam conexão; tarefas diretas responderam. Validar escopo de métricas do Node Exporter no LXC.
- Validar templates/alertas Zabbix, integração Grafana/Zabbix e telemetria RF; realizar bancada e campo.
- Registrar versão/hash do instalador Orion e manifesto de manutenção sanitizado. A execução pelo usuário não prova revisão prévia do instalador nem satisfaz retroativamente REQ-07.
- Completar verificação consistente de DNS/TLS dos três novos nomes pelos resolvedores da VPS. A coleta interna deixou de depender deles.

## Referências

[Inventário](../01-architecture/VPS_INVENTORY.md), [DNS](../02-implementation/DOMAINS_AND_DNS.md), [correção e retorno](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md), [roadmap](../00-project/ROADMAP.md) e [homologação](HOMOLOGATION.md).
