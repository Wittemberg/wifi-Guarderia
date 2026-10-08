# Plano de prova de conceito 4G por barco

Revisão de 29/09/2026. **Estado: planejado, nenhum ensaio celular executado.** Objetivo: comprovar Internet individual, gerência remota, funções locais, consumo e viabilidade por barco. RF-01 a RF-05 do enlace terrestre estão substituídos; o histórico permanece na [homologação](HOMOLOGATION.md).

## Preparação e instrumentos

Inventariar modem, SIM/plano/APN e eventual roteador/AP; autorizar instalação e ensaios, preparar backup e recuperação local, definir autonomia e demanda do kit. Homologar coleta embarcada em bancada antes do campo. Usar orçamento máximo de dados por sessão: definir bytes/tempo e interromper tráfego de carga ao atingi-lo, evitando excedente automático.

Computador de teste a bordo registra localmente LAN, Internet celular, VPN, aplicação, energia e horários sincronizados. A sonda local de LAN não mede a rede celular; a sonda VPS via VPN inclui operadora e túnel. Usar endpoint externo autorizado para upload/download, com direção e bytes registrados. Não depender da VPS para conservar evidência durante falha WAN. Não transmitir imagens identificáveis como carga de teste.

## Ensaios propostos

| ID | Execução | Duração/amostra proposta | Evidência |
|---|---|---|---|
| CEL-01 | Bancada: SIM/APN, registro 4G, dados, LAN e VPN simultâneos | 1 h | Modelo/firmware, tecnologia, rotas, logs, bytes |
| CEL-02 | Campo nos locais reais de fundeio, pico e fora de pico | 10 min por posição/horário | Sinal suportado, upload/download, RTT/perda, aplicações |
| CEL-03 | Giro e movimento natural; obstáculos/cabine na condição de uso | Orientações 0/90/180/270° quando seguras; 3 ciclos se viável | Pior caso, lacunas e reconexões; sem manobra insegura |
| CEL-04 | Carga de alarme, consultas de vídeo e navegação prevista | 30 min por perfil, limitado ao orçamento de dados | Demanda, filas/prioridades, CPU, perda, bytes |
| CEL-05 | Permanência, variando horários e condições naturais | 24 h e depois 7 dias | Cobertura de coleta, incidentes e projeção de consumo |
| CEL-06 | Perda/retorno celular, mudança de IP e reboot controlado | 3 ciclos por falha quando viável | Registro 4G, DNS, túnel, aplicação e recuperação |
| CEL-07 | Dois kits com SIMs próprios: falha isolada e carga concorrente | 30 min por cenário | Independência dos barcos e limitações da célula/operadora |
| SIM-01 | Gestão individual de duas linhas de teste; suspensão/reativação se contratadas e autorizadas | Um ciclo por controle contratado | Ação/efeito/prazo em A; B preservada; portal ou atendimento |
| DATA-01 | Conciliar bytes do kit, VPN/vídeo e operadora; alertas/ciclo/franquia | 24 h inicial + fechamento de ciclo | Fonte, atraso, unidade, reset, quota e custo |
| LAN-01 | DHCP/DNS, WiFi/Ethernet, Internet e gerência | 10 repetições funcionais | Tempo/falha por camada |
| ENE-01 | Repouso, transmissão, noite, sirene, reboot e autonomia | Período de autonomia acordado | Wh/Ah, pico e tensão nos terminais |

0° é referência de proa registrada no croqui privado; não precisa apontar para a margem. Os 50–100 m da ideia anterior não são critérios de cobertura celular. Cenários impossíveis ficam não executados, nunca interpolados.

## Critérios de aceite propostos, a aprovar antes do ensaio

| Medida | Critério inicial | Limite de interpretação |
|---|---|---|
| Aplicações | Alarme entregue e consulta de vídeo dentro dos prazos definidos para o kit antes do teste | Prazo depende do serviço/modelo; sem prazo aprovado, aceite pendente |
| Vazão útil por sentido | Pelo menos 1,3 × demanda simultânea medida naquele sentido | Não é SLA nem promessa de velocidade da operadora |
| Perda para endpoint Internet do ensaio | ≤ 2% por janela de 10 min, com enviados/recebidos registrados | ICMP depende do destino; correlacionar com aplicação e não inferir por TCP |
| Latência Internet em repouso | p95 ≤ 150 ms ao endpoint definido | Meta técnica inicial; não reutilizar limites do antigo enlace local |
| Retorno 4G/VPN | Até 180 s após retorno da rede e boot concluído | Medir também tempo total desde energização; falhas sem tempo conhecido ficam inconclusivas |
| Coleta | ≥ 99% das amostras programadas de itens suportados durante janela de conectividade | Relatar separadamente lacunas totais, falhas induzidas e log local |
| Dados | Consumo projetado com margem cabe na franquia aprovada | Projeção identificada; DATA-01 só completo após conciliação do ciclo |
| Isolamento | SEC-01/02 aprovados no hub e kits, incluindo IPv6 | Falha bloqueia multicliente |
| Autonomia | Sem subtensão/reset na carga e duração acordadas | Base em medição do kit, sem usar consumo de rádio antigo |
| Relógios | Desvio ≤ 1 s entre fontes do ensaio | Registrar desvios e impacto na correlação |

RSRP/RSRQ/SINR são diagnósticos quando expostos, sem limiar universal de aceite. Ausência de um campo não vira zero. Falha do modem, SIM, operadora, DNS, VPN, coletor e aplicação exige identificação separada em MON-03.

## Falhas e independência

Induzir, uma por vez e com recuperação preparada: perda 4G do barco A, indisponibilidade do hub, Internet da central NOC, reinício do kit e restrição de linha autorizada. Alarme e gravação locais continuam conforme alimentação independente; Internet de B não deve depender de A. Falha de uma operadora pode atingir ambos e não demonstra dependência entre kits. Não bloquear a única linha remotamente sem acesso local.

## Decisão

O piloto inclui [IOT-01 a IOT-05](../01-architecture/IOT_MONITORING_RESEARCH.md): bancada de bateria/fumaça/bomba, calibração, comandos com falhas induzidas e automático preservado, seguida de energia, latência e consumo no barco. Integrar os bytes ao DATA-01 e a energia ao ENE-01. Nenhuma atuação em bomba em uso é autorizada apenas por este plano; preparar inventário, recuperação e escopo operacional antes do ensaio.

Aprovar por barco, local, operadora/plano, kit e configuração ensaiados, com evidência privada e aceite humano. Restrições devem indicar impacto e teste faltante; item P0 reprovado impede o serviço afetado. Ausência de cobertura exige rever posição/antena/operadora e repetir campo. Um barco aprovado não homologa 20; CAP-01 verifica concorrência, observabilidade e custos de expansão. A PoC não estabelece SLA comercial.
