# WireGuard, rotas e acesso administrativo

Estado em 16/09/2026: próxima etapa planejada após conclusão da instalação da stack. WireGuard ainda não instalado/configurado/homologado. Esta entrega documenta o plano; não executa alterações na VPS ou nas RBs. Endereçamento proposto: [IPAM](../01-architecture/NETWORK_PLAN.md).

## Peers

| Ponta | IP WireGuard | Endpoint remoto | Keepalive proposto |
|---|---|---|---|
| VPS | 10.250.0.1 | Endpoints aprendidos dos clientes | Não necessário como padrão |
| RB951 central NOC | 10.250.0.2 | vpn-guarderia.awecloudsolution.com:51820 | 25 s |
| RB750 core | 10.250.0.3 | vpn-guarderia.awecloudsolution.com:51820 | 25 s |
| Notebook recuperação | 10.250.0.10 | vpn-guarderia.awecloudsolution.com:51820 | Conforme NAT e uso |

Gerar par de chaves exclusivo em cada ponta. Nunca reutilizar chave entre core e central NOC. O keepalive mantém o mapeamento NAT; não prova saúde do caminho. Referência: [WireGuard RouterOS](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard).

## AllowedIPs e roteamento

`AllowedIPs`/`allowed-address` autoriza prefixos de origem e seleciona peer; não substitui firewall nem, no RouterOS, a criação de rotas necessárias. Evitar sobreposição entre peers da mesma interface.

| Configuração local | Peer | Prefixos remotos permitidos |
|---|---|---|
| VPS | Central NOC | 10.250.0.2/32 e 10.21.0.0/24 |
| VPS | Core | 10.250.0.3/32, 10.20.0.0/24, LANs N ativas e /30 de trânsito ativos |
| VPS | Notebook | 10.250.0.10/32 |
| Central NOC | VPS/hub | 10.250.0.1/32, .3/32, .10/32 e redes guarderia ativas |
| Core | VPS/hub | 10.250.0.1/32, .2/32, .10/32 e 10.21.0.0/24 |
| Notebook | VPS/hub | 10.250.0.1/32, .3/32 e redes guarderia necessárias |

As abreviações `.2/.3/.10` na tabela significam `10.250.0.x`. Adicionar somente o barco da PoC inicialmente e expandir junto de IPAM/ACLs. Não enviar default `0.0.0.0/0` ou `::/0` para a VPN nesta arquitetura.

## Trânsito da administração

Habilitar forwarding IPv4 no host e permitir somente fluxos da [matriz de segurança](../04-security/SECURITY.md). Fluxo central NOC → guarderia entra e sai em `wg0` na VPS; precisa de regra de forwarding entre peers. O core deve ter rota de retorno para `10.21.0.0/24`. O wAP usa default do core.

## Containers de coleta

Escolha proposta: SNAT explícito para `10.250.0.1` apenas quando a rede Docker de coleta autorizada alcança redes de gerência da guarderia pela `wg0`. Não NATear tráfego da central NOC, de retorno ou entre LANs de barcos. Restringir também portas/protocolos e origem do container no firewall antes do SNAT.

Assim o core autoriza a VPS como coletor e não precisa aprender redes Docker. Confirmar por captura controlada/contadores o endereço de origem real: masquerade padrão de Docker não deve ser tomado como contrato. Se a opção mudar para roteamento puro, documentar prefixos Docker em AllowedIPs, rotas e ACLs nos dois lados.

## MTU, DNS e NTP

MTU inicial candidata de 1420, a ajustar por medição de PMTU com a WAN real. Testar datagramas grandes, HTTPS e SNMP, não somente ping pequeno. Se necessário, ajustar MSS de TCP em escopo restrito, após identificar a causa.

Endpoint DNS exige resolução antes de o túnel subir; evitar dependência circular de DNS exclusivamente pela VPN. Configurar NTP no host e RouterOS. Persistir timestamps UTC; painéis exibem America/Sao_Paulo.

## Sequência segura

### 1. Preparação da VPS e recuperação

- Confirmar console do provedor e preservar uma sessão SSH na porta 5822; testar acesso de recuperação antes de restringir gerência.
- Criar backup protegido das regras de firewall, rede e configurações afetadas; nas RBs, backup e export privados. Registrar versão e plano de retorno.
- Verificar suporte efetivo a WireGuard e permissões no LXC antes da instalação. A ausência de `/dev/net/tun` não é prova isolada de incompatibilidade; o funcionamento de Docker não comprova suporte ao túnel.
- Conferir rede real da central NOC, rotas e sobreposições com Docker/VPN/LANs antes de aplicar o IPAM proposto.
- Revalidar resolução de `vpn-guarderia.awecloudsolution.com` fora da VPN. Endpoint proposto: UDP 51820.

### 2. Hub na VPS e primeiro peer na central NOC

- Instalar/configurar WireGuard no host e preparar interface e chaves exclusivas, guardadas fora do Git. Registrar versões e configuração sanitizada.
- Preparar regras de entrada/encaminhamento no host e no provedor, liberando UDP 51820 e preservando SSH. O forwarding IPv4 já estava em 1 após Docker; confirmar o estado e as chains Docker, sem redefinir regras indiscriminadamente.
- Configurar primeiro a RB951G da central NOC: VPS `10.250.0.1`, RB951G `10.250.0.2`, keepalive proposto 25 s e somente prefixos efetivamente implantados. Não adicionar rota default pela VPN.
- Validar handshake, tráfego bidirecional, rotas de retorno e acesso administrativo em nova sessão. Se a LAN 10.21.0.0/24 ainda não corresponder à rede real, resolver o endereçamento antes de anunciá-la.
- Preparar/testar peer de recuperação quando disponível. Reinício da VPS/RB somente em janela controlada, com console e pós-teste; verificar recuperação da VPN e dos serviços já instalados.

### 3. Core da guarderia e coleta pela VPN

- Após validar VPS ↔ central NOC, conferir inventário/backup da RB750Gr3 e adicioná-la como peer `10.250.0.3`.
- Habilitar somente redes de gerência e do barco da PoC necessárias, com rotas de retorno e ACLs explícitas. Não anunciar redes futuras por conveniência.
- Testar central NOC → core → wAP e retorno; testar coletor → alvo e comprovar SNAT/origem real conforme a seção de containers.
- Verificar que falha da central NOC ou da VPS não altera a saída Internet local da guarderia.

### 4. Restrições administrativas e encerramento

- Com acesso via VPN comprovado, restringir painéis e portas de monitoramento à administração autorizada; conferir caminhos pelo IP público, proxy e portas diretas, em IPv4/IPv6.
- Revalidar coleta Prometheus interna, serviços e regras após mudanças e restart Docker em janela controlada.
- Registrar resultados em VPN-01/02/03, SEC-03/04 e OPS-01. A implantação do primeiro peer não aprova os testes que dependem do core, recuperação ou falhas.
- Concluir em paralelo a revisão de persistência, backups e restauração; eles continuam necessários para homologar F2/STACK-01 integralmente.

## Testes VPN-01/02/03

- Renovação de IP WAN/CGNAT não exige edição manual do endpoint cliente no hub.
- Falha da central NOC não afeta guarderia; falha da VPS não altera a saída Internet do core.
- Notebook de recuperação consegue administrar o core se a central NOC estiver indisponível e a VPS ativa.
- Porta administrativa não responde à Internet pública.
- Reinício de Docker preserva forwarding WireGuard.
- Handshake sem rota funcional é reportado como VPN sem conectividade, não como serviço saudável.

## Recuperação

Notebook também depende da VPS: não é contingência para falha total do hub. Nessa falha, usar console do provedor ou acesso físico à porta administrativa do core. Restaurar pares/chaves do backup protegido ou reprovisionar peers coordenadamente.

## Ensaio com duas WANs na central NOC

O [template recebido](ROUTEROS_BASELINE_REVIEW.md) usa 10.200.0.0/24 e aceita somente o /32 da VPS; isso não substitui a tabela de peers, AllowedIPs e rotas desta especificação. Adaptar ambos antes do import. A porta local UDP 51821 é candidata da RB951G; o endpoint da VPS continua UDP 51820.

Executar WAN-06 do [plano dual-WAN](NOC_DUAL_WAN.md): falha/retorno de cada WAN, handshake e tráfego real central NOC→VPS→core, com verificação de retorno. Medir recuperação e efeito em sessões existentes; keepalive de 25 s não estabelece SLA de recuperação.

## Critérios de saída desta próxima etapa

| Marco | Evidência exigida | Estado |
|---|---|---|
| VPS e RB951G conectadas | Handshake recente, tráfego bidirecional, rotas e nova sessão administrativa funcionando | Pendente |
| Recuperação | Console confirmado e retorno ao estado anterior descrito/testado no escopo da mudança | Pendente |
| Core integrado | Central NOC e coletor alcançam alvos autorizados, com retorno e origem de coleta confirmados | Pendente |
| Gerência restrita | Acesso positivo pela VPN e negativo de origem externa autorizada, incluindo portas diretas | Pendente |
| Continuidade | Reinício e falhas controladas preservam/recuperam serviços, com tempos medidos | Pendente |

Se perder acesso, usar console e restaurar somente o conjunto alterado a partir do backup; verificar SSH, rotas, serviços e coleta. Não remover regras ou reiniciar a stack às cegas. Parar a expansão de peers enquanto o marco anterior estiver reprovado.

Persistência do Grafana/Prometheus, diagnóstico dos VIPs Swarm e abrangência das métricas de host continuam pendências da etapa NOC, conforme [fechamento anterior](../06-validation/VPS_PHASE_COMPLETION.md).
