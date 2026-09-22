# Contrato de coleta e qualidade das métricas

Estado: especificação, sem templates importados ou resultados reais. Zabbix é a fonte principal; Grafana consulta essa fonte. O Kuma fornece síntese de disponibilidade e não substitui coleta RF.

## Dimensões obrigatórias

Toda amostra deve ser associada a local, equipamento, interface/peer, origem da medição, timestamp de coleta e unidade. Registrar versão RouterOS, pacote WiFi, versão do template e origem SNMP/API/sonda. A fonte de RSSI da base descreve recepção na base; não rotular como recepção no barco.

Estados: `valid`, `unsupported`, `timeout`, `stale`, `unauthorized`, `error`. Valor ausente é nulo/sem dado. Não preencher com zero, repetir indefinidamente último valor nem interpolar falhas em relatório de aceite.

## Matriz de coleta proposta

| Métrica | Fonte candidata | Unidade/tipo | PoC | Operação | Observações |
|---|---|---|---|---|---|
| RSSI por peer | WiFi registration table | dBm | 5 s | 30 s | Coletar em ambos os lados quando exposto |
| Taxa física Tx/Rx | WiFi registration table | Texto bruto + valor normalizado | 5 s | 30 s | Não é vazão útil |
| Tempo de associação | WiFi registration table | s | 5 s | 30 s | Reset não equivale automaticamente a reboot |
| Reconexão/desassociação | Eventos RouterOS + uptime associação | contador/evento | Evento | Evento | Distinguir perda de logs e reboot |
| SNR/ruído/CCQ | Somente se exposto e validado | dB/dBm/% | 5 s | 30 s | Não presumir equivalência entre drivers |
| Tráfego interfaces | Contadores 64-bit SNMP/API | octetos → bit/s | 5 s | 30 s | Tratar reset/wrap e intervalo real |
| Erros e drops | Contadores interface | contagem/delta | 5 s | 60 s | Sem converter diretamente em perda fim a fim |
| ICMP local core–barco | Host cabeado de teste → LAN barco | RTT ms, enviados/recebidos | 1 s em ensaio | Perfil a definir | Isola rádio e roteamento local |
| ICMP VPS–core/wAP | Zabbix via VPN | RTT ms, perda % | Janela 5 s | 30 s | Inclui WAN e VPN |
| CPU/RAM | SNMP/API | %, bytes | 30 s | 60 s | Memória total e livre reais |
| Temperatura/tensão | Health suportado | °C/V | 60 s | 60 s | Não inferir estado de carga só pela tensão |
| Uptime/versão | SNMP/API | s/texto | 60 s | 300 s | Versão reavaliada após mudança |
| Saúde WireGuard | Host/RouterOS | idade handshake, bytes | 30 s | 60 s | Somar sonda de rota funcional |
| NOC/banco/disco | Métricas internas e host | fila, atraso, bytes/% | 30–60 s | 60 s | Monitorar o monitoramento |

Intervalo proposto não assegura resolução real. Medir agendamento, atraso e custo; coleta concorrente não pode sobrecarregar a RB750r2/core. Interface WiFi moderna e campos documentados: [MikroTik WiFi](https://help.mikrotik.com/docs/spaces/ROS/pages/224559120/WiFi).

## Fontes e descoberta

SNMPv3 autenticado/cifrado é preferido para contadores e recursos. Fazer descoberta limitada aos dispositivos autorizados e mapear OID/índice por identidade estável; não inventar OIDs RF. Importar template compatível com versão e revisar itens não suportados. Referência: [itens SNMP no Zabbix](https://www.zabbix.com/documentation/7.0/en/manual/config/items/itemtypes/snmp).

Para WiFi AX não exposto por SNMP, coletor restrito por API/REST TLS validado pode produzir uma leitura mestre e itens dependentes. Validar formatos e permissão por equipamento. Não criar acesso administrativo irrestrito apenas para ler registro RF. Se um campo não for exposto, registrar `unsupported` e avaliar alternativa em laboratório.

## Fórmulas

`Vazão (bit/s) = 8 × (contador_atual − contador_anterior) / Δt_real`

Após reset, descartar o delta inválido e marcar interrupção. Não transformar valor negativo em tráfego normal.

`Perda ICMP (%) = 100 × (enviados − recebidos) / enviados`

Registrar quantidade e timeout por janela; janela sem pacotes enviados não tem perda calculável. TCP connect apenas demonstra acessibilidade de uma porta e sua latência de estabelecimento. Não equivale a perda ICMP 0%/100%.

Calcular percentis sobre amostras brutas identificadas, não sobre médias horárias. Atraso de atualização do dashboard não é latência de rede. Resolução de coleta de 5 s não captura eventos subsegundo; por isso há sonda local de 1 s e eventos durante a PoC.

## Testes de qualidade

1. Comparar amostra com consulta direta do equipamento no mesmo instante.
2. Interromper credencial e caminho separadamente; observar estados distintos.
3. Reiniciar equipamento de laboratório e verificar reset de contadores.
4. Pausar coletor e confirmar “Sem dados”, sem mostrar alvo como normal.
5. Comparar timestamps; meta proposta de desvio menor ou igual a 1 s entre fontes de ensaio.
6. Exportar dados brutos com lacunas e verificar que o gráfico não mascara ausência.

Sem WAN, coleta central fica interrompida. Para preservar evidência RF em campo, host local grava arquivo protegido durante o ensaio. Proxy Zabbix local é evolução opcional, dependente de equipamento persistente não previsto no inventário atual.
