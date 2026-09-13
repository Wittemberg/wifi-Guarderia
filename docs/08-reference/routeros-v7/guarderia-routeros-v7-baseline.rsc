# WiFi Guarderia Vitoria - RouterOS v7 baseline
# Alvo inicial: RB951G-2HnD / RouterOS 7.23.x long-term
#
# IMPORTANTE:
# 1) Edite SOMENTE o bloco de variaveis antes de importar.
# 2) Este modelo assume WANs com IP/gateway estaticos entregues pelos roteadores/modems dos provedores.
# 3) WAN1 = primaria; WAN2 = backup.
# 4) O failover NAO desabilita rotas por script. Usa roteamento recursivo + check-gateway.
# 5) Se as duas WANs cairem, as rotas default ficam INATIVAS (nao disabled) e se recuperam sozinhas.
# 6) WireGuard e o canal de gerenciamento para a VPS publica.
#
# Recomendado aplicar apos:
# /system reset-configuration no-defaults=yes skip-backup=yes
#
# ---------------------------------------------------------------------------
# VARIAVEIS - EDITE AQUI
# ---------------------------------------------------------------------------
{
    :global CFG_IDENTITY       "GUARDERIA-POC-RB951";

    :global CFG_WAN1_ADDR      "192.168.15.253/24";
    :global CFG_WAN1_NET       "192.168.15.0";
    :global CFG_WAN1_GW        "192.168.15.1";

    :global CFG_WAN2_ADDR      "192.168.68.253/24";
    :global CFG_WAN2_NET       "192.168.68.0";
    :global CFG_WAN2_GW        "192.168.68.1";

    :global CFG_LAN_ADDR       "192.168.50.1/24";
    :global CFG_LAN_NET        "192.168.50.0";
    :global CFG_LAN_CIDR       "192.168.50.0/24";
    :global CFG_LAN_GW         "192.168.50.1";
    :global CFG_LAN_POOL       "192.168.50.50-192.168.50.220";

    # WireGuard - VPS
    :global CFG_WG_ADDR        "10.200.0.2/24";
    :global CFG_WG_VPS_IP      "COLOQUE_IP_PUBLICO_DA_VPS";
    :global CFG_WG_VPS_PORT    51820;
    :global CFG_WG_VPS_PUBKEY  "COLOQUE_CHAVE_PUBLICA_WIREGUARD_DA_VPS";
    :global CFG_WG_VPS_TUN_IP  "10.200.0.1/32";
}

# ---------------------------------------------------------------------------
# IDENTIDADE / INTERFACES
# ---------------------------------------------------------------------------
/system identity set name=$CFG_IDENTITY

/interface ethernet
set [find default-name=ether1] name=ether1-WAN1 comment="WAN1 - PRIMARIA"
set [find default-name=ether2] name=ether2-WAN2 comment="WAN2 - BACKUP"
set [find default-name=ether3] name=ether3-LAN
set [find default-name=ether4] name=ether4-LAN
set [find default-name=ether5] name=ether5-LAN

/interface bridge
add name=bridge-LAN protocol-mode=rstp comment="LAN Guarderia"

/interface bridge port
add bridge=bridge-LAN interface=ether3-LAN
add bridge=bridge-LAN interface=ether4-LAN
add bridge=bridge-LAN interface=ether5-LAN

# RB951: radio legado nao e necessario no core/gerenciamento.
# Se quiser usa-lo depois, reabilite e configure conscientemente.
/interface wireless
set [find default-name=wlan1] disabled=yes

/interface list
add name=WAN comment="Links de Internet"
add name=LAN comment="Rede local confiavel"
add name=MGMT comment="Interfaces de gerenciamento"

/interface list member
add interface=ether1-WAN1 list=WAN
add interface=ether2-WAN2 list=WAN
add interface=bridge-LAN list=LAN
add interface=bridge-LAN list=MGMT

# ---------------------------------------------------------------------------
# ENDERECAMENTO
# ---------------------------------------------------------------------------
/ip address
add address=$CFG_WAN1_ADDR interface=ether1-WAN1 network=$CFG_WAN1_NET comment="WAN1"
add address=$CFG_WAN2_ADDR interface=ether2-WAN2 network=$CFG_WAN2_NET comment="WAN2"
add address=$CFG_LAN_ADDR interface=bridge-LAN network=$CFG_LAN_NET comment="LAN"

# ---------------------------------------------------------------------------
# DHCP / DNS
# ---------------------------------------------------------------------------
/ip pool
add name=pool-LAN ranges=$CFG_LAN_POOL

/ip dhcp-server
add name=dhcp-LAN interface=bridge-LAN address-pool=pool-LAN lease-time=12h disabled=no

/ip dhcp-server network
add address=$CFG_LAN_CIDR gateway=$CFG_LAN_GW dns-server=$CFG_LAN_GW

/ip dns
set allow-remote-requests=yes cache-size=4096KiB servers=1.0.0.1,8.8.4.4

# ---------------------------------------------------------------------------
# FAILOVER ROUTEROS v7 - SEM SCRIPT QUE DESABILITA ROTAS
#
# Dois alvos independentes por WAN.
# As /32 fixam cada sonda no seu respectivo gateway.
# As defaults recursivas usam check-gateway=ping.
#
# WAN1: distance=1
# WAN2: distance=2
#
# Se WAN1 falhar -> WAN2 assume.
# Se WAN1 voltar -> WAN1 reassume automaticamente.
# Se ambas falharem -> defaults ficam INATIVAS, mas as /32 continuam presentes,
# permitindo que o RouterOS continue testando e reative a default assim que
# qualquer caminho voltar.
# ---------------------------------------------------------------------------
/ip route
# Sondas WAN1
add dst-address=9.9.9.9/32 gateway=$CFG_WAN1_GW scope=10 comment="PROBE-WAN1-QUAD9"
add dst-address=208.67.222.222/32 gateway=$CFG_WAN1_GW scope=10 comment="PROBE-WAN1-OPENDNS"

# Sondas WAN2
add dst-address=149.112.112.112/32 gateway=$CFG_WAN2_GW scope=10 comment="PROBE-WAN2-QUAD9"
add dst-address=208.67.220.220/32 gateway=$CFG_WAN2_GW scope=10 comment="PROBE-WAN2-OPENDNS"

# Defaults recursivas WAN1 - primaria
add dst-address=0.0.0.0/0 gateway=9.9.9.9 distance=1 scope=30 target-scope=11 check-gateway=ping comment="DEFAULT-WAN1-PROBE1"
add dst-address=0.0.0.0/0 gateway=208.67.222.222 distance=1 scope=30 target-scope=11 check-gateway=ping comment="DEFAULT-WAN1-PROBE2"

# Defaults recursivas WAN2 - backup
add dst-address=0.0.0.0/0 gateway=149.112.112.112 distance=2 scope=30 target-scope=11 check-gateway=ping comment="DEFAULT-WAN2-PROBE1"
add dst-address=0.0.0.0/0 gateway=208.67.220.220 distance=2 scope=30 target-scope=11 check-gateway=ping comment="DEFAULT-WAN2-PROBE2"

# ---------------------------------------------------------------------------
# NAT
# ---------------------------------------------------------------------------
/ip firewall nat
add chain=srcnat action=masquerade out-interface-list=WAN comment="NAT Internet"

# ---------------------------------------------------------------------------
# WIREGUARD -> VPS
# MikroTik inicia a sessao; funciona atras de CGNAT.
# A interface gera sua propria private/public key ao ser criada.
# ---------------------------------------------------------------------------
/interface wireguard
add name=wg-VPS listen-port=51821 mtu=1420 comment="Gerenciamento -> VPS"

/ip address
add address=$CFG_WG_ADDR interface=wg-VPS comment="WireGuard VPS"

/interface wireguard peers
add interface=wg-VPS \
    public-key=$CFG_WG_VPS_PUBKEY \
    endpoint-address=$CFG_WG_VPS_IP \
    endpoint-port=$CFG_WG_VPS_PORT \
    allowed-address=$CFG_WG_VPS_TUN_IP \
    persistent-keepalive=25s \
    comment="VPS Guarderia"

/interface list member
add interface=wg-VPS list=MGMT

# ---------------------------------------------------------------------------
# FIREWALL INPUT - PROTEGE O PROPRIO MIKROTIK
# ---------------------------------------------------------------------------
/ip firewall filter
add chain=input action=accept connection-state=established,related,untracked comment="INPUT - established/related"
add chain=input action=drop connection-state=invalid comment="INPUT - drop invalid"
add chain=input action=accept protocol=icmp comment="INPUT - ICMP"
add chain=input action=accept in-interface-list=MGMT comment="INPUT - gerenciamento LAN/WireGuard"
add chain=input action=drop in-interface-list=WAN comment="INPUT - bloqueia WAN"
add chain=input action=drop comment="INPUT - drop final"

# ---------------------------------------------------------------------------
# FIREWALL FORWARD - PROTEGE A LAN
# ---------------------------------------------------------------------------
/ip firewall filter
add chain=forward action=fasttrack-connection connection-state=established,related hw-offload=yes comment="FWD - FastTrack"
add chain=forward action=accept connection-state=established,related,untracked comment="FWD - established/related"
add chain=forward action=drop connection-state=invalid comment="FWD - drop invalid"
add chain=forward action=accept in-interface-list=LAN out-interface-list=WAN comment="FWD - LAN -> Internet"
add chain=forward action=accept in-interface=wg-VPS out-interface=bridge-LAN comment="FWD - VPS -> LAN"
add chain=forward action=accept in-interface=bridge-LAN out-interface=wg-VPS comment="FWD - LAN -> VPS"
add chain=forward action=drop in-interface-list=WAN connection-state=new connection-nat-state=!dstnat comment="FWD - bloqueia entrada WAN nao solicitada"
add chain=forward action=drop comment="FWD - drop final"

# ---------------------------------------------------------------------------
# SERVICOS / DESCOBERTA / ACESSO MAC
# ---------------------------------------------------------------------------
/ip service
set telnet disabled=yes
set ftp disabled=yes
set www disabled=yes
set www-ssl disabled=yes
set api disabled=no port=58728
set api-ssl disabled=yes
set ssh disabled=yes
set winbox disabled=no port=58292

/ip neighbor discovery-settings
set discover-interface-list=MGMT

/tool mac-server
set allowed-interface-list=none

/tool mac-server mac-winbox
set allowed-interface-list=LAN

# ---------------------------------------------------------------------------
# CLOUD / HORA
# ---------------------------------------------------------------------------
/ip cloud
set ddns-enabled=yes ddns-update-interval=5m

/system clock
set time-zone-autodetect=no time-zone-name=America/Sao_Paulo

/system ntp client
set enabled=yes mode=unicast

/system ntp client servers
add address=time.cloudflare.com
add address=time.google.com

# ---------------------------------------------------------------------------
# OPCIONAL - SNMP PARA MONITORAMENTO CENTRAL NA VPS
# Recomendo ativar depois que o WireGuard estiver operacional.
#
# Exemplo conceitual (NAO importar sem trocar credenciais):
#
# /snmp set enabled=yes contact="WR Tecologia" location="Guarderia"
# /snmp community
# add name="TROCAR_USUARIO_SNMPV3" \
#     addresses=10.200.0.1/32 \
#     security=private \
#     authentication-protocol=SHA1 \
#     authentication-password="TROCAR_AUTH" \
#     encryption-protocol=AES \
#     encryption-password="TROCAR_PRIV"
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# VALIDACAO POS-IMPORT
# ---------------------------------------------------------------------------
:log warning "GUARDERIA: baseline RouterOS v7 aplicada. Validar WAN1/WAN2, failover e WireGuard."
