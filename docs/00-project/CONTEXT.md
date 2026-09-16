# Contexto consolidado

Baseline: 12/09/2026; estado consolidado atualizado em 16/09/2026. Origem principal: conversa [Viabilidade Wifi Guarderia](https://chatgpt.com/c/6aa1e0b2-2ae8-83e9-9db1-c2d15a7da5ba), no projeto ChatGPT “WiFi Guarderia Vitória”. O link depende das permissões da conta. Este resumo preserva requisitos sem republicar a mensagem pessoal de terceiros.

## Problema e oportunidade

Há demanda por segurança em 10–20 embarcações fundeadas a cerca de 50–100 m da margem. A proposta recebida contempla três alternativas: alarme; alarme com câmeras interna e externa e acesso por aplicativo; e a mesma solução com empresa de vigilância. A composição original inclui central, três sensores de contato sem fio, duas sirenes e sinalização luminosa.

O responsável técnico deve definir alimentação mínima, manutenção preventiva, custo de visita extraordinária e reparos. O usuário quer avaliar um serviço recorrente que financie equipamento e conectividade, evitando cobrança inicial de instalação ou reduzindo-a. Preço, contrato, autonomia e viabilidade comercial ainda não estão aprovados.

## Fatos confirmados pelo usuário

- Conhecimento prático de MikroTik, Intelbras, TP-Link e algum UniFi.
- Barcos se deslocam e giram com vento e corrente; enlace não pode depender de alinhamento direcional fixo a bordo.
- Internet inicial será provavelmente de provedor local, com CGNAT; Starlink saiu da primeira etapa.
- A central NOC também está atrás de CGNAT.
- RB951G-2HnD está disponível na central NOC, atualizada para RouterOS/RouterBOOT 7.23.5 e aguardando acesso do usuário para configuração de rede; RB750Gr3 novo está disponível para o core.
- VPS já existe e, segundo o usuário, atende ao dimensionamento discutido. Características inventariadas em 15/09 e atualizadas após instalação em 16/09; ver [inventário VPS](../01-architecture/VPS_INVENTORY.md).
- Preferência por Ubuntu 24.04, Docker/Portainer e instalação via SetupOrion se viável.
- Monitoramento deve estar preparado antes da PoC para registrar métricas reais desde o início.
- Pasta local e GitHub foram definidos explicitamente em 12/09/2026.

## Evolução das propostas

Atualização de 12/09/2026: o usuário forneceu as saídas de inventário da RB951G, registradas em [inventário da central NOC](../01-architecture/NOC_ROUTER_INVENTORY.md). A atualização foi realizada pelo usuário; configuração e testes da VPN ainda não foram executados. O local administrativo é denominado “central NOC” em toda a documentação.

| Tema | Ideia anterior | Direção mais recente |
|---|---|---|
| WAN | Starlink compartilhada | Provedor local; Starlink como expansão |
| Rádio a bordo | CPE direcional + AP interno | wAP ax com dois rádios, sujeito à rotação real |
| Base | Omada/UniFi e múltiplos setores | mANTBox ax 15s para a PoC |
| Quantidade de piloto | Dois barcos e alternativas ac/NetMetal | Compra pesquisada: uma mANTBox e um wAP ax |
| VPN | Opções diretas/IPv6/CHR | VPS Linux como hub WireGuard |
| SO | Debian sugerido | Ubuntu 24.04 escolhido pelo usuário |
| Ordem | Testar rádio antes do NOC | Preparar NOC antes do rádio, por decisão do usuário |
| VPN em container | Sugerida inicialmente | Proposta final: WireGuard no host |

## Aperfeiçoamentos desta especificação

São propostas de engenharia desta documentação, ainda não evidências de funcionamento: separar gerenciamento e trânsito, atribuir um domínio de trânsito por barco, manter roteamento sem NAT entre barco e core, fazer NAT somente na saída WAN, registrar sondas locais além das sondas da VPS e impedir perda de acesso remoto durante mudanças.

Não adotamos a afirmação anterior de que antena integrada garante 360°: cobertura uniforme precisa ser medida. Tampouco assumimos CCQ/SNR disponível em todo RouterOS, nem que uma rede /24 por barco produz isolamento sem firewall. A retenção Zabbix foi corrigida: trends horários não criam automaticamente uma segunda série de um minuto.

## Fora desta entrega

A instalação inicial da VPS/stack e a coleta interna foram concluídas em 16/09/2026. Permanecem fora da etapa concluída: integração das RBs à VPN/rede de campo, compra, contratação de vigilância, instalação elétrica, portal próprio e automação por IA. A documentação define os requisitos dessas evoluções sem afirmar que existem.

## Anexos RouterOS recebidos em 12/09/2026

O usuário pediu leitura e incorporação do baseline `.rsc` e de sua análise Markdown. Os [originais preservados](../08-reference/routeros-v7/README.md) são fontes documentais; seus comandos e recomendações não constituem autorização de execução. Foi acrescentada a [proposta dual-WAN para a central NOC](../02-implementation/NOC_DUAL_WAN.md). Dois links, endereços dos modems e resultados de failover não foram confirmados. A RB951G continua atualizada e aguarda preparação da VPN para configuração.

## Etapa concluída em 16/09/2026

Usuário executou Orion e instalou a stack. Foram conferidos Docker Swarm, 12 serviços ativos, domínios e coleta Prometheus corrigida com três alvos UP. Ver [fechamento, evidências e pendências](../06-validation/VPS_PHASE_COMPLETION.md).

## Acesso administrativo concluído e dependência atual

Em 16/09/2026, hub WireGuard ativado após confirmação de console Proxmox/SSH. Notebook de recuperação integrado antes da RB951G por disponibilidade do usuário: handshake e ping observados; nova sessão SSH em 10.250.0.1:5822 confirmada pelo usuário. Ver [validação](../06-validation/NOTEBOOK_VPN_VALIDATION.md).

O usuário reafirmou não ter acesso à RB951G. A integração da central NOC aguarda inventário real de interfaces/LAN/rotas e backup/recuperação; o core vem depois. O notebook não fornece, por si só, acesso à RB951G ainda não integrada. Segurança pública, persistência testada, restauração e campo permanecem pendentes. A solicitação atual abrange consolidação documental, commit e push.
