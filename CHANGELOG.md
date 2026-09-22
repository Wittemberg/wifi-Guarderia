# Histórico de alterações

## Aceite funcional do gateway — 2026-09-21

- Usuário confirmou navegação atual pela RB750r2 e operação plena como gateway; NOC-02 atualizado para aceite funcional, preservando o escopo separado de VPN/failover.

## 0.1.3 — 2026-09-21

- Inventário atual da central NOC: RB750r2 (hEX lite) r3, RouterOS/RouterBOOT 7.23.7, recursos e configuração básica de gateway.
- Análise de WAN1, LAN/DHCP/DNS, NAT, firewall e serviços; testes ICMP registrados com limites de evidência.
- Arquitetura, requisitos, integração incremental, riscos e homologação alinhados à configuração em uso. Coletas brutas mantidas fora do Git.

## Revisão de consistência documental — 2026-09-17

- Corrigidos resumos que ainda marcavam restrições, reboot ou alertas como pendentes; consolidados memória, roadmap, requisitos, riscos, homologação e procedimentos.
- Criado estado único de acompanhamento, mantendo registros históricos identificados e pendências reais separadas. Conjunto revisado para publicação autorizada, sem nova implantação nesta revisão.


## Alertas de backup implantados — 2026-09-17

- Implantados monitor externo, heartbeat e canais SES/Telegram; dez testes locais e ensaios integrados aprovados.
- Permissões corrigidas e automação ativada após testes. Usuário confirmou alertas e recuperação nos dois canais; primeira avaliação automática saudável observada.


## Reboot validado — 2026-09-16

- Preparados inventário anterior, verificador automático e plano de recuperação para reboot autorizado da VPS; pré-testes e retorno local aprovados após novo boot, com SSH VPN confirmado; testes externos TCP IPv4 e scripts VPN pós-reboot aprovados; logins nos quatro consoles confirmados pelo usuário; aceite funcional concluído.


## Restrições de infraestrutura — 2026-09-16

- Auditado Swarm de um nó, dependências RPC/NFS e cadastro Zabbix.
- Aplicados filtros públicos de infraestrutura e novas sessões SSH, com preservação de sessões existentes; nova sessão VPN e console confirmados e reversão automática cancelada. Aceite externo TCP IPv4 e acesso VPN aprovados conforme saída do notebook; UDP, IPv6 externo e reboot pendentes.


## Restrições dos painéis — 2026-09-16

- Aplicadas restrições por origem aos sete routers e filtro persistente nas quatro portas diretas de monitoramento; manifestos locais e Portainer reconciliados.
- Preservados os contêineres, doze serviços e três alvos UP; exceção de NAT local limitada ao Prometheus para manter o datasource Grafana.
- Incluídos procedimentos Windows, retorno operacional e unidade do filtro no backup; teste externo IPv4 e HTTPS pela VPN aprovados conforme saída do notebook; logins pós-mudança nos quatro consoles confirmados pelo usuário.


## 0.2.2 — 2026-09-16

- Instalado e ativado o hub WireGuard no host LXC, com backup protegido e console confirmado.
- Cadastrado o notebook de recuperação com rota /32 e configuração persistida; handshake e ping observados, SSH pela VPN confirmado pelo usuário.
- Consolidada a documentação do projeto, removendo estados superados e separando implantação, medição e aceite humano; adicionado registro canônico de validação do notebook.
- Atualizados requisitos, decisões, IPAM, riscos, inventários, procedimentos, segurança, backups, roadmap e homologação.
- RB951G permanece inacessível ao usuário; sua integração depende de inventário/backup e antecede o core. Reboot, restauração, gerência pública e rede de campo continuam pendentes.

## 0.2.1 — 2026-09-16

- Documentada a próxima etapa WireGuard: hub VPS, RB951G primeiro, core depois e endpoint DNS explícito.
- Detalhados pré-requisitos LXC/rede, backup/console, validação, retorno e restrições administrativas.
- Atualizados roadmap, requisitos, decisão, homologação e memória; implantação VPN permanece pendente.


## 0.2.0 — 2026-09-16

- Concluída a etapa VPS/stack e coleta interna; atualizados roadmap, inventário, especificações, memória e homologação com pendências explícitas.
- Registrados os 12 serviços 1/1, imagens/digests e três alvos UP em nova consulta às 03:38 UTC.
- Corrigida coleta Prometheus para endereços internos das tarefas Swarm, com backup, validação promtool e recarga por SIGHUP.
- Registrada falha dos IPs virtuais como pendência independente.


## Não publicado — 2026-09-15

- Registrados inventário parcial medido da VPS e seus limites: LXC, recursos visíveis, serviços, portas e firewall. Gateway e detalhes operacionais mantidos fora do Git; IP público de destino DNS documentado.
- Documentados domínio awecloudsolution.com, aliases CNAME propostos e critérios de acesso/DNS/TLS.
- Atualizados preparação, stack, requisitos, decisão, pendências, índice, memória e VPS-01; sem implantação presumida. Publicação DNS confirmada pelo usuário e resolução A/CNAME medida na VPS; política de dados ajustada para IP público publicado.


## 0.1.2 — 2026-09-12

- Arquivados os dois anexos RouterOS v7 recebidos, preservando bytes e hashes SHA-256.
- Documentados achados de sintaxe, escopo, IPAM, WireGuard, firewall e repetição do import.
- Incorporada proposta de WAN primária/backup para a central NOC, com requisitos, pendências, procedimento e testes rastreáveis.
- Nenhum script importado ou equipamento alterado; o original permanece referência não homologada.

## 0.1.1 — 2026-09-12

### Adicionado

- Estimativa informada pelo usuário de aporte de aproximadamente R$ 3.000,00 para aquisição dos equipamentos básicos e início dos testes da PoC, registrada no README.
- Inventário sanitizado da RB951G-2HnD: RouterOS 7.23.5 (long-term), RouterBOOT 7.23.5 e recursos fornecidos pelo usuário; pronta para configuração após a VPS.

### Alterado

- Padronizada a denominação “central NOC” para o local administrativo, inclusive topologia, rotas, procedimentos e memória.
- Atualizados roadmap, pendências e homologação para refletir o inventário recebido sem presumir configuração ou testes de VPN.

## 0.1.0 — 2026-09-12

### Adicionado

- Baseline documental de contexto, requisitos, arquitetura, rede, equipamentos e alimentação.
- Especificação de VPS, Docker/Portainer, WireGuard e provisionamento MikroTik.
- Plano de monitoramento, alertas, persistência, backup e operação.
- Plano de PoC, matriz de homologação e modelos de evidência.
- Dimensionamento paramétrico de custos e escopo dos serviços.
- Orientações locais para agentes e adaptação dos padrões Witteberg.
- Análise rastreável do `nocagent` no commit `e5ce6e3f9a84ca368472f771ef54f72e824b5a7c`.

### Limites desta versão

Nenhum equipamento foi configurado, nenhuma VPS foi alterada e nenhuma medição de campo foi realizada. Versões exatas dos serviços, domínio, segredos, dados do provedor e homologação permanecem registrados como pendências.

## Em andamento — persistência e backups, 2026-09-16

- Auditados volumes; confirmados riscos de persistência Grafana/Prometheus.
- Criados backups locais privados, restaurados PostgreSQL 15/14 e testadas cópias Grafana/Kuma em isolamento, incluindo reinício.
- Preparado manifesto de volumes, sem aplicação à produção. BAK-01 parcial; migração, backup integral e off-site pendentes.
- [Relatório e plano](docs/06-validation/PERSISTENCE_BACKUP_AUDIT.md).

## 16/09/2026 — Persistência e backup automático

- Registrada migração dos volumes Grafana/Prometheus e reconciliação do manifesto Portainer.
- Implementados backup local AES-256, hashes, retenção, status de falha e agendamento diário.
- Testadas restauração isolada de quatro aplicações e PostgreSQL 14/15, validação de sete certificados e rejeição de arquivo corrompido.
- Preparado envio S3 ao destino informado; permissões AWS, custódia externa da chave e homologação de recuperação integral pendentes.

## 16/09/2026 — Cópia externa S3 ativada

- Permissões AWS corrigidas pelo usuário; arquivo enviado e baixado com SHA-256 correspondente.
- Restauração isolada de aplicações/bancos e validação de certificados a partir do S3 concluídas.
- Envio diário habilitado após os testes; cópia externa da chave confirmada pelo usuário.
- Retenção/versionamento S3, teste da chave externa e recuperação integral seguem pendentes.


## 16/09/2026 — Retenção S3 e consolidação documental

- Registrada expiração da versão atual em sete dias configurada pelo usuário; HeadObject confirma previsão de expiração no backup e recibo. Leitura integral do lifecycle negada; exclusão futura ainda não ensaiada.
- Separadas retenção local 7 diários/4 semanais/3 mensais, janela externa de sete dias e retenção de métricas.
- Corrigidos estados superados nos resumos, contexto, inventário, riscos, requisitos, decisões e homologação; preservados os registros históricos da implantação e auditoria.
- Preparado plano de auditoria de exposição e validação dos painéis pela VPN como próximo passo independente da RB951G. Nenhum firewall/proxy foi alterado nesta revisão.
