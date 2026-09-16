# Registros de decisão de arquitetura

Data da baseline: 12/09/2026. “Adotado para especificação” significa direção documental, sem homologação implícita de hardware.

## ADR-001 — Reaproveitar infraestrutura disponível

**Status:** confirmado pelo usuário para RBs e VPS. **Contexto:** reduzir desembolso inicial. **Decisão:** RB750Gr3 no core, RB951G na central NOC e VPS existente. **Consequência:** medir CPU, RAM e throughput com firewall, VPN e coleta ativos; substituição somente se a medição demonstrar insuficiência.

## ADR-002 — WireGuard com hub público

**Status:** adotado para especificação. **Contexto:** CGNAT nos dois locais. **Decisão:** peers central NOC/core iniciam túneis até VPS; WireGuard no host. **Alternativas:** conexão IPv6 direta ou CHR. **Consequência:** VPS é ponto único de gerenciamento; Internet local não depende dela. Console e restauração documentados são obrigatórios.

## ADR-003 — Ubuntu 24.04 e Docker/Portainer

**Status:** implementado em 16/09/2026. **Decisão:** Docker Swarm instalado pelo usuário via Orion, substituindo a proposta inicial Compose. Serviços e digests registrados no fechamento da etapa; manifesto de manutenção e testes de persistência pendentes. **Consequência:** não misturar semântica de secrets, labels e dependências entre modos.

## ADR-004 — Coleta antes do rádio em campo

**Status:** confirmado pelo usuário. **Decisão:** Zabbix/PostgreSQL, Grafana e Kuma antes da PoC. **Alternativa descartada nesta fase:** testar e instalar observabilidade depois. **Consequência:** maior preparo inicial, com evidências desde o primeiro ensaio.

## ADR-005 — Dois rádios no wAP ax

**Status:** candidato à PoC. **Decisão:** 5 GHz cliente e 2,4 GHz AP local; mANTBox como base. **Consequência:** simplifica kit e alimentação, porém não comprova cobertura em toda orientação. Reprovação RF pode exigir reposicionamento ou outro conjunto de antenas.

## ADR-006 — Roteamento por barco e trânsito segregado

**Status:** proposta de engenharia desta baseline. **Decisão:** LAN /24 por barco, trânsito /30 em VLAN atribuída por estação, sem NAT no wAP. **Contexto:** gerência direta e defesa contra tráfego lateral. **Consequência:** rotas e ACLs devem ser criadas em conjunto. Compatibilidade e autenticação por estação são gate de laboratório.

## ADR-007 — Separar vídeo e NOC

**Status:** adotado para especificação. **Decisão:** gravação embarcada e acesso sob demanda. **Consequência:** VPS não dimensionada como NVR/relay de vídeo; nuvem do fabricante pode consumir upload e franquia e deve ser medida.

## ADR-008 — Métricas por capacidade e origem

**Status:** baseline corporativa adaptada. **Decisão:** sem dados inventados; campos não suportados têm estado próprio; cada medição registra origem e tempo. **Consequência:** SNR/CCQ indisponível não bloqueia sozinho a PoC se perda, RSSI, taxa e aplicação forem medidos; a lacuna fica explícita.

## ADR-009 — Automação restrita e integração opcional

**Status:** adotado para especificação. **Decisão:** recuperação de processos é determinística; alterações de rede não são autoexecutadas por IA nesta fase. NOC-Agent começa futuramente por leitura. **Consequência:** disponibilidade não depende de LLM/Chatwoot; sem copiar runtime ou stack do repositório de referência.

## ADR-010 — Evidências protegidas e Git documental

**Status:** adotado para especificação. **Decisão:** repositório recebe documentos e futuros templates sanitizados; arquivos reais e chaves ficam em armazenamento privado. **Consequência:** hash e identificador permitem rastrear evidência sem publicar dados de clientes. A retenção depende da classificação.

## ADR-011 — Capacidade e custos são hipóteses mensuráveis

**Status:** adotado para especificação. **Decisão:** dimensionamento inicial da conversa é ponto de partida; aprovação exige carga real, retenção e orçamento. **Consequência:** não converter número de barcos em garantia de capacidade nem preços históricos em cotação vigente.

## ADR-012 — Avaliar redundância WAN da central NOC

**Status:** proposta, dependente de inventário e laboratório. **Contexto:** anexos fornecidos pelo usuário descrevem duas WANs estáticas e recuperação recursiva. **Decisão proposta:** WAN1 preferencial e WAN2 backup na RB951G, com duas sondas por WAN, sem scripts que desabilitem defaults. Preservar o IPAM e separar essa atribuição de portas da RB750Gr3. **Alternativa:** manter uma WAN enquanto não houver segundo link confirmado. **Consequência:** adaptar sintaxe, segurança e rotas VPN antes de importar; medir recuperação de sessões e WireGuard. Trata-se de comportamento determinístico do roteamento, não de ação por IA. Ver [especificação e testes](../02-implementation/NOC_DUAL_WAN.md).

## ADR-013 — Domínio e aliases da Guarderia

**Data:** 15/09/2026. **Status:** domínio awecloudsolution.com e preferência por CNAME confirmados; nomes publicados pelo usuário e resolução A/CNAME conferida na VPS (TTL 300 s). **Decisão:** um A para vps-guarderia e aliases por serviço com sufixo guarderia, conforme [plano DNS](../02-implementation/DOMAINS_AND_DNS.md). **Consequência:** centralizar mudança de IP, manter administração restrita pela VPN e validar DNS, proxy e TLS separadamente.

## ADR-014 — Coleta Prometheus pela rede interna

Em 16/09/2026, adotados os nomes DNS das tarefas Swarm para coleta dos três serviços de monitoramento, removendo dependência de DNS público/TLS. IPs virtuais recusaram conexão; tarefas responderam. Ver [procedimento](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md). Diagnóstico da rede virtual permanece pendente.
