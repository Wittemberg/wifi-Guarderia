# WireGuard, rotas e acesso administrativo

Evolução consolidada em 17/09/2026: volumes/S3, restrições TCP IPv4, reboot e alertas externos concluídos no escopo testado. [Estado vigente e limites](../00-project/IMPLEMENTATION_STATUS.md). As etapas de equipamentos ainda não executadas permanecem propostas.

Estado em 16/09/2026: execução iniciada por autorização do usuário. wireguard-tools instalado; suporte no LXC e configuração criptográfica testados em namespace isolada. Hub wg0 ativo e habilitado no boot, com notebook de recuperação conectado, ping observado e SSH confirmado pelo usuário; RB750r2 e homologação integral pendentes. Endereçamento proposto: [IPAM](../01-architecture/NETWORK_PLAN.md).

## Peers

| Ponta | IP WireGuard | Endpoint remoto | Keepalive proposto | Estado |
|---|---|---|---|---|
| VPS | 10.250.0.1 | Endpoints aprendidos dos clientes | Não necessário como padrão | ✅ Ativo |
| RB750r2 central NOC | 10.250.0.2 | vpn-guarderia.awecloudsolution.com:51820 | 25 s | ✅ Implementado 22/09/2026 |
| RB750 core | 10.250.0.3 | vpn-guarderia.awecloudsolution.com:51820 | 25 s | ❌ Pendente |
| Notebook recuperação | 10.250.0.10 | vpn-guarderia.awecloudsolution.com:51820 | Conforme NAT e uso | ⚠️ Standby (mantido para uso externo) |

Gerar par de chaves exclusivo em cada ponta. Nunca reutilizar chave entre core e central NOC. O keepalive mantém o mapeamento NAT; não prova saúde do caminho. Referência: [WireGuard RouterOS](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard).

## AllowedIPs e roteamento

`AllowedIPs`/`allowed-address` autoriza prefixos de origem e seleciona peer; não substitui firewall nem, no RouterOS, a criação de rotas necessárias. Evitar sobreposição entre peers da mesma interface.

| Configuração local | Peer | Prefixos remotos permitidos | Estado |
|---|---|---|---|
| VPS | Central NOC | 10.250.0.2/32 e 192.168.15.0/24 | ✅ Implementado |
| VPS | Core | 10.250.0.3/32, 10.20.0.0/24, LANs N ativas e /30 de trânsito ativos | ❌ Pendente |
| VPS | Notebook | 10.250.0.10/32 | ✅ Implementado (standby) |
| Central NOC | VPS/hub | 10.250.0.1/32, .3/32, .10/32 e redes guarderia ativas | ✅ Implementado (.1); demais pendentes |
| Core | VPS/hub | 10.250.0.1/32, .2/32, .10/32 e 10.21.0.0/24 | ❌ Pendente |
| Notebook | VPS/hub | 10.250.0.1/32, .3/32 e redes guarderia necessárias | ✅ Implementado (.1); demais pendentes |

**Nota sobre LAN da central NOC:** o IPAM original reservava 10.21.0.0/24 para LAN administrativa dedicada futura; a LAN operacional real é 192.168.15.0/24, anunciada no peer do MikroTik.

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

### 2. Hub e notebook concluídos; próxima integração na central NOC

- Hub já instalado/configurado, com chaves privadas fora do Git e notebook conectado. Preservar interface/chaves existentes e conferir o inventário antes de acrescentar peers.
- UDP 51820 já alcançado pelo notebook; revisar regras de entrada/encaminhamento necessárias à integração das RBs, preservando SSH. O forwarding IPv4 já estava em 1 após Docker; confirmar o estado e as chains Docker, sem redefinir regras indiscriminadamente.
- Configurar primeiro a RB750r2 da central NOC: VPS `10.250.0.1`, RB750r2 `10.250.0.2`, keepalive proposto 25 s e somente prefixos efetivamente implantados. Não adicionar rota default pela VPN.
- Validar handshake, tráfego bidirecional, rotas de retorno e acesso administrativo em nova sessão. Se a LAN 10.21.0.0/24 ainda não corresponder à rede real, resolver o endereçamento antes de anunciá-la.
- Peer de recuperação do notebook já cadastrado, com SSH à VPS confirmado; testar acesso ao core quando ele existir. Reinício da VPS/RB somente em janela controlada, com console e pós-teste; verificar recuperação da VPN e dos serviços já instalados.

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

O [template recebido](ROUTEROS_BASELINE_REVIEW.md) usa 10.200.0.0/24 e aceita somente o /32 da VPS; isso não substitui a tabela de peers, AllowedIPs e rotas desta especificação. Adaptar ambos antes do import. A porta local UDP 51821 é candidata da RB750r2; o endpoint da VPS continua UDP 51820.

Executar WAN-06 do [plano dual-WAN](NOC_DUAL_WAN.md): falha/retorno de cada WAN, handshake e tráfego real central NOC→VPS→core, com verificação de retorno. Medir recuperação e efeito em sessões existentes; keepalive de 25 s não estabelece SLA de recuperação.

## Critérios de saída e estado atual

| Marco | Evidência exigida | Estado |
|---|---|---|
| Notebook e VPS conectados | Handshake, ping e nova sessão SSH | Validado no escopo notebook ↔ VPS; ver registro abaixo |
| VPS e RB750r2 conectadas | Handshake recente, tráfego bidirecional, rotas e nova sessão administrativa funcionando | Pendente |
| Recuperação | Console confirmado e retorno ao estado anterior descrito/testado no escopo da mudança | Parcial: console e retorno após reboot da VPS validados; rollback integral e equipamentos de campo pendentes |
| Core integrado | Central NOC e coletor alcançam alvos autorizados, com retorno e origem de coleta confirmados | Pendente |
| Gerência restrita | Acesso positivo pela VPN e negativo de origem externa autorizada, incluindo portas diretas | VPS validada por TCP IPv4, inclusive após reboot; equipamentos e UDP/IPv6 externo pendentes |
| Continuidade | Reinício e falhas controladas preservam/recuperam serviços, com tempos medidos | Reboot da VPS validado; cenários de falha das RBs e recuperação integral pendentes |

Se perder acesso, usar console e restaurar somente o conjunto alterado a partir do backup; verificar SSH, rotas, serviços e coleta. Não remover regras ou reiniciar a stack às cegas. Parar a expansão de peers enquanto o marco anterior estiver reprovado.

Persistência Grafana/Prometheus e reboot foram validados; diagnóstico dos VIPs Swarm e abrangência das métricas de host continuam pendentes. [Estado vigente](../00-project/IMPLEMENTATION_STATUS.md).

## Histórico: execução inicial — 16/09/2026

- Instalado pacote Ubuntu wireguard-tools 1.0.20210914-1ubuntu4, sem atualizar/remover outros pacotes.
- Criada interface WireGuard temporária em namespace isolada; configuração de chave e porta 51820 aceita pelo kernel. Nenhuma interface WireGuard ficou ativa no host.
- DNS vpn-guarderia.awecloudsolution.com conferido: CNAME para vps-guarderia e A 204.157.108.99.
- Backup privado de firewall IPv4/IPv6, rotas, regras e inventário de serviços salvo antes de alterações de rede.
- Chave da VPS gerada e configuração de hub com 10.250.0.1/32, MTU 1420 e UDP 51820 preparada fora do Git; sem peers enquanto faltar chave pública da RB750r2.
- Usuário confirmou acesso SSH e painel Proxmox; acesso à RB750r2 e LAN real indisponíveis no momento. Após essa confirmação, o hub foi ativado sem peers; rotas da central NOC e firewall permanecem sem alteração.

A configuração preparada não configura LAN, rota default, NAT ou encaminhamento entre peers. Na expansão de peers, adicionar somente rota/AllowedIPs necessários após conferência. Evidências e segredos estão no diretório privado wireguard-preflight da VPS. Referência de procedimento: [guia oficial WireGuard](https://www.wireguard.com/quickstart/).

## Histórico: hub ativado inicialmente sem peers — 16/09/2026

- Console SSH/Proxmox confirmado pelo usuário; acesso à RB750r2 e LAN atual ainda indisponíveis.
- Serviço wg-quick@wg0 ativo e habilitado no boot, endereço 10.250.0.1/32, MTU 1420 e UDP 51820. Configuração em /etc/wireguard/wg0.conf com permissão 600; chave privada fora do Git.
- Nesse marco inicial, ainda sem peers, handshake ou rotas de LAN. Políticas e regras IPv4/IPv6 e tabela de rotas main comparadas antes/depois e preservadas. INPUT já estava ACCEPT; nenhuma liberação adicional foi necessária no host. Naquele marco, firewall do provedor e alcance UDP externo ainda não estavam comprovados; o alcance a partir do notebook foi confirmado no marco seguinte.
- Pós-teste: SSH e Docker ativos, 12 serviços Swarm 1/1 e três alvos Prometheus UP/sem erro.
- Primeira ativação revertida automaticamente porque a comparação incluía dados variáveis do iptables-save; segunda ativação validada comparando regras sem timestamps/contadores. O teste comprovou parada da interface, não recuperação após reboot.
- Retorno específico: systemctl disable --now wg-quick@wg0 remove a interface e desabilita sua ativação no boot; preservar configuração/chaves privadas para diagnóstico. Não restaurar todo o firewall Docker quando nenhuma regra foi alterada.

Próximo passo da RB750r2, com inventário recebido em 21/09/2026: confirmar backup e recuperação local, gerar chave do peer na própria RB, trocar somente chaves públicas e configurar primeiro o trânsito 10.250.0.1 ↔ 10.250.0.2. Só anunciar LAN depois de confirmar a faixa real. VPN-01/02 estão parciais pelo notebook; VPN-03 continua pendente.


## Estado atual — VPN de borda implementada em 22/09/2026

A RB750r2 da central NOC foi integrada como **gateway VPN de borda**, substituindo a topologia de cliente direto no notebook. Toda a LAN local (192.168.15.0/24) agora acessa a VPS através do túnel WireGuard configurado no MikroTik, com NAT masquerade e roteamento validados.

**Peers ativos:**
- **VPS hub (10.250.0.1):** servidor central
- **MikroTik RB750r2 (10.250.0.2):** gateway VPN de borda para a LAN 192.168.15.0/24 — ✅ ativo e validado
- **Notebook (10.250.0.10):** mantido em standby; usado quando fora da rede local

**Validações concluídas:**
- ✅ Handshake WireGuard ativo entre MikroTik e VPS
- ✅ Ping da LAN local para VPS (10.250.0.1)
- ✅ SSH da LAN local para VPS porta 5822
- ✅ Acesso aos painéis web (Portainer) da LAN local após atualização de IP allowlist do Traefik
- ✅ Backup das configurações MikroTik e VPS

**Documentação detalhada:** [VPN de borda no MikroTik](MIKROTIK_WIREGUARD_EDGE.md)

**Pendências:**
- Core da guarderia (RB750Gr3, peer 10.250.0.3)
- Forwarding entre peers na VPS (NOC → core)
- Rotas de retorno no core
- Coleta Zabbix via VPN com SNAT
- Testes de failover dual-WAN

## Estado da central NOC em 21/09/2026

Inventário completo de recursos e rede recebido: RB750r2 r3, RouterOS/RouterBOOT 7.23.7, gateway básico em uso. As indisponibilidades de acesso descritas nos registros datados de 16/09 não representam o estado desta coleta. WireGuard da RB permanece ausente. Usar o hub existente e preservar o peer do notebook; confirmar backup, recuperação local e ACLs antes de adicionar o novo peer. LAN administrativa dedicada continua proposta; não anunciar a LAN operacional automaticamente. Ver [inventário](../01-architecture/NOC_ROUTER_INVENTORY.md).
