# Contexto consolidado

Data: 12/09/2026. Origem principal: conversa [Viabilidade Wifi Guarderia](https://chatgpt.com/c/6aa1e0b2-2ae8-83e9-9db1-c2d15a7da5ba), no projeto ChatGPT “WiFi Guarderia Vitória”. O link depende das permissões da conta. Este resumo preserva requisitos sem republicar a mensagem pessoal de terceiros.

## Problema e oportunidade

Há demanda por segurança em 10–20 embarcações fundeadas a cerca de 50–100 m da margem. A proposta recebida contempla três alternativas: alarme; alarme com câmeras interna e externa e acesso por aplicativo; e a mesma solução com empresa de vigilância. A composição original inclui central, três sensores de contato sem fio, duas sirenes e sinalização luminosa.

O responsável técnico deve definir alimentação mínima, manutenção preventiva, custo de visita extraordinária e reparos. O usuário quer avaliar um serviço recorrente que financie equipamento e conectividade, evitando cobrança inicial de instalação ou reduzindo-a. Preço, contrato, autonomia e viabilidade comercial ainda não estão aprovados.

## Fatos confirmados pelo usuário

- Conhecimento prático de MikroTik, Intelbras, TP-Link e algum UniFi.
- Barcos se deslocam e giram com vento e corrente; enlace não pode depender de alinhamento direcional fixo a bordo.
- Internet inicial será provavelmente de provedor local, com CGNAT; Starlink saiu da primeira etapa.
- Casa também está atrás de CGNAT.
- RB951G-2HnD sem uso está disponível em casa e RB750Gr3 novo está disponível para o core.
- VPS já existe e, segundo o usuário, atende ao dimensionamento discutido. As características reais ainda não foram inventariadas.
- Preferência por Ubuntu 24.04, Docker/Portainer e instalação via SetupOrion se viável.
- Monitoramento deve estar preparado antes da PoC para registrar métricas reais desde o início.
- Pasta local e GitHub foram definidos explicitamente em 12/09/2026.

## Evolução das propostas

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

Implantação, compra, contratação de vigilância, instalação elétrica, entrega de portal próprio e automação por IA. A documentação define os requisitos dessas evoluções sem afirmar que existem.
