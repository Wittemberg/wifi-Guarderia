# Equipamentos, rádio e montagem

Estado: especificação para aquisição e homologação; conferir SKU e revisão na entrega. Dados de fabricante consultados em 12/09/2026. As tabelas abaixo não são medições da instalação.

## Equipamentos principais

| Equipamento | Dados relevantes de fabricante | Papel/estado |
|---|---|---|
| mANTBox ax 15s, `L22UGS-5HaxD2HaxD-15S` | RouterOS v7, 256 MB RAM, 128 MB NAND; 5 GHz 15 dBi; 1 GbE e SFP com 2,5 G; IP55 | Base candidata |
| wAP ax, `wAPG-5HaxD2HaxD` | RouterOS v7, 256 MB RAM, 128 MB NAND; dual-band 2×2; 5 GHz 7 dBi; 2 GbE; IP54 | Cliente candidato |
| RB750Gr3 | 5 portas GbE, 256 MB RAM | Core já disponível; inventário pendente |
| RB951G-2HnD | 5 portas GbE, 128 MB RAM | Central NOC atualizada para RouterOS/RouterBOOT 7.23.5; aguarda acesso do usuário e inventário de rede |

Fontes: [mANTBox](https://mikrotik.com/product/mantbox_ax_15s), [wAP ax](https://mikrotik.com/product/wap_ax), [hEX RB750Gr3](https://mikrotik.com/product/RB750Gr3), [RB951G](https://mikrotik.com/product/RB951G-2HnD). As especificações de alimentação estão no [projeto DC](POWER_AND_INSTALLATION.md).

## Inventário antes de configurar

O [inventário da RB951G da central NOC](NOC_ROUTER_INVENTORY.md) foi fornecido pelo usuário em 12/09/2026 e confirma a atualização. Os demais equipamentos e os testes de portas, alimentação e capacidade continuam pendentes.

Registrar modelo, revisão, serial privado, MAC privado, origem, nota/garantia, licença, RouterOS, RouterBOOT, pacotes e fontes entregues. Verificar estado das RBs guardadas. Testar portas e alimentação em bancada. Não confundir RB750Gr3 com hEX refresh e wAP ax com wAP ac.

## Perfil RF inicial proposto

| Parâmetro | Proposta | Verificação |
|---|---|---|
| Enlace margem–barco | 5 GHz, AP/cliente | Associação e tráfego bidirecional |
| LAN do barco | 2,4 GHz, 20 MHz | Compatibilidade real alarme/câmeras |
| Canal transporte | Começar em 20 MHz; comparar 40 MHz se necessário | Ruído, utilização, perda e vazão |
| País/instalação | Brasil e outdoor, conforme opções válidas do firmware | Perfil regulatório e canais permitidos |
| Potência | Ajustar a partir da medição, dentro dos limites aplicáveis | Evitar saturação e interferência |
| Autenticação transporte | Credenciais por estação, esquema a homologar | Revogação de um barco e tentativa de troca de identidade |
| LAN IoT | WPA2-AES ou WPA3 conforme dispositivos | Desativar WPS; nenhuma rede aberta |
| Roaming/CAPsMAN | Não requerido com um AP | Expansão exige teste específico |

A interface moderna é `/interface/wifi`; compatibilidade de modo e VLAN depende do pacote. O projeto roteado não requer `station-bridge`. Consulte o [manual WiFi](https://help.mikrotik.com/docs/spaces/ROS/pages/224559120/WiFi) para o firmware escolhido.

## Levantamento de campo

Produzir croqui com posição da base, área de fundeio, limites angulares, obstáculos e alturas nos extremos de maré. Registrar fotografias técnicas sanitizadas, distância medida, embarcações metálicas próximas e locais protegidos para passagem do cabo. Um setor só pode ser dimensionado depois da área e distribuição dos barcos.

O ensaio deve distinguir giro horizontal, inclinação e bloqueio pela cabine. Antena integrada não implica diagrama uniforme; orientação favorável em um ponto não valida a volta completa. Posicionar wAP externamente, evitando superfícies metálicas junto ao rádio e mantendo acesso para manutenção.

## Orçamento de enlace

Usar a equação de engenharia `Pr = Pt + Gt + Gr − Ltrajeto − Lcabos − Lmontagem`. Registrar frequência, ganhos na orientação real e margem para desvanecimento. A estimativa de espaço livre serve apenas para triagem; reflexos na água e nulos de radiação podem dominar o resultado. Não usar potência máxima de catálogo como configuração automática.

## Lista de materiais

| Item | PoC | Escala 20 | Condição |
|---|---:|---:|---|
| RB750Gr3 | 1 existente | 1 inicialmente | Capacidade medida |
| RB951G | 1 existente | 1 administrativo | Não participa do tráfego dos clientes |
| mANTBox ax 15s | 1 | A definir | Setores por levantamento e carga |
| wAP ax | 1 | 20 | Depende da aprovação RF |
| Switch gerenciável | Conforme portas/montagem | A definir | VLAN e orçamento PoE comprovados |
| Injetor/fonte compatível | Por rádio | Por rádio | Conferir itens incluídos e tensão |
| Nobreak na margem | 1 sistema | Dimensionar | Autonomia pelo consumo total |
| Kit DC/caixa/cabos/fixação | 1 barco e base | 20 kits + base | Engenharia de alimentação |
| Reserva de manutenção | A definir | A definir | Prazo/custo de reposição |

NetMetal/antenas externas são alternativas a estudar se o wAP reprovar, sem especificação premium aprovada. Nenhuma compra é autorizada por este documento.
