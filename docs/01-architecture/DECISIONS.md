# Registros de decisão de arquitetura

Data da baseline: 12/09/2026. “Adotado para especificação” significa direção documental, sem homologação implícita de hardware.

## ADR-001 — Reaproveitar infraestrutura disponível

**Status:** confirmado pelo usuário para RBs e VPS. **Contexto:** reduzir desembolso inicial. **Decisão:** RB750Gr3 no core, RB951G na central NOC e VPS existente. **Consequência:** medir CPU, RAM e throughput com firewall, VPN e coleta ativos; substituição somente se a medição demonstrar insuficiência.

## ADR-002 — WireGuard com hub público

**Status:** adotado para especificação. **Contexto:** CGNAT nos dois locais. **Decisão:** peers central NOC/core iniciam túneis até VPS; WireGuard no host. **Alternativas:** conexão IPv6 direta ou CHR. **Consequência:** VPS é ponto único de gerenciamento; Internet local não depende dela. Console e restauração documentados são obrigatórios.

## ADR-003 — Ubuntu 24.04 e Docker/Portainer

**Status:** preferência confirmada; modo de orquestração pendente. **Decisão:** Compose em host único é a baseline proposta. Se a instalação existente/Orion usar Swarm, registrar a opção e gerar manifesto específico antes do deploy. **Consequência:** não misturar semântica de secrets, labels e dependências entre modos.

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
