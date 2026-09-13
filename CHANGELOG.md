# Histórico de alterações

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
