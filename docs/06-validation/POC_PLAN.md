# Plano de prova de conceito

Estado: pronto para revisão e execução futura. Nenhum resultado real preenchido. Objetivo: demonstrar conectividade útil, segura e sustentável a 50/100 m sob movimentação, com observabilidade desde o primeiro teste.

## Preparação obrigatória

NOC e VPN funcionais; relógios sincronizados; coleta RF validada; backup restaurado; alimentação em bancada aprovada; equipamentos e versões inventariados; local e intervenção na embarcação autorizados. Um wAP pode ser usado sequencialmente nas distâncias de 50 e 100 m; isso não equivale a testar dois barcos simultâneos.

## Instrumentação

- mANTBox na montagem candidata; core e estação de teste cabeada na margem.
- wAP na montagem candidata; computador de teste conectado à LAN embarcada.
- Zabbix a 5 s nos itens essenciais, registrando atraso real.
- Sonda ICMP local de 1 s com enviados/recebidos, RTT e horário em arquivo local protegido.
- Gerador de tráfego TCP/UDP em hosts de teste; evitar usar CPU dos roteadores como única fonte de throughput.
- Multímetro/medidor de energia adequados e registro das condições físicas.
- Marcações de distância, orientação, vento, maré, inclinação, obstáculos, canal e carga aplicada.

## Casos de ensaio

| ID | Execução | Duração mínima proposta | Evidência |
|---|---|---|---|
| RF-01 | Bancada: cliente 5 GHz e LAN 2,4 GHz simultâneos | 1 h | Config/associação/tráfego/logs |
| RF-02 | Campo a 50 m e 100 m, orientações 0/90/180/270° | 10 min por orientação/distância | Dados brutos e marcações |
| RF-03 | Giro lento completo, ambos os sentidos quando viável | 3 ciclos por distância | Piores trechos, perda e reconexões |
| RF-04 | Carga progressiva com fluxos de vídeo/alarme | 30 min por cenário | Vazão útil, RTT, perda e CPU |
| RF-05 | Permanência com variação natural | 24 h e depois 7 dias | Cobertura de coleta e incidentes |
| LAN-01 | DHCP/DNS, Internet e acesso administrativo | 10 repetições funcionais | Falhas e tempos |
| ENE-01 | Carga normal, noturna e sirene; autonomia | Período acordado do kit | Wh/Ah e tensão nos terminais |

Orientação 0° significa proa voltada à margem; registrar a orientação do próprio wAP em relação ao barco. Registrar como “não executado” quando a manobra não puder ser feita com segurança; não interpolar resultado faltante.

## Critérios de aceite propostos

| Medida | Critério inicial | Interpretação |
|---|---|---|
| Perda local | ≤ 1% em cada janela de orientação e no ensaio total | Reprovar orientação ruim mesmo com média total boa |
| Interrupção local | Nenhuma sequência > 5 s sem resposta durante teste controlado | Investigar interferência, energia e medição |
| Latência local | p95 ≤ 30 ms em repouso; ≤ 100 ms com carga contratada | Exclui WAN/VPS |
| Vazão útil | ≥ 1,3 × demanda simultânea medida do kit | Valor em Mbps depende do kit real |
| Associação | Sem reconexões espontâneas nos testes controlados | Eventos intencionais são anotados |
| Coleta RF | ≥ 99% das amostras previstas dos itens suportados habilitados | Relatar lacunas e itens excluídos; não inventar dados |
| Relógios | Desvio ≤ 1 s entre fontes do ensaio | Condição para correlação temporal |
| Segurança | Todos os testes negativos de isolamento passam | Falha bloqueia multicliente |
| Alimentação | Sem reset/subtensão durante carga e autonomia definida | Limites pelo projeto do kit |

RSSI alvo inicial de investigação: preferir margem estável acima de −70 dBm; abaixo de −75 dBm requer análise. Não aprovar/reprovar exclusivamente pelo RSSI se taxa, perda e aplicação indicarem outra situação. SNR/CCQ indisponível deve constar como lacuna, não valor inventado.

## Testes de falha

Desconectar WAN, interromper VPS, desligar a conexão da central NOC e reiniciar equipamento em janela controlada, um cenário por vez. Alarme e gravação locais devem continuar quando aplicável. Proposta de recuperação de rede: até 180 s após retorno do serviço/energia e boot concluído; medir também tempo total desde energização, separadamente. Verificar DNS, túnel, rotas e coleta, não somente LEDs.

## Decisão ao final

Resultado: aprovado, aprovado com restrições identificadas ou reprovado. Reprovação por rotação exige nova posição/antena ou arquitetura alternativa e repetição do ensaio afetado. Aprovação de um kit não homologa 20 barcos nem estabelece SLA comercial. Dados brutos e configuração exata devem acompanhar a conclusão.
