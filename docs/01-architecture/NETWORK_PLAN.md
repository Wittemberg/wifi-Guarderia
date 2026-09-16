# Plano de rede, endereçamento e interfaces

Estado: endereços de VPN/LAN/VLAN abaixo continuam reservados em projeto. Docker Swarm já foi instalado com redes overlay interna/ingress e bridges locais; conferir sobreposições antes de aplicar este IPAM. A instalação da stack não comprova implantação destas reservas nem isolamento IPv6.

## Redes canônicas

| Rede | Finalidade | Gateway/atribuições |
|---|---|---|
| `10.250.0.0/24` | WireGuard de gerenciamento | VPS `.1`, central NOC `.2`, core `.3`, notebook de recuperação `.10` reservado |
| `10.21.0.0/24` | LAN administrativa dedicada atrás da RB951 | RB951 `.1`; PC `.10` reservado |
| `10.20.0.0/24` | Gerenciamento fixo da guarderia, VLAN 10 | Core `.1`; mANTBox `.10`; switch `.11` se houver |
| `10.20.1.0/24` a `10.20.20.0/24` | LAN privada de cada barco | wAP `.1` na respectiva LAN |
| `10.20.240.0/24` | Pool dividido em /30 de trânsito RF | Um /30 e uma VLAN por estação |
| `172.30.20.0/24` | Rede Docker de coleta proposta | Zabbix server `.10`; IPs devem ser reservados no manifesto |
| `172.30.21.0/24` | Rede Docker de dados proposta | PostgreSQL acessível somente aos serviços autorizados |

O restante de `10.20.0.0/16` não está atribuído. Usar somente prefixos realmente ativos nas ACLs e AllowedIPs; um resumo /16, se adotado em rotas futuras, deve ter descarte para sub-redes não atribuídas.

## Trânsito por barco

A VLAN é atribuída no AP à estação cadastrada; o wAP opera em `station` roteado e recebe o trânsito como acesso sem tag. O uplink AP–core transporta VLANs tagged. Esta combinação precisa ser validada no RouterOS/pacote real. Não transportar a bridge LAN do barco sobre o rádio.

| Barco | VLAN trânsito | Rede /30 | Core | WAN wAP | LAN |
|---|---:|---|---|---|---|
| 01 | 1001 | 10.20.240.0/30 | 10.20.240.1 | 10.20.240.2 | 10.20.1.0/24 |
| 02 | 1002 | 10.20.240.4/30 | 10.20.240.5 | 10.20.240.6 | 10.20.2.0/24 |
| 03 | 1003 | 10.20.240.8/30 | 10.20.240.9 | 10.20.240.10 | 10.20.3.0/24 |
| 04 | 1004 | 10.20.240.12/30 | 10.20.240.13 | 10.20.240.14 | 10.20.4.0/24 |
| 05 | 1005 | 10.20.240.16/30 | 10.20.240.17 | 10.20.240.18 | 10.20.5.0/24 |
| 06 | 1006 | 10.20.240.20/30 | 10.20.240.21 | 10.20.240.22 | 10.20.6.0/24 |
| 07 | 1007 | 10.20.240.24/30 | 10.20.240.25 | 10.20.240.26 | 10.20.7.0/24 |
| 08 | 1008 | 10.20.240.28/30 | 10.20.240.29 | 10.20.240.30 | 10.20.8.0/24 |
| 09 | 1009 | 10.20.240.32/30 | 10.20.240.33 | 10.20.240.34 | 10.20.9.0/24 |
| 10 | 1010 | 10.20.240.36/30 | 10.20.240.37 | 10.20.240.38 | 10.20.10.0/24 |
| 11 | 1011 | 10.20.240.40/30 | 10.20.240.41 | 10.20.240.42 | 10.20.11.0/24 |
| 12 | 1012 | 10.20.240.44/30 | 10.20.240.45 | 10.20.240.46 | 10.20.12.0/24 |
| 13 | 1013 | 10.20.240.48/30 | 10.20.240.49 | 10.20.240.50 | 10.20.13.0/24 |
| 14 | 1014 | 10.20.240.52/30 | 10.20.240.53 | 10.20.240.54 | 10.20.14.0/24 |
| 15 | 1015 | 10.20.240.56/30 | 10.20.240.57 | 10.20.240.58 | 10.20.15.0/24 |
| 16 | 1016 | 10.20.240.60/30 | 10.20.240.61 | 10.20.240.62 | 10.20.16.0/24 |
| 17 | 1017 | 10.20.240.64/30 | 10.20.240.65 | 10.20.240.66 | 10.20.17.0/24 |
| 18 | 1018 | 10.20.240.68/30 | 10.20.240.69 | 10.20.240.70 | 10.20.18.0/24 |
| 19 | 1019 | 10.20.240.72/30 | 10.20.240.73 | 10.20.240.74 | 10.20.19.0/24 |
| 20 | 1020 | 10.20.240.76/30 | 10.20.240.77 | 10.20.240.78 | 10.20.20.0/24 |

Fórmula para barco N: VLAN = 1000 + N; último octeto da rede = 4 × (N − 1); core = base + 1; wAP = base + 2. Não reutilizar /30 de embarcação ativa.

## Rotas e NAT

| Equipamento | Destino | Próximo salto |
|---|---|---|
| wAP N | Default | IP core do /30 correspondente |
| Core | LAN N /24 | WAN wAP N |
| Core | 10.21.0.0/24, 10.250.0.1/32, .2/32 e .10/32 | WireGuard/hub |
| Core | Default | Gateway real do provedor |
| Central NOC | Prefixos de guarderia ativos e peers de gerência | WireGuard/hub |
| Central NOC | Default | Gateway existente da central NOC |
| VPS | Redes guarderia ativas | Peer core |
| VPS | 10.21.0.0/24 | Peer central NOC |

Sem NAT no wAP. No core, masquerade apenas das redes autorizadas quando a saída for WAN; não aplicar na VPN. Na central NOC, NAT apenas para Internet, preservando origem administrativa na VPN. O prefixo existente da central NOC não é exportado por padrão: PC usa a LAN administrativa dedicada. O acesso a essa LAN por um PC já na central NOC depende de rota adicional ou conexão física à RB951.

## Mapeamento físico proposto

| Equipamento | Porta lógica | Função |
|---|---|---|
| RB750Gr3 | ether1 | WAN provedor, fora da bridge LAN |
| RB750Gr3 | ether2 | Trunk tagged VLAN 10 e VLANs 1001–1020 ativas |
| RB750Gr3 | ether3 | Acesso local VLAN 10 para recuperação física |
| RB750Gr3 | ether4/5 | Reservadas/desabilitadas conforme necessidade |
| mANTBox | Ethernet | Trunk, gerência somente VLAN 10 |
| mANTBox | Rádio 5 GHz | AP, associação cadastra VLAN de trânsito |
| mANTBox | Rádio 2,4 GHz | Desabilitado na PoC |
| wAP | Rádio 5 GHz | Cliente roteado de trânsito |
| wAP | Rádio 2,4 GHz + Ethernet LAN | Bridge LAN privada; confirmar portas reais |

Não assumir `wifi1` como 5 GHz. Identificar banda/rádio pelo inventário. Ether1 do wAP pode alimentar via PoE e pertencer à LAN se o uplink é exclusivamente rádio; etiquetar para evitar ligações em redes externas.

## Serviços da LAN embarcada

Gateway `.1`; central `.10`; câmeras `.20` e `.21`; sensores IP `.30–.49`; pool DHCP `.100–.199`. São reservas propostas, não dispositivos descobertos. Sensores proprietários sem fio não recebem IP individual se conectados somente à central. DHCP/DNS local no wAP; DNS recursivo não deve escutar no rádio ou WAN pública.

## Isolamento e alternativa

No AP, validar a VLAN efetivamente atribuída a cada cliente e isolamento de estações. No core, rejeitar origem incompatível com a VLAN de entrada antes de aceitar encaminhamento. No wAP, rejeitar gerência vinda da LAN de clientes. No trunk, rejeitar tags não autorizadas e quadros sem tag fora da porta de recuperação.

Se VLAN por estação não funcionar com autenticação e firmware escolhidos, a PoC de um barco pode continuar fisicamente isolada; expansão multicliente fica bloqueada até ADR de alternativa testada. Não substituir silenciosamente por bridge compartilhada. Credencial individual forte e teste de troca de MAC/VLAN são condições para homologar segregação.

## Variante dual-WAN da central NOC

A [proposta recebida](../02-implementation/NOC_DUAL_WAN.md) reserva ether1/ether2 da RB951G para WAN1/WAN2 e ether3–5 para LAN administrativa, sujeita a inventário. Nessa variante, a default única é substituída por defaults recursivas com prioridades distintas. O mapeamento ether2 trunk do core permanece válido.

As redes 192.168.50.0/24 e 10.200.0.0/24 do anexo são exemplos divergentes, não novas reservas. Preservar as redes canônicas acima; IPs das WANs e pool DHCP administrativo dependem de confirmação. Ver [reconciliação](../02-implementation/ROUTEROS_BASELINE_REVIEW.md).
