# Inventário e configuração atual da central NOC

Coleta fornecida pelo usuário em 21/09/2026: dez arquivos `noc-01` a `noc-10` e três testes de conectividade. Cabeçalhos: 21:20:49–21:20:50; timezone configurado America/Sao_Paulo, sem comprovação de sincronização NTP. Análise documental, sem acesso remoto ou alteração do gateway. Seriais, software-id e MACs omitidos; arquivos brutos ficam em armazenamento privado.

## Estado atual

**RB750r2 (hEX lite), revisão r3, RouterOS e RouterBOOT 7.23.7**, em uso como gateway da central NOC. Em 21/09/2026, o usuário confirmou que está navegando na Internet através dela e que o gateway está plenamente operacional. Aceite funcional de navegação confirmado pelo usuário. Reset e configuração básica informados pelo usuário. WAN1 estática, LAN com DHCP/DNS e NAT presentes nas coletas. WAN2 reservada, sem link running ou endereço atribuído. Nenhuma interface WireGuard consta nas saídas; integração com a VPS permanece pendente.

O campo `model` da RouterBOARD é a identificação adotada. Identidade de sistema não informada no export; `GV-NOC-01` permanece proposta.

## Recursos e firmware

| Campo | Valor observado |
|---|---|
| Modelo / board-name / revisão | RB750r2 / hEX lite / r3 |
| Arquitetura / plataforma | mipsbe / MikroTik |
| RouterOS | 7.23.7 (long-term) |
| Build-time | 2026-09-16 12:19:15 |
| CPU | MIPS 24Kc V7.4; 1 núcleo; 850 MHz |
| CPU na amostra | 6% |
| RAM total / livre | 64,0 MiB / 24,3 MiB |
| Armazenamento total / livre | 16,0 MiB / 3172,0 KiB |
| Uptime | 17 min 1 s |
| Setores gravados desde reboot / total | 70 / 3108 |
| Factory-software | 6.44.6 |
| Firmware-type | qca9531L |
| Factory-firmware | 6.45.9 |
| Current-firmware / upgrade-firmware | 7.23.7 / 7.23.7 |
| Bad blocks | Campo não fornecido; não interpretar como zero |

Pacotes `routeros` (10,9 MiB) e `wireless` (1388,1 KiB), ambos 7.23.7, build 2026-09-16 12:19:15, sem flags de desabilitado. A presença do pacote wireless não indica rádio físico: nenhuma interface WLAN foi listada.

O [datasheet oficial hEX lite](https://cdn.mikrotik.com/web-assets/product_files/hEX_lite_210251.pdf), consultado em 21/09/2026, especifica cinco portas Ethernet 10/100. Velocidade negociada e throughput não foram coletados. RAM, CPU e disco são amostras pontuais; medir capacidade com VPN e coleta antes do aceite. O espaço livre exige planejamento de pacotes, atualização e logs; nenhuma remoção foi executada.

## Interfaces e rede observadas

| Interface | Papel / estado na coleta |
|---|---|
| ether1-LINK1 | WAN1, running, fora da bridge |
| ether2-LINK2 | WAN2 reservada, sem flag running, fora da bridge |
| ether3, ether4, ether5-lan | LAN, running/slave, membros de bridge-LAN |
| bridge-LAN | Running; lista LAN |
| lo | Loopback running |

As duas portas WAN pertencem à lista WAN. MTU Ethernet 1500. O diagrama lógico existente deve distinguir essa rede em uso das reservas futuras do [IPAM](NETWORK_PLAN.md).

A WAN1 tem endereço privado estático /24 e next-hop no mesmo segmento; a LAN usa outro /24 privado. Endereços operacionais exatos permanecem nos anexos privados. Não há cliente DHCP WAN listado. Há uma default estática ativa, distance 1, check-gateway=ping, scope 30 e target-scope 10, e duas rotas conectadas. O ping do gateway verifica o próximo salto, não a Internet além dele. Não há sondas recursivas nem failover configurado.

DHCP `dhcpLAN` na bridge: pool de hosts .31 a .199, lease 1 dia; gateway e DNS entregues apontam para o endereço .1 da LAN. DNS upstream 1.1.1.1 e 8.8.8.8, allow-remote-requests=yes, cache 2048 KiB, uso 83 KiB. DoH não configurado; verify-doh-cert=no não representa validação TLS em uso. DDNS MikroTik habilitado, intervalo 5 min; status público e mapeamento do provedor não coletados. WAN privada, isoladamente, não comprova CGNAT do provedor; essa condição permanece informação do usuário.

## Firewall e serviços observados

Input: aceita established/related/untracked, descarta invalid, aceita ICMP, aceita todo tráfego da lista LAN e descarta demais entradas da lista WAN. Não há descarte final explícito. Forward: aceita established/related/untracked, descarta invalid, permite LAN→WAN e descarta novas conexões WAN sem dstnat. Não há descarte final explícito nem FastTrack no export. NAT: masquerade por lista WAN; nenhuma regra dstnat exportada.

| Serviço | Estado / porta TCP |
|---|---|
| WebFig HTTP | Habilitado / 780 |
| SSH | Habilitado / 5822 |
| WinBox | Habilitado / 58292 |
| API sem TLS | Habilitada / 58728 |
| API-SSL | Desabilitada / 58729 |
| FTP, Telnet, WWW-SSL, reverse-proxy | Desabilitados |

Os serviços administrativos têm `address` vazio. Na política IPv4 recebida, a LAN pode alcançá-los; novas conexões TCP pela WAN são bloqueadas pela regra input, mas isso não substitui sondagem externa. A troca de portas não restringe origens e não habilita TLS. O export não comprova política IPv6, usuários/privilégios, restrições de MAC/descoberta ou SNMP. Serviços dinâmicos listados não são prova de exposição externa nem de uso efetivo.

Antes de adicionar VPN ou novas interfaces: definir ACLs por fonte/serviço, política de descarte final e IPv6, validar acesso de recuperação e preservar DHCP/NAT do gateway. Avaliar necessidade de HTTP/API sem TLS e DDNS. Não aplicar automaticamente o template de referência sobre esta configuração.

## Testes recebidos

Todos os testes são amostras de cinco pacotes fornecidas pelo usuário, sem timestamp e comando de origem nos arquivos.

| Arquivo | Alvo | Enviados/recebidos | Perda | RTT mín. / médio / máx. |
|---|---|---|---|---|
| 01-teste-gateway.txt | Gateway privado WAN1 | 5/5 | 0% | 0,686 / 0,834 / 1,036 ms |
| 02-teste-internet.txt | 1.1.1.1 | 5/5 | 0% | 20,387 / 29,466 / 51,732 ms |
| 03-teste-dns.txt | 142.250.219.238 | 5/5 | 0% | 16,626 / 25,405 / 35,799 ms |

Há resposta ICMP aos três destinos nas amostras. O terceiro arquivo mostra somente IP: não registra nome consultado, comando de resolução ou resposta DNS. A navegação de cliente LAN foi confirmada separadamente pelo usuário em uso real em 21/09/2026. A limitação do arquivo não representa falha de Internet ou pendência do aceite funcional do gateway. O caminho específico de resolução DNS não foi isolado; throughput, VPN e failover não foram medidos por esses pings.

## Próximas verificações

1. Preservar backup privado e acesso local ao gateway em uso; não resetar/importar globalmente.
2. Usar o hub VPS já documentado como ativo, preservando seu peer do notebook; preparar somente o novo peer da RB.
3. Definir implantação da LAN administrativa dedicada 10.21.0.0/24 sem substituir a LAN atual; escolher porta/VLAN e PC autorizado.
4. Revisar serviços, fontes, IPv6, MAC/descoberta e credenciais; testar SEC-03/04.
5. Confirmar WAN2 e seu endereçamento: o exemplo WAN1 do template coincide com a rede LAN atual, portanto não deve ser aplicado.
6. Executar VPN-01/02/03, testes dual-WAN e carga quando essas funções forem implantadas. Navegação pelo gateway já tem aceite funcional do usuário; investigação específica de DNS somente se necessária.

O inventário da RB750Gr3 do core permanece pendente. Ver [homologação](../06-validation/HOMOLOGATION.md).
