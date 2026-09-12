# WireGuard, rotas e acesso administrativo

Estado: desenho implementável após inventário. Não inclui chaves nem comandos de alteração prontos para execução. Endereçamento: [IPAM](../01-architecture/NETWORK_PLAN.md).

## Peers

| Ponta | IP WireGuard | Endpoint remoto | Keepalive proposto |
|---|---|---|---|
| VPS | 10.250.0.1 | Endpoints aprendidos dos clientes | Não necessário como padrão |
| RB951 casa | 10.250.0.2 | IP público/DNS da VPS:51820 | 25 s |
| RB750 core | 10.250.0.3 | IP público/DNS da VPS:51820 | 25 s |
| Notebook recuperação | 10.250.0.10 | VPS:51820 | Conforme NAT e uso |

Gerar par de chaves exclusivo em cada ponta. Nunca reutilizar chave entre core e casa. O keepalive mantém o mapeamento NAT; não prova saúde do caminho. Referência: [WireGuard RouterOS](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard).

## AllowedIPs e roteamento

`AllowedIPs`/`allowed-address` autoriza prefixos de origem e seleciona peer; não substitui firewall nem, no RouterOS, a criação de rotas necessárias. Evitar sobreposição entre peers da mesma interface.

| Configuração local | Peer | Prefixos remotos permitidos |
|---|---|---|
| VPS | Casa | 10.250.0.2/32 e 10.21.0.0/24 |
| VPS | Core | 10.250.0.3/32, 10.20.0.0/24, LANs N ativas e /30 de trânsito ativos |
| VPS | Notebook | 10.250.0.10/32 |
| Casa | VPS/hub | 10.250.0.1/32, .3/32, .10/32 e redes guarderia ativas |
| Core | VPS/hub | 10.250.0.1/32, .2/32, .10/32 e 10.21.0.0/24 |
| Notebook | VPS/hub | 10.250.0.1/32, .3/32 e redes guarderia necessárias |

As abreviações `.2/.3/.10` na tabela significam `10.250.0.x`. Adicionar somente o barco da PoC inicialmente e expandir junto de IPAM/ACLs. Não enviar default `0.0.0.0/0` ou `::/0` para a VPN nesta arquitetura.

## Trânsito da administração

Habilitar forwarding IPv4 no host e permitir somente fluxos da [matriz de segurança](../04-security/SECURITY.md). Fluxo casa → guarderia entra e sai em `wg0` na VPS; precisa de regra de forwarding entre peers. O core deve ter rota de retorno para `10.21.0.0/24`. O wAP usa default do core.

## Containers de coleta

Escolha proposta: SNAT explícito para `10.250.0.1` apenas quando a rede Docker de coleta autorizada alcança redes de gerência da guarderia pela `wg0`. Não NATear tráfego de casa, de retorno ou entre LANs de barcos. Restringir também portas/protocolos e origem do container no firewall antes do SNAT.

Assim o core autoriza a VPS como coletor e não precisa aprender redes Docker. Confirmar por captura controlada/contadores o endereço de origem real: masquerade padrão de Docker não deve ser tomado como contrato. Se a opção mudar para roteamento puro, documentar prefixos Docker em AllowedIPs, rotas e ACLs nos dois lados.

## MTU, DNS e NTP

MTU inicial candidata de 1420, a ajustar por medição de PMTU com a WAN real. Testar datagramas grandes, HTTPS e SNMP, não somente ping pequeno. Se necessário, ajustar MSS de TCP em escopo restrito, após identificar a causa.

Endpoint DNS exige resolução antes de o túnel subir; evitar dependência circular de DNS exclusivamente pela VPN. Configurar NTP no host e RouterOS. Persistir timestamps UTC; painéis exibem America/Sao_Paulo.

## Sequência segura

1. Backup protegido, console e sessão administrativa preservados.
2. Habilitar acesso UDP no host/provedor e criar interface/peers sem alterar a rota default.
3. Configurar casa e core com endpoint, chaves e keepalive.
4. Validar handshake e contadores bidirecionais.
5. Adicionar rotas específicas e testar gerência da VPS ao core.
6. Testar PC na LAN administrativa → core → wAP e retorno.
7. Testar container → alvo e comprovar SNAT pretendido.
8. Aplicar ACLs restritivas e repetir testes positivos e negativos.
9. Reiniciar em janela controlada; confirmar recuperação.

## Testes VPN-01/02/03

- Renovação de IP WAN/CGNAT não exige edição manual do endpoint cliente no hub.
- Falha da casa não afeta guarderia; falha da VPS não altera a saída Internet do core.
- Notebook de recuperação consegue administrar o core se a casa estiver indisponível e a VPS ativa.
- Porta administrativa não responde à Internet pública.
- Reinício de Docker preserva forwarding WireGuard.
- Handshake sem rota funcional é reportado como VPN sem conectividade, não como serviço saudável.

## Recuperação

Notebook também depende da VPS: não é contingência para falha total do hub. Nessa falha, usar console do provedor ou acesso físico à porta administrativa do core. Restaurar pares/chaves do backup protegido ou reprovisionar peers coordenadamente.
