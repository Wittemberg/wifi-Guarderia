# Plano de rede, endereçamento e interfaces

Revisão de 29/09/2026: LAN por barco e peer direto à VPS sobre 4G. Endereços de campo são reservas propostas, sem implantação. Conferir conflito com redes Docker, LAN administrativa e rede de gerência de cada modem antes de aplicar.

## Redes canônicas

| Rede/endereço | Finalidade | Estado |
|---|---|---|
| `10.250.0.1/32` | Hub WireGuard VPS | Existente |
| `10.250.0.2/32` | RB750r2 central NOC | VPN confirmada em 22/09 |
| `10.250.0.10/32` | Notebook de recuperação | Existente; uso externo/recuperação |
| `10.250.0.101/32` a `10.250.0.120/32` | Peers dos barcos 01–20 | Reservas; uma chave por barco |
| `10.20.1.0/24` a `10.20.20.0/24` | LAN privada de cada barco | Reservas mantidas; gateway `.1` no roteador embarcado |
| `10.21.0.0/24` | LAN administrativa dedicada futura | Reserva; não substituir LAN NOC em uso |
| `172.30.20.0/24`, `172.30.21.0/24` | Redes Docker propostas de coleta e dados | Conferir redes efetivas antes de qualquer alteração |

A LAN NOC operacional e seu NAT/roteamento existentes têm registro próprio em [VPN de borda](../02-implementation/MIKROTIK_WIREGUARD_EDGE.md). Não reendereçá-la nem anunciar a reserva futura automaticamente.

Retirados da topologia ativa: `10.250.0.3/32` (core), `10.20.0.0/24` (gestão da margem), `10.20.240.0/24` (/30 de trânsito), VLAN 10 da margem e VLANs 1001–1020 de transporte. Manter esses blocos indisponíveis para reutilização até conferir ausência de uso real; a retirada documental não remove rotas em produção.

## Atribuição por barco

| Barco | Peer WireGuard | LAN | Gateway LAN |
|---|---|---|---|
| 01 | 10.250.0.101/32 | 10.20.1.0/24 | 10.20.1.1 |
| 02 | 10.250.0.102/32 | 10.20.2.0/24 | 10.20.2.1 |
| 03 | 10.250.0.103/32 | 10.20.3.0/24 | 10.20.3.1 |
| 04 | 10.250.0.104/32 | 10.20.4.0/24 | 10.20.4.1 |
| 05 | 10.250.0.105/32 | 10.20.5.0/24 | 10.20.5.1 |
| 06 | 10.250.0.106/32 | 10.20.6.0/24 | 10.20.6.1 |
| 07 | 10.250.0.107/32 | 10.20.7.0/24 | 10.20.7.1 |
| 08 | 10.250.0.108/32 | 10.20.8.0/24 | 10.20.8.1 |
| 09 | 10.250.0.109/32 | 10.20.9.0/24 | 10.20.9.1 |
| 10 | 10.250.0.110/32 | 10.20.10.0/24 | 10.20.10.1 |
| 11 | 10.250.0.111/32 | 10.20.11.0/24 | 10.20.11.1 |
| 12 | 10.250.0.112/32 | 10.20.12.0/24 | 10.20.12.1 |
| 13 | 10.250.0.113/32 | 10.20.13.0/24 | 10.20.13.1 |
| 14 | 10.250.0.114/32 | 10.20.14.0/24 | 10.20.14.1 |
| 15 | 10.250.0.115/32 | 10.20.15.0/24 | 10.20.15.1 |
| 16 | 10.250.0.116/32 | 10.20.16.0/24 | 10.20.16.1 |
| 17 | 10.250.0.117/32 | 10.20.17.0/24 | 10.20.17.1 |
| 18 | 10.250.0.118/32 | 10.20.18.0/24 | 10.20.18.1 |
| 19 | 10.250.0.119/32 | 10.20.19.0/24 | 10.20.19.1 |
| 20 | 10.250.0.120/32 | 10.20.20.0/24 | 10.20.20.1 |

Fórmula: barco N usa peer `10.250.0.(100+N)/32` e LAN `10.20.N.0/24`, N entre 1 e 20. No hub, associar somente o /32 e a LAN do próprio barco à sua chave. Não cadastrar /16 ou /24 completo de peers como AllowedIPs de uma embarcação.

## WAN, rotas e NAT

| Local | Destino | Caminho proposto |
|---|---|---|
| Roteador N | Default de Internet e endpoint público da VPS | WAN celular de N |
| Roteador N | `10.250.0.1/32`, `.2/32`, `.10/32` | Peer hub; rotas explícitas e ACL de serviços |
| VPS | Peer N e `10.20.N.0/24` | Peer N exclusivo |
| Central NOC/notebook | Peer N/LAN N autorizados | Hub VPS; adicionar rotas junto das ACLs |
| Dispositivos LAN N | Default | Gateway `10.20.N.1` |

Os `.2/.10` acima são endereços `10.250.0.x`. Para administração originada no NOC, preservar o NAT existente para `.2` enquanto essa for a política ativa. Se for adotado roteamento sem NAT, cadastrar somente as origens administrativas reais e suas rotas de retorno; a reserva `10.21.0.0/24` não deve entrar por inferência.

NAT IPv4 apenas na saída Internet de cada kit. Não mascarar LAN N ao entrar na VPN; a proposta de coleta usa SNAT delimitado no host VPS. Se modem separado operar como roteador, registrar a sub-rede de enlace e o NAT adicional, sem sobrepor LAN/VPN/Docker. Bridge/passthrough depende do modelo e de ensaio. Não requerer IP público ou redirecionamento de portas no SIM para o túnel iniciado a bordo.

Não enviar `0.0.0.0/0` ou `::/0` à VPN. AllowedIPs, rotas instaladas e firewall são verificações distintas. A [especificação WireGuard](../02-implementation/WIREGUARD.md) define ida/retorno, SNAT e testes.

## Interfaces e serviços locais

WAN LTE integrada ou porta Ethernet/USB dedicada ao modem, fora da bridge LAN. LAN: Ethernet e WiFi local conforme modelo; porta de recuperação protegida. Não presumir nome de interface, suporte a VLAN ou quantidade de rádios.

Reservas locais: gateway `.1`; central `.10`; câmeras `.20/.21`; sensores IP `.30–.49`; DHCP `.100–.199`. Sensores proprietários ligados à central podem não ter IP. DHCP/DNS apenas nas interfaces locais autorizadas. Rede de visitantes, se oferecida, deve ficar separada do kit e da gerência, com endereçamento próprio aprovado antes de uso.

## Isolamento

Na VPS, negar barco → barco e barco → NOC/painéis; permitir somente administração/coleta autorizadas e retorno rastreado. No kit, negar gerência pela WAN e pela LAN de clientes; liberar somente fontes VPN e serviços necessários. Vincular origens do túnel ao peer correto, testar spoof de LAN alheia e política IPv6. Redes celulares distintas e sub-redes diferentes não comprovam isolamento por si sós.
