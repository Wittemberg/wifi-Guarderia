# Contrato de coleta e qualidade das métricas

Revisão de 29/09/2026. Coleta interna da VPS tem evidência anterior; integração e telemetria embarcada 4G continuam propostas. Não há modelo de modem selecionado, template LTE homologado ou API da operadora contratada.

## Identidade e qualidade

Toda amostra identifica barco, ativo, interface/peer, linha lógica, fonte, timestamp, unidade e versão do coletor/firmware. Identificadores reais de SIM, IMEI, célula e localização ficam no registro privado. Troca de IP celular não cria novo barco.

Estados: `valid`, `unsupported`, `timeout`, `stale`, `unauthorized`, `error`. Ausência é nulo, nunca zero ou normal. Preservar lacunas, idade do dado e motivo; uma última leitura não pode parecer atual.

## Matriz proposta

| Métrica | Fonte candidata | Unidade | PoC / operação | Limite |
|---|---|---|---|---|
| Registro celular e tecnologia efetiva | API/diagnóstico do modem | Estado/texto | 5 s / 60 s | Distinguir ausência de SIM, registro e sessão de dados se expostos |
| RSRP/RSRQ/SINR | Modem, conforme suporte | dBm/dB/dB | 5 s / 60 s | Sem OID inventado; não substituir por RSSI WiFi |
| Banda/célula e reconexões | Modem/log local | Texto/evento | Evento / evento | Célula privada; mudança não prova indisponibilidade |
| Tráfego WAN Tx/Rx | Contadores 64-bit do kit | Bytes e bit/s | 5 s / 60 s | Tratar reset/wrap; não equivale à cobrança |
| Consumo/franquia/ciclo da linha | Portal, relatório ou API contratada | Bytes/GB, datas, estado | Manual na PoC / conforme contrato | Registrar atraso; não presumir API ou quota individual em pool |
| Sonda LAN local | Computador a bordo → gateway/dispositivo | RTT, enviados/recebidos | 1 s em ensaio / a definir | Mede LAN, não cobertura 4G |
| Sonda Internet local | Computador a bordo → endpoint autorizado via 4G | RTT/perda e bytes | 1 s em ensaio / a definir | Inclui operadora, sem VPN |
| Sonda VPS → peer/LAN N | Zabbix via VPN | RTT/perda | 30 s / 60 s | Inclui celular e VPN, sem diagnóstico isolado de causa |
| WireGuard | Host/roteador | Idade handshake, bytes | 30 s / 60 s | Somar rota e serviço funcional |
| CPU/RAM/uptime | SNMP/API suportada | %, bytes, s | 30 s / 60 s | Inventário real, sem capacidade presumida |
| Energia/temperatura | Sensor ou health suportado | V, A, W, °C | 60 s / 60 s | Tensão sozinha não é estado de carga |
| Alarme/vídeo/aplicação | Teste funcional autorizado | Tempo, resultado, bytes | Por ensaio/evento | Porta TCP acessível não comprova proteção/gravação |
| NOC/banco/disco/coletor | Métricas internas | Fila, idade, bytes/% | 30–60 s / 60 s | Preservar coleta já instalada |

Frequências são propostas; medir bytes consumidos por coleta, VPN/keepalive e logs. Perfil de 5 s só em ensaio com orçamento; reduzir/agrupar leituras quando necessário e registrar nova resolução. A fonte LTE depende do modelo: [documentação MikroTik LTE](https://help.mikrotik.com/docs/spaces/ROS/pages/30146563/LTE), consultada em 29/09/2026, é referência para modelos compatíveis, não garantia para qualquer modem.

## Fontes, cálculos e conciliação

Preferir leitura autenticada/cifrada por VPN e template oficial compatível; API com TLS validado e privilégio mínimo quando suportada. Se o modelo não expuser dado essencial, selecionar outra instrumentação ou manter pendência explícita. Nunca abrir gerência na WAN para facilitar coleta.

`Vazão (bit/s) = 8 × (contador_atual − contador_anterior) / Δt_real`

Reset/wrap sem tratamento invalida o delta. Contagem de sessão do modem não é consumo mensal persistente. Guardar baseline por ciclo, reinícios e horário; conciliar com a operadora, registrando unidade, atraso e diferença. Franquia faturada tem a fonte definida no contrato; estimativa local serve ao diagnóstico e alerta preventivo.

`Perda ICMP (%) = 100 × (enviados − recebidos) / enviados`

Janela sem envio não tem perda calculável. TCP connect não fornece perda ICMP nem disponibilidade de aplicação. Percentis exigem amostras brutas; não calculá-los sobre médias horárias.

## Ensaios MON-01/02/03 e DATA-01

Comparar leitura direta, interromper credencial/caminho/coletor separadamente, provocar reset em bancada e conferir estados/timestamps. Diferenciar falhas de LAN, registro celular, sessão/APN, DNS, Internet, VPN, aplicação e NOC. A VPS sem acesso ao barco não consegue concluir qual dessas camadas falhou sem evidência adicional.

Host local registra ensaio mesmo sem WAN; buffer persistente embarcado em produção é capacidade a selecionar, não existente. Guardar bruto e agregações separadamente. Relatório da operadora atrasado aparece como atrasado. Telemetria privada e dados de faturamento seguem retenções próprias.

## Bateria, fumaça e bomba — proposta IoT de 29/09/2026

Demanda confirmada; [contrato detalhado, sensores e fontes](../01-architecture/IOT_MONITORING_RESEARCH.md). Cadastrar V/A/W/Ah/SoC com validade, alarme de fumaça, corrente/partidas/duração da bomba, nível alto proposto e estado de comandos. Metas locais de 1 s e publicação agrupada de 5 s são sujeitas a ensaio; eventos seguem imediatamente, com timestamp e idade explícitos. Sensor em repouso tem política própria, sem exigir polling contínuo.

Não apresentar SoC como medida direta/saúde da bateria, fumaça como ppm ou corrente do motor como prova de vazão. Broker/ingestão MQTT e buffer ainda dependem de implantação; dados antigos não voltam como atuais. IOT-01 a IOT-05 complementam MON-01/02/03 e DATA-01.
