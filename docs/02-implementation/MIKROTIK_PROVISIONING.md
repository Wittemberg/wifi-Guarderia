# Provisionamento MikroTik

Estado: roteiro planejado; comandos abaixo são somente leitura. Há um [template recebido arquivado](ROUTEROS_BASELINE_REVIEW.md), ainda inadequado para importação. Scripts `.rsc` adaptados serão produzidos após inventário e seleção do modem/roteador 4G, credenciais e homologação da VPN por barco.

## Inventário comum

```routeros
/system resource print
/system package print
/system routerboard print
/interface print detail
/ip address print
/ip route print
```

Registrar saídas em armazenamento privado. Para rádios AX, inspecionar `/interface/wifi print detail` e `/interface/wifi/registration-table print detail` conforme pacote instalado. A ausência desse menu na RB750r2 não é falha: ela não será o rádio AX do projeto.

## Padrão comum

Identidades propostas: `GV-NOC-01`, `GV-BARCO-001` a `020`; ativos de modem/AP separados recebem sufixo de função. Usuários administrativos nominais; conta de coleta separada e privilégio mínimo; desativar contas padrão após testar substitutas. Desabilitar serviços não utilizados, WPS e descoberta/gerência MAC em interfaces não administrativas.

Atualização RouterOS/RouterBOOT deve ser feita em bancada com backup e acesso local, considerando arquitetura e espaço livre. WireGuard requer RouterOS v7; a versão exata deve ser escolhida e registrada após verificar compatibilidade das RBs. Não copiar pacotes ARM para equipamentos de outra arquitetura.

## Kit 4G embarcado — proposta de 29/09/2026

O modelo ainda não foi escolhido e pode não ser MikroTik. Aplicar comandos RouterOS somente a equipamento/versão inventariados; o procedimento geral está em [conectividade celular](CELLULAR_CONNECTIVITY.md).

1. Cadastrar modem/roteador e SIM; conferir APN e bandas com documentação do modelo/plano.
2. Preparar recuperação local e backup; validar sessão 4G, DNS/NTP e acesso à Internet em bancada.
3. Separar WAN celular da LAN; configurar gateway, DHCP e WiFi local conforme [IPAM](../01-architecture/NETWORK_PLAN.md).
4. Aplicar NAT IPv4 só na WAN, firewall e política IPv6; isolar rede de clientes, kit e gerência conforme interfaces disponíveis.
5. Adicionar peer WireGuard exclusivo à VPS, rotas de retorno e ACLs restritas; não anunciar default pelo túnel.
6. Testar QoS/limites locais e comparar contadores com consumo da operadora. Filas não garantem velocidade no 4G; conferir efeito de FastTrack/offload quando usados.
7. Integrar telemetria suportada, ensaiar reconexão, reboot e restauração antes da instalação embarcada.

A RB750Gr3 fica disponível para avaliação de bancada ou roteador complementar; seu uso não é obrigatório. Provisionamento de mANTBox e uplink 5 GHz do wAP foi retirado com o enlace terrestre. AP local adicional exige seleção própria.

## Central NOC — RB750r2

Atualização concluída pelo usuário: RouterOS 7.23.7 (long-term), RouterBOOT atual/disponível 7.23.7. A VPS e o notebook já estão conectados; a RB750r2 tem inventário de rede recebido em 21/09/2026; a funcionalidade da VPN da RB foi confirmada pelo usuário em 22/09/2026. Confirmar backup e recuperação local antes de qualquer expansão. Não há necessidade de tratar sua atualização para RouterOS v7 como etapa ainda pendente. Consultar o [inventário recebido](../01-architecture/NOC_ROUTER_INVENTORY.md); manter backup, conferência das interfaces e testes antes de aplicar o plano.

Usar uma porta de uplink da central NOC e uma LAN administrativa dedicada. Configurar WireGuard e rotas de gerenciamento sem alterar a rede existente da central NOC. Não publicar WinBox/API. Manter somente o tráfego administrativo autorizado no túnel, sem transformar a RB750r2 em requisito da operação da guarderia.

A [variante dual-WAN](NOC_DUAL_WAN.md) propõe ether1/ether2 como WAN e ether3–5 como LAN na RB750r2. Confirmar segundo link e portas antes de adotar. Resolver os achados da revisão, completar parâmetros e executar ROS-01; não importar o original nem seguir automaticamente seu comentário de reset.

## Dados mínimos para futuro template

Cada template exige modelo/versão, identity, mapa de portas, IPs, segmentação local, SIM/APN por referência, perfil celular, DNS/NTP, rotas, ACLs, coleta e método de rollback. Gerar um diff por equipamento; evitar reset/import global como padrão. Templates sanitizados devem ter parâmetros obrigatórios que falhem quando ausentes.

## Critérios

HW-01, LAN-01, CEL-01 e SEC-01/02/03 precisam de evidência. Export real, inclusive sem senhas explícitas, pode conter identidade e detalhes sensíveis: manter fora do Git. Testar boot frio, lease DHCP, DNS, retorno VPN, isolamento e acesso de recuperação antes da instalação embarcada.

## Condição de partida da central NOC — 21/09/2026

O [inventário](../01-architecture/NOC_ROUTER_INVENTORY.md) confirma gateway em uso, WAN1 estática, bridge LAN nas três últimas portas, DHCP, DNS e masquerade. Preservar essa operação. A LAN 10.21.0.0/24 é futura e exige desenho de porta/VLAN; WAN2 está reservada. A coleta de 21/09 não continha WireGuard; sua funcionalidade foi confirmada pelo usuário em 22/09. Nenhum reset/import global é necessário para preparar a integração. Conferir acesso local e backup antes de mudar ACLs, endereços ou serviços.
