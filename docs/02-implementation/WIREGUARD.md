# WireGuard, rotas e acesso administrativo

Revisão de 29/09/2026: preservar hub, notebook e VPN da RB750r2 existentes; adicionar futuramente um peer por barco sobre a própria WAN 4G. O peer de core terrestre foi retirado da expansão planejada. Esta revisão não alterou peers, rotas ou firewall em execução.

Evidências: [notebook](../06-validation/NOTEBOOK_VPN_VALIDATION.md), [VPN de borda NOC](MIKROTIK_WIREGUARD_EDGE.md) e [alcance reverso da LAN NOC](../06-validation/NOC_EDGE_VPN_VALIDATION.md). O último registro tem escopo próprio; não equivale a homologar isolamento, coleta e recuperação integral. [IPAM de destino](../01-architecture/NETWORK_PLAN.md).

## Peers e origem das conexões

| Ponta | IP do túnel | Endpoint | Estado |
|---|---|---|---|
| VPS | `10.250.0.1/32` | Aprende endpoints dos clientes | Existente |
| RB750r2 central NOC | `10.250.0.2/32` | `vpn-guarderia.awecloudsolution.com:51820` | VPN confirmada em 22/09 |
| Notebook | `10.250.0.10/32` | Mesmo hub | Mantido para recuperação/uso externo |
| Barco N (01–20) | `10.250.0.(100+N)/32` | Mesmo hub | Proposto; chave exclusiva por barco |

Cada barco inicia a conexão UDP a partir da rede celular. CGNAT e IP variável devem ser ensaiados no plano contratado; não exigir porta entrante/IP público no barco. Keepalive de 25 s é ponto inicial de teste sob NAT, com consumo contabilizado; não é sonda de saúde. Fonte consultada em 29/09/2026: [WireGuard Quick Start](https://www.wireguard.com/quickstart/).

## AllowedIPs, rotas e retorno propostos

| Configuração local | Peer | Prefixos admitidos |
|---|---|---|
| VPS | Barco N | Somente `10.250.0.(100+N)/32` e `10.20.N.0/24` |
| Barco N | Hub | `10.250.0.1/32`, `10.250.0.2/32`, `10.250.0.10/32` como origens de gerência autorizadas |
| Central NOC/notebook | Hub | Peers e LANs de barcos autorizados, além dos destinos existentes |
| VPS | NOC/notebook | Preservar configuração existente e conferir origens reais antes da expansão |

Criar rotas correspondentes nos equipamentos; não supor que mudar AllowedIPs instala rotas em todos os sistemas. AllowedIPs seleciona peer e valida origem, mas não substitui ACL. Evitar sobreposição entre peers. No RouterOS, conferir rotas explícitas conforme [documentação oficial](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard), consultada em 29/09/2026.

Não anunciar outros barcos ao peer N nem default `0.0.0.0/0`/`::/0` na VPN. A Internet local e o endpoint público usam a WAN celular. Os clientes da LAN retornam pela default para o roteador N, que encaminha respostas administrativas ao hub.

A central NOC tem NAT para `.2` no caminho registrado. Preservá-lo nesta revisão; `.2` representa o gateway, não identidade individual do operador. Caso se adote roteamento da LAN administrativa sem NAT, revisar origens/retorno e ACLs nos barcos e no hub como mudança separada. Não usar a reserva `10.21.0.0/24` como rede ativa.

## Encaminhamento e coleta

Administração NOC/notebook → barco entra e sai por `wg0` no hub. Liberar somente fontes, destinos e serviços aprovados. Negar barco → barco, barco → LAN NOC e barco → painéis/gerência do host; aceitar apenas retornos rastreados e fluxos explicitamente necessários. Fazer a mesma restrição no input/forward do kit. O hub já existente precisa dessa revisão antes de receber clientes embarcados.

Para containers, a proposta é SNAT restrito da rede real do coletor para `10.250.0.1` ao acessar alvos autorizados pela `wg0`. Filtrar origem, destino e serviço antes do SNAT; verificar por contadores/captura controlada. Não aplicar masquerade genérico na VPN dos barcos. Esse SNAT não encaminha navegação ou vídeo contínuo pela VPS.

## MTU, DNS e reconexão

1420 é MTU inicial candidata, não valor validado para o plano 4G. Medir PMTU e testar tráfego maior, HTTPS e aplicações; ajustar MSS só após diagnóstico e em escopo limitado. DNS do endpoint e sincronização de horário devem funcionar antes do túnel. Registrar timestamps UTC.

Testar mudança de IP celular, perda/retorno de cobertura, reinício do modem/roteador e indisponibilidade do hub; exigir restabelecimento sem intervenção normal e sem alterar identidade. Repetição deve ser limitada, com backoff quando suportado; não reiniciar continuamente o modem por ausência de handshake.

## Sequência segura de expansão

1. Preservar evidências e caminhos existentes. Inventariar configuração efetiva, backup, console da VPS e recuperação local do kit. Não reiniciar `wg0` pelo próprio túnel sem console.
2. Aprovar linha/modelo e acesso 4G em bancada; cadastrar um barco no IPAM.
3. Gerar chave na ponta, cadastrar somente seu /32 e LAN no hub, e instalar rotas/ACLs com comparação do antes/depois.
4. Testar VPS → peer → LAN e retorno; testar NOC/notebook → barco apenas nos serviços autorizados. Confirmar origem real do coletor.
5. Executar testes negativos com segundo peer de laboratório: tráfego lateral, spoof, acesso ao NOC e exposição pública IPv4/IPv6. Não adicionar sub-rede inteira de barcos à allowlist dos painéis.
6. Executar falhas/recuperação, persistência e revogação de um peer sem afetar os demais. Confirmar Internet local com hub indisponível.
7. Em falha, remover/restaurar somente as entradas da mudança usando backup; preservar NOC/notebook, registrar resultado e acesso recuperado.

Aceite por VPN-01/02/03, CEL-06 e SEC-01/02/03/04 na [homologação](../06-validation/HOMOLOGATION.md). Evidência de notebook/NOC não libera automaticamente nenhum barco.
