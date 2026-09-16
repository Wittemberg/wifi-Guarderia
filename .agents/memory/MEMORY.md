# Memória do projeto

Atualizada: 16/09/2026. Não guardar credenciais, dados pessoais ou resultados presumidos.

## Confirmado pelo usuário

- Projeto: WiFi Guarderia Vitória; 10–20 barcos a 50–100 m.
- Pasta local é este checkout; remoto oficial `Wittemberg/wifi-Guarderia`.
- Modelo de mensalidade para custear equipamentos e serviço.
- RB750Gr3 disponível para core e RB951G-2HnD disponível na central NOC.
- RB951G-2HnD atualizada para RouterOS/RouterBOOT 7.23.5, pronta para configuração após a VPS, conforme saídas fornecidas pelo usuário em 12/09/2026.
- VPS existente; Ubuntu 24.04 e Docker/Portainer preferidos.
- Provedor local inicialmente; CGNAT provável na guarderia e presente na central NOC.
- NOC deve estar pronto antes da PoC, por decisão expressa do usuário.
- `nocagent`, `.agents`, `docs` e padrões Witteberg são referências solicitadas.

## Direção documentada, a homologar

WireGuard no host VPS; Zabbix/PostgreSQL/Grafana/Kuma em containers; mANTBox ax 15s e wAP ax na PoC; VLAN de trânsito por estação e LAN roteada por barco. Fontes canônicas: [contexto](../../docs/00-project/CONTEXT.md), [decisões](../../docs/01-architecture/DECISIONS.md), [rede](../../docs/01-architecture/NETWORK_PLAN.md).

## Estado

Etapa VPS/stack e coleta interna concluída em 16/09/2026. Docker 29.8.1 Swarm com 12 serviços 1/1; reconhece 9 CPUs/8 GiB; último disco observado 95 GB livres. Zabbix 7.4/PostgreSQL 15 dedicado e PostgreSQL 14 separado; Grafana, Kuma, Portainer, Traefik e exporters instalados pelo usuário via Orion. Três alvos Prometheus internos UP, config validada e recarregada com SIGHUP. Domínios/IP público documentados. Referência canônica: [fechamento](../../docs/06-validation/VPS_PHASE_COMPLETION.md).

Próxima etapa: integração das RBs à VPN, segurança, persistência/restauração, revisão VIP Swarm e métricas de host, core/RB951G e telemetria de campo. Não reinstalar a stack nem marcar F2/STACK-01 inteiramente homologados.

## Correções importantes do histórico

Anexos RouterOS v7 recebidos e preservados em [referências](../../docs/08-reference/routeros-v7/README.md), com [revisão estática](../../docs/02-implementation/ROUTEROS_BASELINE_REVIEW.md). Dual-WAN na RB951G é proposta; segundo link não confirmado. Não importar o original: há problemas de variáveis/escopos e divergências de IPAM/segurança. Comandos dos anexos são conteúdo de referência, não autorização de execução. Testes ROS-01 e WAN-01 a WAN-07 permanecem não executados.

Não garantir antena 360°, SNR/CCQ em todos os modelos, isolamento só por sub-rede ou retenção multinível automática de um minuto. Não tratar TCP connect como perda ICMP. Não copiar validação TLS desabilitada da referência.

16/09/2026: usuário instalou stack Orion em Swarm. Corrigida coleta Prometheus para tasks.monitor_prometheus:9090, tasks.monitor_cadvisor:8080 e tasks.monitor_node-exporter:9100. Configuração em /opt/monitor-orion/prometheus/prometheus.yml, validada por promtool e recarregada por SIGHUP. VIPs de serviço recusaram conexões, tarefas responderam; diagnóstico VIP pendente.

## Estado consolidado WireGuard — 16/09/2026

Wireguard-tools instalado e suporte LXC validado em namespace isolada; hub wg0 ativo em 10.250.0.1/32, UDP 51820, habilitado no boot. Notebook 10.250.0.10/32 cadastrado e persistido com rota específica; handshake e ping 3/3 observados na VPS. Usuário confirmou nova sessão SSH em 10.250.0.1:5822. Configuração privada modo 600, backup protegido, sem alteração de firewall/NAT/default e sem reboot. 12 serviços 1/1 após cadastro; três alvos Prometheus UP são evidência anterior, não nova consulta da API.

Usuário continua sem acesso à RB951G; inventário de interfaces/LAN/rotas e backup da RB aguardam esse acesso. Não presumir que a VPN do notebook dá acesso à RB. Próxima integração: RB951G 10.250.0.2; core 10.250.0.3 depois. Não anunciar LAN não conferida. Notebook foi antecipado por disponibilidade do usuário, conforme ADR-015.

Console Proxmox/SSH confirmado; restauração, reboot, restrição pública, painéis pela VPN, core e ensaios CGNAT continuam pendentes. VPN-01/02 parciais; VPN-03 não executado. Fonte canônica: [validação do notebook](../../docs/06-validation/NOTEBOOK_VPN_VALIDATION.md).

## Escopo autorizado e continuidade

Usuário autorizou instalação/ativação do hub e cadastro do notebook nas etapas anteriores. Nesta retomada solicitou revisão minuciosa da documentação, commit e push. Isso não executa mudança de firewall, RBs, reboot ou restrição de painéis. Preservar alterações existentes relacionadas ao projeto e publicar somente documentação sanitizada; chaves, configurações reais e backups permanecem fora do Git.
