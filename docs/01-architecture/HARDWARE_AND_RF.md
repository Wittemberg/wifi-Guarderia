# Equipamentos, cobertura celular e montagem

Direção de 29/09/2026: um modem 4G e um SIM por barco. Modelos, consumo e desempenho ainda não selecionados nem medidos. O nome deste arquivo foi mantido para preservar os links existentes.

## Equipamentos e reaproveitamento

| Item | Papel | Estado |
|---|---|---|
| Modem/roteador 4G | Acesso WAN de cada barco; VPN integrada se suportada | A selecionar e homologar |
| SIM | Linha própria de cada barco | Fornecida pela operação ou proprietário; Vivo provável |
| Roteador adicional | LAN, firewall e VPN quando modem não atender | Condicional; incluir energia/custo |
| AP WiFi local | Conectar dispositivos a bordo | Integrado ou separado conforme cobertura |
| RB750r2 central NOC | Gateway administrativo e VPN | Inventário e evidências existentes preservados |
| RB750Gr3 disponível | Possível bancada ou roteamento embarcado | Sem papel obrigatório de core; inventário/consumo/capacidade pendentes |
| mANTBox e wAP ax do desenho anterior | Distribuição margem–barco retirada | Não comprar como requisito; eventual AP local exige reavaliação |

O [inventário NOC](NOC_ROUTER_INVENTORY.md) documenta apenas equipamento observado. Não considerar modem integrado, rádio LTE, antena externa ou suporte VPN presentes por analogia com outros modelos.

## Matriz de aquisição a preencher

Comparar modelos usando bandas e homologação aplicáveis, SIM/APN, WireGuard ou roteador complementar, firewall IPv4/IPv6, portas e WiFi, atualização/backup, telemetria disponível, faixa DC, corrente de pico, temperatura e proteção ambiental. Registrar fonte oficial e revisão do fabricante antes da compra; validar itens essenciais em bancada. Detalhamento em [conectividade celular](../02-implementation/CELLULAR_CONNECTIVITY.md).

## Levantamento celular

Medir no local de fundeio e nas posições reais do kit, em horários de pico e fora de pico, com giro/movimento natural, cabine fechada e condições de maré/obstrução registradas. Comparar posição interna/externa e alternativas de operadora quando a candidata não atender. Os antigos 50–100 m até a margem são contexto geográfico, não orçamento de enlace nem critério de cobertura 4G.

Registrar tecnologia efetiva, bandas/célula quando expostas, RSRP/RSRQ/SINR quando suportados, reconexões, vazão útil de upload/download, RTT, perda e aplicação. Ausência de métricas vira `unsupported`; não usar limites de RSSI WiFi como limites LTE. Registros de célula/localização e identificadores ficam privados.

Cobertura declarada pela operadora não substitui medição embarcada. Testar WiFi local separadamente do 4G; não inferir qualidade do acesso celular a partir da LAN. Modem e antena não devem ficar encobertos por metal sem ensaio; antena externa, MIMO, cabo e conectores dependem do modelo selecionado.

## Lista de materiais proposta

| Item | PoC de um barco | Até 20 barcos | Condição |
|---|---:|---:|---|
| Modem/roteador 4G | 1 | 20 | Homologar o conjunto |
| SIM/linha | 1 | 20 | Contrato e cobertura validados |
| Roteador VPN complementar | Se necessário | Por kit que necessitar | Sem duplicar item integrado |
| AP local | Se necessário | Por kit que necessitar | Cobertura/isolamento |
| Antena LTE/cabo/conectores | Se necessário | Conforme cada instalação | Ganho e montagem medidos |
| DC/DC, proteção, caixa, cabos/fixação | 1 kit | 20 kits | Projeto elétrico e ambiente |
| Alarme/câmeras/armazenamento | Conforme plano A/B/C | Conforme adesões | Energia e consumo de dados medidos |
| Reserva de modem/SIM/componentes | A definir | A definir | Prazo de reposição e reativação |

VPS e central NOC permanecem infraestrutura administrativa existente. Não prever base/setores/nobreak na costa para distribuir Internet. O orçamento anterior da PoC deve ser recotado para esta composição; nenhum preço novo foi presumido.
