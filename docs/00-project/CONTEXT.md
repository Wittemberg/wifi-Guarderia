# Contexto consolidado

Direção atualizada em 29/09/2026 por instrução do usuário. Origem inicial: conversa [Viabilidade Wifi Guarderia](https://chatgpt.com/c/6aa1e0b2-2ae8-83e9-9db1-c2d15a7da5ba), com acesso dependente da conta; decisões posteriores e registros locais prevalecem. Não reproduzir dados pessoais de terceiros.

## Problema e serviço

Segurança para 10–20 embarcações fundeadas, originalmente descritas a 50–100 m da margem. Alternativas solicitadas: alarme com central, três contatos sem fio, duas sirenes e sinalizador; alarme com câmeras interna/externa e aplicativo; e serviço com empresa de vigilância. Alimentação, autonomia, preventiva, visitas e mensalidade sustentável seguem em estudo.

## Confirmado pelo usuário — mudança de 29/09/2026

A dificuldade de posicionar antenas e passar infraestrutura ao longo da costa levou à substituição da topologia: não haverá central em terra distribuindo Internet por antenas. Cada barco terá modem 4G e chip próprios. A operação poderá fornecer os chips para obter gestão individual de banda/linhas pelo contrato da operadora escolhida. Vivo é a provável candidata, sem escolha definitiva.

A central NOC administrativa e a VPS permanecem como gestão/monitoramento já existentes; não são a central de distribuição terrestre retirada. Nenhuma compra, contratação, ativação de chip ou alteração de equipamento decorre desta revisão documental.

## Evolução das escolhas

| Tema | Desenho substituído | Direção vigente |
|---|---|---|
| Internet | Provedor fixo compartilhado na margem | Linha 4G própria por barco |
| Distribuição | RB750Gr3 + mANTBox + enlace 5 GHz | Retirada da topologia |
| Kit de rede | wAP ax cliente 5 GHz/AP 2,4 GHz obrigatório | Modem/roteador 4G; WiFi local integrado ou separado conforme seleção |
| VPN | Core de campo concentra LANs | Peer individual por barco até VPS, como proposta técnica |
| Gestão de banda | Filas no core/WAN compartilhada | Recursos contratuais da linha e filas locais, conforme suporte/testes |
| PoC | 50/100 m e rotação no enlace terrestre | Cobertura celular no fundeio, horários, movimento, dados, energia e reconexão |
| Custos | Base compartilhada e rádios | Modem/linha por barco e NOC compartilhado |

REQ-02/03 e RF-01 a RF-05 originais ficam substituídos; decisões antigas continuam rastreáveis em [ADRs](../01-architecture/DECISIONS.md) e Git.

## Proposta técnica e pendências

Cada barco mantém LAN exclusiva, saída Internet local e túnel de gerência iniciado sobre 4G. A VPS aplica ACL entre peers; alarme e gravação permanecem locais. Modelo, APN, bandas, capacidade, cobertura, consumo elétrico e franquia ainda serão medidos. CGNAT/IP variável devem ser ensaiados, não contornados com gerência pública.

Distinguir franquia, velocidade e priorização: fornecer um chip não garante API, limite individual de velocidade ou controle instantâneo. Contratar e testar cada recurso. Chips do proprietário são modalidade possível, com limites de controle documentados. [Conectividade e linhas](../02-implementation/CELLULAR_CONNECTIVITY.md).

## Contexto preservado e estado operacional

Usuário tem experiência com MikroTik, Intelbras, TP-Link e algum UniFi. RB750Gr3 está disponível, sem obrigação de uso como core; RB750r2 da central NOC opera como gateway, com VPN funcional confirmada em 22/09/2026. Dual-WAN NOC segue proposta sem segundo link confirmado. [Inventário](../01-architecture/NOC_ROUTER_INVENTORY.md).

VPS Ubuntu 24.04, Swarm/Portainer e stack NOC instalados; coleta interna, notebook VPN, restrições TCP IPv4, reboot, backup criptografado local/S3 e alertas SES/Telegram têm evidências datadas. [Estado e limites](IMPLEMENTATION_STATUS.md). Recuperação integral e homologação celular não foram concluídas.

O usuário definiu preparar monitoramento antes da PoC. Pasta local e repositório oficial devem ser preservados; nocagent/Witteberg são referências seletivas. Os [anexos RouterOS](../08-reference/routeros-v7/README.md) permanecem fontes históricas, sem autorização de importação ou reset. Valores operacionais e segredos ficam fora do Git.

## Próxima etapa

Selecionar e cotar kit/plano candidatos, levantar cobertura real e preparar bancada com coleta. Em paralelo, preparar recuperação integral da VPS em ambiente separado. Não repetir etapas já comprovadas sem causa. [Roadmap](ROADMAP.md) e [pendências](RISKS_AND_OPEN_ITEMS.md).
