# Memória do projeto

Atualizada: 12/09/2026. Não guardar credenciais, dados pessoais ou resultados presumidos.

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

Baseline documental 0.1.0 com atualização de inventário informada pelo usuário em 12/09/2026. RB951G da central NOC atualizada e aguardando configuração da VPS; VPN ainda não configurada/homologada. Próxima fase: preparar a VPS, conferir o inventário do core e configurar a RB951G. Usar sempre “central NOC” para o local administrativo, distinguindo-o dos serviços de monitoramento hospedados na VPS. Consultar [homologação](../../docs/06-validation/HOMOLOGATION.md) antes de informar prontidão.

## Correções importantes do histórico

Não garantir antena 360°, SNR/CCQ em todos os modelos, isolamento só por sub-rede ou retenção multinível automática de um minuto. Não tratar TCP connect como perda ICMP. Não copiar validação TLS desabilitada da referência.
