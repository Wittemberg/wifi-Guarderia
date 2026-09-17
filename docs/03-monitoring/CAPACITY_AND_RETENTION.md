# Capacidade, retenção e desempenho

Estado: orçamento de capacidade paramétrico, sem benchmark de carga. Inventário da sessão registrou 95 GB livres após instalação; Docker reconhece 9 CPUs/8 GiB. Isso não valida retenção ou capacidade para 20 barcos. Ver [inventário](../01-architecture/VPS_INVENTORY.md).

## Inventário de escala

Para 20 barcos, prever pelo menos core, AP(s), 20 wAPs e host VPS. Central e 1–2 câmeras por barco podem elevar o inventário para cerca de 62–82 equipamentos no local; isso não significa que todos suportem SNMP ou a mesma frequência de coleta. A RB da central NOC e serviços da VPS entram separadamente.

## Taxa de amostras

`Amostras/dia = Σ(número de itens × 86400 / intervalo em segundos)`

**Cenário de cálculo, não inventário real:** 20 barcos × 12 itens a 5 s = 48 valores/s = 4.147.200 valores/dia, antes de base, WAN, logs e demais equipamentos. Em 14 dias são 58.060.800 valores. Com hipótese de 100 bytes efetivos por valor, seriam aproximadamente 5,8 GB decimais; índices, WAL, bloat, metadados, logs e backup podem multiplicar esse consumo. Medir bytes efetivos no banco após 24/72 h antes de aceitar capacidade.

Portanto, 4 GB RAM e 60 GB SSD são ponto de partida discutido, não garantia de retenção de todos os itens a 5 s. A fase de campo começa com um barco e coleta seletiva.

## Retenção proposta

| Classe | Coleta | Histórico bruto | Tendência/arquivo |
|---|---|---|---|
| Rádio intensivo de PoC | 5 s | 14 dias | Exportar ensaio antes da expiração |
| Sonda local de ensaio | 1 s | Arquivo protegido do ensaio | Conservar relatório + dados pelo período aprovado |
| Operação normal | 30–60 s | 90 dias se capacidade aprovada | Tendências 365 dias inicialmente |
| Logs técnicos | Evento | 30 dias inicialmente | Incidentes relevantes preservados com referência |
| Eventos de mudança/aceite | Por ocorrência | Retenção própria | 1 ano proposto, revisar classificação |

O Zabbix mantém history e trends numéricos horários; não converte automaticamente history de 5 s em history de 1 min. Reduzir intervalo depois da PoC não reamostra o passado. Se for necessário manter duas resoluções em paralelo, projetar itens/série agregada explícitos e contabilizar armazenamento. Fonte: [history e trends](https://www.zabbix.com/documentation/7.0/en/manual/config/items/history_and_trends).

Reter métricas por 2–5 anos, como sugerido na conversa, é expansão a orçar; não é compromisso desta baseline. Dados de câmera seguem política separada, nunca a retenção Zabbix.

## Recursos a medir

CPU, RAM disponível, swap, IO wait, latência de disco, tamanho de banco/WAL, crescimento diário, itens sem suporte, fila Zabbix, atraso de ingestão e duração de backup. Coleta saudável tem atraso inferior a duas vezes o intervalo contratado para o item na maior parte do ensaio; medir percentil 95 e máxima lacuna.

Meta inicial de operação: RAM sem pressão sustentada, CPU média abaixo de 70% por 15 min e pelo menos 25% de disco livre. Se extrapolado, reduzir coleta não crítica ou ampliar recursos, documentando efeito. Não reduzir silenciosamente frequência que serve ao aceite RF.

## Capacidade RF/WAN

`Banda de vídeo = número de streams simultâneos × bitrate medido por stream`

Somar upload de alarmes, consultas, retransmissões e tráfego de clientes; aplicar margem de engenharia proposta de 30% sobre a demanda medida. Taxa física WiFi é capacidade de enlace negociada e não entrega garantida a cada barco. Clientes lentos consomem tempo de rádio e afetam os demais.

Testar carga progressiva, começando em 1 e 2 estações, depois lote piloto e 20 estações reais ou emulação claramente identificada. Simulação de carga valida recursos de processamento, mas não reproduz vinte enlaces reais sobre água. Aprovar quantidade de setores por RF-04 e CAP-01.


## Retenção de backup não é retenção de métricas

A tabela de histórico/trends acima continua uma proposta de capacidade da telemetria. A política de cópias implantada é distinta: local 7 diários/4 semanais/3 mensais; S3 com expiração da versão atual em sete dias, configurada pelo usuário e observada em backup/recibo. Não alterar history/trends ou TSDB para refletir o prazo do arquivo de backup. Uma cópia pode conter histórico maior que sua janela de permanência no S3. Crescimento e custo seguem sujeitos a medição. [Procedimento e evidências](../05-operations/BACKUP_RESTORE.md).
