# Histórico de alterações

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
