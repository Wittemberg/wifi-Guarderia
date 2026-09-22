# WireGuard no MikroTik RB750r2 — VPN de Borda

Estado em 22/09/2026: WireGuard configurado e validado na RB750r2 (hEX lite) da central NOC como gateway VPN de borda. A topologia migrou de VPN cliente-servidor direta (notebook → VPS) para VPN de borda (LAN → MikroTik → VPS), permitindo que toda a rede local acesse a infraestrutura remota sem cliente individual.

## Topologia implementada

**Antes (16/09/2026):**
```
Notebook (10.250.0.10) ←→ VPS (10.250.0.1)
    └─ túnel WireGuard direto
```

**Agora (22/09/2026):**
```
LAN Local (192.168.15.0/24)
    └─ Notebook, desktops, dispositivos
         ↓
    MikroTik RB750r2 (10.250.0.2) ←→ VPS (10.250.0.1)
         └─ túnel WireGuard na borda
```

## Peers ativos

| Ponta | IP WireGuard | Endpoint remoto | Keepalive | Estado |
|---|---|---|---|---|
| VPS hub | 10.250.0.1 | Aprendido dos clientes | Não | ✅ Ativo |
| MikroTik RB750r2 | 10.250.0.2 | vpn-guarderia.awecloudsolution.com:51820 | 25s | ✅ Ativo |
| Notebook recuperação | 10.250.0.10 | vpn-guarderia.awecloudsolution.com:51820 | Conforme uso | ⚠️ Standby |

O peer do notebook permanece configurado mas inativo quando na LAN local; será usado quando o notebook estiver fora da rede base.

## Configuração do MikroTik RB750r2

### Interface WireGuard

```routeros
/interface wireguard
add listen-port=31923 mtu=1420 name=wg-VPS private-key="<chave_privada_gerada>"

/interface wireguard peers
add allowed-address=10.250.0.1/32,10.250.0.3/32,10.250.0.10/32,192.168.15.0/24 \
    comment="VPS Hub WireGuard" \
    endpoint-address=vpn-guarderia.awecloudsolution.com \
    endpoint-port=51820 \
    interface=wg-VPS \
    persistent-keepalive=25s \
    public-key="VNMJ7imaMMELxUmoIaLn4UpOXCOrW6TBZxesq0pB7Ec="
```

**Parâmetros críticos:**
- `listen-port=31923`: porta UDP local aleatória alta (não conflita com padrão 51820)
- `endpoint-port=51820`: porta UDP do servidor VPS
- `persistent-keepalive=25s`: mantém mapeamento NAT ativo
- `allowed-address`: inclui `192.168.15.0/24` para aceitar tráfego da LAN local

### Endereço IP

```routeros
/ip address
add address=10.250.0.2/32 interface=wg-VPS network=10.250.0.2
```

### Rota estática

```routeros
/ip route
add dst-address=10.250.0.1/32 gateway=wg-VPS
```

### NAT masquerade

```routeros
/ip firewall nat
add action=masquerade chain=srcnat comment="NAT LAN para VPN WireGuard" \
    out-interface=wg-VPS
```

**Razão:** a LAN local usa endereços privados 192.168.15.0/24; ao atravessar o túnel, o tráfego é mascarado para 10.250.0.2 (IP do MikroTik na VPN).

### Firewall — Forward

```routeros
/ip firewall filter
add action=accept chain=forward comment="Permitir LAN acessar VPN WireGuard" \
    out-interface=wg-VPS place-before=0 src-address=192.168.15.0/24
```

**Posição:** `place-before=0` coloca a regra no topo, antes de qualquer drop padrão.

## Configuração da VPS

### Peer do MikroTik

```bash
wg set wg0 peer CK79CNjGAECiyl9bW8gfPMFEtDTNmVf+FbA1nTxpgDo= \
    allowed-ips 10.250.0.2/32,192.168.15.0/24
```

**AllowedIPs críticos:**
- `10.250.0.2/32`: aceita tráfego do próprio MikroTik
- `192.168.15.0/24`: associa a LAN NOC ao peer do MikroTik e permite que `wg-quick` instale a rota Linux de retorno pela `wg0`; o tráfego LAN → VPS chega normalmente mascarado como `10.250.0.2`

A configuração está persistida em `/etc/wireguard/wg0.conf`. O serviço `wg-quick@wg0` está habilitado e instala a rota `192.168.15.0/24 dev wg0` durante a subida. Não adicionar `PostUp`/`PreDown` para a mesma rota, pois isso duplica a rota derivada de `AllowedIPs`.

Ao alterar um peer ativo com `wg set`, lembrar que o comando atualiza o WireGuard, mas não cria rotas na tabela Linux. Para uma alteração sem reinício, instalar e validar a rota separadamente; para persistência, atualizar o arquivo e testar a subida por console fora de banda.

### Firewall e forwarding

O host VPS já tinha:
```bash
net.ipv4.ip_forward = 1  # Ativado por Docker
```

Não foram necessárias alterações adicionais no firewall da VPS; INPUT já estava ACCEPT e o forwarding entre peers do WireGuard é permitido.

## Restrições de acesso aos painéis

Os serviços web (Portainer, Grafana, Zabbix, Kuma) executam em Docker Swarm atrás do Traefik como proxy reverso. O Traefik aplica **middleware de IP allowlist** por origem.

### Problema inicial

Após configurar o WireGuard no MikroTik, o acesso aos painéis retornava **HTTP 403 Forbidden** porque:
- Tráfego da LAN (192.168.15.0/24) era mascarado para `10.250.0.2`
- A allowlist do Traefik só incluía `10.250.0.10/32` (notebook), `10.250.0.1/32` (VPS) e o IP público

### Solução aplicada

Atualização do label do serviço Portainer (exemplo):

```bash
docker service update portainer_portainer \
  --label-add 'traefik.http.middlewares.guarderia-portainer.ipallowlist.sourcerange=\
10.250.0.1/32,10.250.0.2/32,10.250.0.10/32,192.168.15.0/24,204.157.108.99/32'
```

**IPs permitidos:**
- `10.250.0.1/32`: VPS (loopback via túnel)
- `10.250.0.2/32`: MikroTik (origem do tráfego mascarado da LAN)
- `10.250.0.10/32`: Notebook via VPN direta (quando fora da base)
- `192.168.15.0/24`: LAN completa (caso tráfego chegue sem masquerade em cenários futuros)
- `204.157.108.99/32`: IP público da VPS (acesso local/console)

A mesma atualização deve ser aplicada aos demais serviços (Grafana, Zabbix frontend, Kuma) conforme necessário.

## Validação executada

### 1. Handshake WireGuard

**MikroTik:**
```routeros
/interface wireguard peers print detail
# last-handshake=49s
# rx=1812 tx=4988
```

**VPS:**
```bash
wg show wg0
# peer: CK79CNjGAECiyl9bW8gfPMFEtDTNmVf+FbA1nTxpgDo=
#   endpoint: 179.48.69.206:31923
#   allowed ips: 10.250.0.2/32, 192.168.15.0/24
#   latest handshake: 1 minute, 32 seconds ago
#   transfer: 136.24 KiB received, 58.23 KiB sent
```

✅ Handshake ativo e tráfego bidirecional confirmado.

### 2. Conectividade ICMP

**Do notebook na LAN local:**
```bash
ping 10.250.0.1
# PING 10.250.0.1: 56 data bytes
# 64 bytes from 10.250.0.1: icmp_seq=0 ttl=64 time=42 ms
```

✅ Ping responde através do túnel.

**Da VPS para a LAN NOC:**

O primeiro teste para o NVR `192.168.15.110` falhou porque a VPS ainda encaminhava esse prefixo pela interface pública. Após instalar e persistir a rota pela `wg0`, o teste retornou 3/3 respostas, 0% de perda e RTT médio de 25,262 ms. A rota foi novamente observada após reinicialização. Consulte a [validação do alcance reverso](../06-validation/NOC_EDGE_VPN_VALIDATION.md).

### 3. SSH via VPN

**Do notebook na LAN local:**
```bash
ssh -p 5822 root@10.250.0.1
# Conexão SSH estabelecida
```

✅ Acesso SSH funcional via túnel de borda.

### 4. Acesso aos painéis web

**Após atualização da allowlist:**
```
https://portainer-guarderia.awecloudsolution.com/
```

✅ Portainer acessível da LAN local sem forbidden.

## Cenários de uso

### Cenário 1: Usuário na LAN local (central NOC)

- **Dispositivos:** notebooks, desktops, tablets na 192.168.15.0/24
- **Gateway:** MikroTik RB750r2 faz NAT e encaminha tráfego VPN
- **Cliente WireGuard:** não necessário nos dispositivos
- **Rota:** LAN → MikroTik (10.250.0.2) → VPS (10.250.0.1)

### Cenário 2: Notebook externo (fora da base)

- **Dispositivo:** notebook com cliente WireGuard instalado
- **Peer:** 10.250.0.10 conecta diretamente à VPS
- **Rota:** Notebook → Internet → VPS (10.250.0.1)
- **Uso:** acesso administrativo remoto quando fora da central NOC

### Cenário 3: Futuro — Core da guarderia

- **Peer:** RB750Gr3 (10.250.0.3) será adicionado
- **Rota central NOC → core:** PC → MikroTik (10.250.0.2) → VPS (10.250.0.1) → Core (10.250.0.3)
- **Coleta:** containers na VPS acessarão dispositivos da guarderia via SNAT para 10.250.0.1

## Limitações e pendências

| Item | Estado | Observação |
|---|---|---|
| VPN de borda na central NOC | ✅ Implementado | MikroTik RB750r2 |
| Roteamento LAN → VPS | ✅ Implementado | NAT + firewall |
| Acesso a painéis da LAN | ✅ Implementado | Allowlist atualizada |
| Peer do notebook | ⚠️ Standby | Mantido para uso externo |
| Peer do core (RB750Gr3) | ❌ Pendente | Aguarda configuração |
| Forwarding VPS entre peers | ❌ Pendente | Necessário para NOC → core |
| Rota VPS → LAN NOC | ✅ Implementado | `192.168.15.0/24 dev wg0`; NVR 192.168.15.110 respondeu após reboot |
| Rotas de retorno no core | ❌ Pendente | Core futuro precisa conhecer as redes administrativas autorizadas |
| Coleta Zabbix via VPN | ❌ Pendente | SNAT e alvos autorizados |
| Testes de failover WAN | ❌ Pendente | Dual-WAN NOC ainda não configurado |

## Segurança e isolamento

### Princípios aplicados

1. **Allowlist por IP de origem:** Traefik restringe acesso aos painéis apenas a IPs VPN autorizados
2. **Roteamento reverso controlado:** a VPS possui rota para `192.168.15.0/24` via peer do MikroTik; o NVR respondeu a ICMP originado na VPS. Portanto, não presumir isolamento unidirecional — restringir acessos VPS → LAN por firewall conforme a política desejada
3. **Persistência de peers:** peer do notebook permanece configurado mas inativo; não é deletado
4. **Chaves privadas:** nunca expostas em logs, repositório ou transmissão não criptografada

### Melhorias futuras

- [ ] Implementar firewall na VPS para controlar tráfego entre peers (NOC ↔ core)
- [ ] Adicionar logging de conexões VPN para auditoria
- [ ] Configurar alertas de handshake perdido (peer offline)
- [ ] Testar rotação de chaves WireGuard
- [ ] Implementar ACLs granulares por serviço (ex: NOC acessa Portainer, mas não SSH do core)

## Recuperação e rollback

### Backup da configuração

**MikroTik:**
```routeros
/export file=backup-wireguard-20260922
```

Arquivo gerado: `backup-wireguard-20260922.rsc` (salvo localmente e em evidências privadas)

**VPS:**
```bash
wg-quick save wg0
cp /etc/wireguard/wg0.conf /root/guarderia-backups/wg0.conf.20260922
```

### Procedimento de rollback

**Remover WireGuard do MikroTik:**
```routeros
/interface wireguard peers remove [find interface=wg-VPS]
/interface wireguard remove wg-VPS
/ip address remove [find interface=wg-VPS]
/ip route remove [find gateway=wg-VPS]
/ip firewall nat remove [find comment~"VPN WireGuard"]
/ip firewall filter remove [find comment~"VPN WireGuard"]
```

**Remover peer da VPS:**
```bash
wg set wg0 peer CK79CNjGAECiyl9bW8gfPMFEtDTNmVf+FbA1nTxpgDo= remove
wg-quick save wg0
```

**Reativar cliente no notebook** (se necessário):
```bash
wg-quick up wg0
```

## Comandos de diagnóstico

### MikroTik

```routeros
# Status da interface
/interface wireguard print detail

# Peers e handshake
/interface wireguard peers print detail

# Rotas VPN
/ip route print where gateway=wg-VPS

# Regras NAT
/ip firewall nat print where out-interface=wg-VPS

# Regras firewall
/ip firewall filter print where out-interface=wg-VPS

# Conexões ativas através da VPN
/ip firewall connection print where connection-mark=wg-VPS
```

### VPS

```bash
# Status do túnel
wg show wg0

# Peers e tráfego
wg show wg0 peers

# Rotas instaladas
ip route show | grep wg0

# Conferir decisão de rota para a LAN NOC
ip route get 192.168.15.110

# Forwarding habilitado
sysctl net.ipv4.ip_forward

# Conexões ativas
ss -tunap | grep wg0
```

### Cliente (notebook na LAN)

```bash
# Testar conectividade
ping -c 3 10.250.0.1

# Testar SSH
ssh -p 5822 root@10.250.0.1

# Traçar rota
traceroute 10.250.0.1

# Ver rota efetiva
ip route get 10.250.0.1
```

## Referências

- [MikroTik WireGuard Documentation](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard)
- [WireGuard Protocol](https://www.wireguard.com/)
- [Plano de rede canônico](../01-architecture/NETWORK_PLAN.md)
- [WireGuard hub inicial](WIREGUARD.md)
- [Inventário RB750r2](../01-architecture/NOC_ROUTER_INVENTORY.md)

## Histórico de execução

### 22/09/2026 — Implementação inicial

1. ✅ Desativado cliente WireGuard no notebook (mantido peer na VPS)
2. ✅ Criada interface `wg-VPS` no MikroTik com chave privada exclusiva
3. ✅ Configurado peer apontando para `vpn-guarderia.awecloudsolution.com:51820`
4. ✅ Atribuído IP 10.250.0.2/32 à interface WireGuard
5. ✅ Criada rota estática para 10.250.0.1/32 via wg-VPS
6. ✅ Configurado NAT masquerade para tráfego LAN → VPN
7. ✅ Configurada regra de firewall forward permitindo LAN → wg-VPS
8. ✅ Atualizado peer do MikroTik na VPS: allowed-ips 10.250.0.2/32,192.168.15.0/24
9. ✅ Validado handshake WireGuard bidirecional
10. ✅ Testado ping e SSH do notebook na LAN para a VPS
11. ✅ Identificado HTTP 403 nos painéis (IP allowlist do Traefik)
12. ✅ Atualizado middleware Traefik do Portainer incluindo 10.250.0.2 e 192.168.15.0/24
13. ✅ Validado acesso ao Portainer da LAN local
14. ✅ Backup das configurações MikroTik e VPS
15. ⚠️ Detectada ausência inicial da rota Linux VPS → 192.168.15.0/24 após alteração dinâmica do peer
16. ✅ Instalada e persistida a rota pela `wg0`; NVR 192.168.15.110 respondeu 3/3, sem perda
17. ⚠️ Reinício da interface pelo próprio túnel interrompeu a administração; recuperação realizada pelo console do provedor
18. ✅ Serviço `wg-quick@wg0` habilitado/ativo e rota confirmada após reinicialização; SSH público permaneceu bloqueado

**Responsável:** Wittemberg  
**Validado por:** Usuário (testes de ping, SSH e painel)  
**Evidências:** handshake ativo, logs de acesso, screenshots salvos em `/root/guarderia-evidencias/`
