# Provisionamento MikroTik

Estado: roteiro planejado; comandos abaixo são somente leitura. Há um [template recebido arquivado](ROUTEROS_BASELINE_REVIEW.md), ainda inadequado para importação. Scripts `.rsc` adaptados serão produzidos após inventário e homologação do modelo de VLAN/credenciais.

## Inventário comum

```routeros
/system resource print
/system package print
/system routerboard print
/interface print detail
/ip address print
/ip route print
```

Registrar saídas em armazenamento privado. Para rádios AX, inspecionar `/interface/wifi print detail` e `/interface/wifi/registration-table print detail` conforme pacote instalado. A ausência desse menu na RB951 não é falha: ela não será o rádio AX do projeto.

## Padrão comum

Identidades propostas: `GV-CORE-01`, `GV-AP-SETOR01`, `GV-NOC-01`, `GV-BARCO-001` a `020`. Usuários administrativos nominais; conta de coleta separada e privilégio mínimo; desativar contas padrão após testar substitutas. Desabilitar serviços não utilizados, WPS e descoberta/gerência MAC em interfaces não administrativas.

Atualização RouterOS/RouterBOOT deve ser feita em bancada com backup e acesso local, considerando arquitetura e espaço livre. WireGuard requer RouterOS v7; a versão exata deve ser escolhida e registrada após verificar compatibilidade das RBs. Não copiar pacotes ARM para equipamentos de outra arquitetura.

## Core RB750Gr3

1. Mapear WAN real e portas físicas; WAN fora da bridge LAN.
2. Configurar porta local de recuperação antes de VLAN filtering.
3. Criar VLAN 10 e apenas trânsitos dos barcos ativos.
4. Definir IP de gestão, gateways /30 e rotas LAN via wAP.
5. Configurar cliente WAN conforme provedor e NAT restrito à saída WAN.
6. Aplicar anti-spoof por interface de trânsito, ACL entre barcos e bloqueio da gerência.
7. Configurar WireGuard, rotas de retorno e coleta.
8. Configurar limites de banda conforme ensaio, evitando que vídeo monopolize upload.

FastTrack e offload podem alterar passagem por filas/contadores; verificar na configuração real. Não afirmar QoS ativo só porque uma fila existe. Toda mudança de bridge/VLAN exige teste da porta de recuperação.

## mANTBox

Identificar banda, configurar AP 5 GHz e perfil de país/instalação válido. Manter 2,4 GHz desligado durante a PoC. Uplink trunk transporta gerenciamento e trânsitos autorizados. Mapear estação autenticada para sua VLAN, validar isolamento de clientes e manter IP de gestão somente na VLAN 10.

Autenticação por barco é requisito de expansão. Escolher em laboratório mecanismo suportado para credencial individual e VLAN, com revogação individual. ACL de MAC com senha compartilhada não comprova identidade contra falsificação; se houver limitação, documentar alternativa antes de liberar múltiplos clientes.

## wAP ax

Identificar rádio 5 GHz como uplink `station`, IP WAN /30 fixo e default para core. Criar LAN privada /24 em bridge de 2,4 GHz/Ethernet; DHCP e reservas locais. Não incluir uplink 5 GHz na bridge LAN. Não criar masquerade no wAP.

Firewall input aceita gerência apenas das fontes autorizadas via trânsito; LAN de clientes recebe somente serviços locais necessários. Forward permite Internet e retorno de sessões, mas bloqueia redes de outros barcos e infraestrutura. O core repete a proteção como segunda fronteira. Validar ausência de bypass por IPv6/bridge.

## Central NOC — RB951G

Atualização concluída pelo usuário: RouterOS 7.23.5 (long-term), RouterBOOT atual/disponível 7.23.5. A VPS e o notebook já estão conectados; a RB951G aguarda acesso pelo usuário, inventário de rede e backup antes da configuração. Não há necessidade de tratar sua atualização para RouterOS v7 como etapa ainda pendente. Consultar o [inventário recebido](../01-architecture/NOC_ROUTER_INVENTORY.md); manter backup, conferência das interfaces e testes antes de aplicar o plano.

Usar uma porta de uplink da central NOC e uma LAN administrativa dedicada. Configurar WireGuard e rotas de gerenciamento sem alterar a rede existente da central NOC. Não publicar WinBox/API. Manter somente o tráfego administrativo autorizado no túnel, sem transformar a RB951 em requisito da operação da guarderia.

A [variante dual-WAN](NOC_DUAL_WAN.md) propõe ether1/ether2 como WAN e ether3–5 como LAN na RB951G. Confirmar segundo link e portas antes de adotar. Resolver os achados da revisão, completar parâmetros e executar ROS-01; não importar o original nem seguir automaticamente seu comentário de reset.

## Dados mínimos para futuro template

Cada template exige modelo/versão, identity, mapa de portas, IPs, VLAN, credencial por referência, perfil RF, DNS/NTP, rotas, ACLs, coleta e método de rollback. Gerar um diff por equipamento; evitar reset/import global como padrão. Templates sanitizados devem ter parâmetros obrigatórios que falhem quando ausentes.

## Critérios

HW-01, LAN-01, RF-01 e SEC-01/02/03 precisam de evidência. Export real, inclusive sem senhas explícitas, pode conter identidade e detalhes sensíveis: manter fora do Git. Testar boot frio, lease DHCP, DNS, retorno VPN, isolamento e acesso de recuperação antes da instalação embarcada.
