# Proposta de redundância WAN da central NOC

Estado: proposta incorporada a partir dos anexos do usuário; depende de inventário, adaptação e laboratório. Referência: [revisão do template](ROUTEROS_BASELINE_REVIEW.md). Alvo: RB750r2 (hEX lite) da central NOC, RouterOS 7.23.7. A VPS continua sendo pré-requisito da configuração WireGuard.

## Escopo

WAN1 preferencial e WAN2 de contingência, com retorno automático à WAN1 depois de detectada sua recuperação. A redundância protege o acesso da central NOC; não torna redundante a WAN da guarderia ou a VPS. Existência e contratação de dois links na central NOC ainda não foram confirmadas.

## Portas propostas para esta variante

| Porta RB750r2 | Papel |
|---|---|
| ether1 | WAN1 para modem/roteador do provedor primário |
| ether2 | WAN2 para modem/roteador do provedor de contingência |
| ether3–5 | LAN administrativa; definir porta física de recuperação |
| Rádio WLAN | Não aplicável: nenhuma interface WLAN na RB750r2 |
| wg-VPS | Administração roteada até VPS; IP do plano canônico |

Essa atribuição não se aplica ao RB750Gr3, cujo ether2 transporta as VLANs da guarderia.

## Parâmetros a confirmar

Inventariar por WAN: provedor, modem, endereço/máscara/gateway, estático ou DHCP/PPPoE, reserva fora do pool do modem, disponibilidade ICMP e capacidade. Verificar ausência de sobreposição entre as WANs e as redes do projeto. Dois modems com a mesma sub-rede não são cobertos diretamente por este template; reendereçar ou projetar separação específica.

A variante recebida é estática. WAN DHCP exige tratamento da mudança/expiração do lease e atualização das rotas de sonda. Impedir default dinâmica concorrente que burle a prioridade definida. PPPoE requer variante própria. Não adaptar só o IP mantendo next-hop antigo.

## Roteamento esperado

| WAN | Sondas candidatas do anexo | Rota de sonda | Defaults recursivas |
|---|---|---|---|
| WAN1 | 9.9.9.9 e 208.67.222.222 | /32 via gateway WAN1, scope 10 | distance 1, target-scope 11, check-gateway ping |
| WAN2 | 149.112.112.112 e 208.67.220.220 | /32 via gateway WAN2, scope 10 | distance 2, target-scope 11, check-gateway ping |

Endereços são candidatos fornecidos no anexo, não alvos já ensaiados. Confirmar permissões/limitação de resposta, próximo salto efetivo e origem usada por cada teste. Sonda manual pode seguir uma default alternativa quando sua /32 não é utilizável; não validar o vínculo à WAN apenas com ping genérico. Conferir resolução recursiva, interfaces e observação por link no laboratório.

Manter defaults configuradas e sem scripts que as desabilitem ao perder Internet. O tempo de detecção depende das opções de checagem vigentes; registrar intervalos, timeout, contagem de falhas e tempo medido. Retorno automático pode oscilar em link intermitente: testar e decidir necessidade de política adicional de estabilidade, sem prometer cooldown que o arquivo não implementa.

## VPN e segurança

Preservar IPAM/AllowedIPs/rotas do [WireGuard](WIREGUARD.md). O endpoint público da VPS deve seguir a WAN disponível, sem rota fixa que o aprisione na WAN1. A RB750r2 inicia a sessão e mantém keepalive; testar novo tráfego bidirecional após falha, além de observar handshake.

Se for necessária regra UDP de entrada adicional, restringir endpoint/porta conforme desenho e teste; não abrir gerência pública. O caminho iniciado pela RB pode receber respostas via conntrack, mas mudança de WAN/NAT deve ser ensaiada. Limitar input e forward por fonte/destino/serviço. NTP/DNS/WinBox/SNMP têm funções e permissões distintas; uma lista MGMT não deve autorizar toda a LAN indiscriminadamente.

Durante ensaios, retirar FastTrack dos fluxos que dependem de medição/filas, preservando acesso de recuperação. Decisão de habilitá-lo posteriormente deve incluir teste de carga e contadores, sem afirmar suporte de offload a partir de `hw-offload=yes` no arquivo.

## Plano de testes

Todos os casos abaixo estão **não executados**. Registrar em [homologação](../06-validation/HOMOLOGATION.md).

| ID | Cenário | Critério observável |
|---|---|---|
| ROS-01 | Adaptação e import dry-run em laboratório | Sintaxe válida, parâmetros completos e portas corretas; sem alterações no dry-run |
| WAN-01 | Duas WANs operantes | Novas conexões preferem WAN1; ambas sondadas pelo caminho esperado |
| WAN-02 | Queda física WAN1 e retorno | WAN2 assume; WAN1 reassume após detecção; medir interrupção |
| WAN-03 | Falha de uma sonda e depois das duas da WAN1 com Ethernet ativa | Uma sonda sobrevivente mantém WAN1; ambas indisponíveis tornam WAN2 elegível |
| WAN-04 | Queda simultânea | Defaults sem caminho ficam inativas, não desabilitadas; rotas de sondas mantidas |
| WAN-05 | Recuperar somente WAN2 após falha total; repetir só WAN1 | Recuperação automática em cada cenário, sem editar rotas |
| WAN-06 | Repetir falha/retorno com WireGuard e sessões ativas | Tráfego real central NOC→VPS→core retorna; registrar efeito em sessões existentes |
| WAN-07 | Reboot e intermitência | Configuração persiste; contagem de trocas e estabilidade registradas |

Os sete testes do anexo são cobertos por WAN-01, WAN-02, WAN-04, WAN-05 e WAN-06; WAN-03 e WAN-07 ampliam a cobertura. Dry-run não equivale a esses ensaios.

## Próximo passo autorizado nesta fase

Somente incorporar e documentar. A futura configuração adaptada depende de inventário das WANs, VPS pronta, backup e plano de recuperação. A proposta não autoriza executar o reset indicado no comentário do original nem configurar os equipamentos agora.

## Pré-condição observada em 21/09/2026

WAN1 estática já funciona em ether1-LINK1; ether2-LINK2 consta apenas como reserva. Bridge LAN ativa em ether3/ether4/ether5-lan. A default atual verifica o gateway diretamente, sem sondas recursivas. Portanto WAN-01 a WAN-07 seguem não executados. O equipamento não apresenta interface wlan1: a instrução correspondente do template não se aplica. A configuração de partida é o [inventário atual](../01-architecture/NOC_ROUTER_INVENTORY.md), não uma bancada vazia. A LAN ativa sobrepõe o exemplo WAN1 do template; parâmetros devem ser reconstruídos sem importar valores de exemplo.
