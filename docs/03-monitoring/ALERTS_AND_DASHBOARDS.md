# Alertas, painéis e estados operacionais

Revisão de 29/09/2026: política embarcada proposta, sem dashboards LTE ou alertas de SIM implantados. Alertas de backup SES/Telegram já têm [evidência própria](../06-validation/BACKUP_ALERTS.md); não comprovam notificação de equipamentos ou integração da operadora. Plantão e destinatários embarcados seguem em OPEN-13.

## Painéis propostos

| Painel | Conteúdo |
|---|---|
| Frota | Estado por barco: Internet, VPN, última coleta, incidente e operadora lógica |
| Linha e consumo | Ciclo, franquia/plano, bytes local/operadora, atraso e projeção claramente identificada |
| PoC celular | Sinal suportado, posição/orientação lógica, upload/download, RTT/perda e reconexões |
| Diagnóstico | LAN, registro 4G, sessão de dados, DNS, Internet, VPN e aplicação com fonte explícita |
| NOC | Coletor, fila, banco, disco, backup e entrega de alertas |
| Barco | Somente dados do barco para usuário autorizado; filtros visuais não são autorização |
| IoT por barco | Tensão, corrente, SoC válido, fumaça, corrente/ciclos da bomba, nível alto e idade de cada dado; integração pendente |

Toda visualização informa fonte, período e atualização. Usar [estados de apresentação](../../witteberg-development-standards/UX_AND_WRITING.md); sem dados, manutenção e erro de autenticação ficam distintos de normal.

## Regras iniciais a calibrar

| Condição | Disparo proposto | Recuperação |
|---|---|---|
| Coletor sem atualização | Mais de 3 intervalos + 15 s | 3 leituras válidas |
| Barco inacessível pela VPN | 3 falhas consecutivas da sonda | 3 sucessos e aplicação/caminho conferidos |
| Registro ou sessão celular ausente | Estado direto persistente por 60 s, quando há coleta local | Registro e sessão restabelecidos |
| Degradação de aplicação/Internet | Meta da PoC/contrato violada em janela válida | Meta restabelecida na janela acordada |
| Franquia utilizada | 70%, 85% e 95% como alertas propostos | Novo ciclo ou alteração contratual confirmada |
| Projeção excede franquia | Dados suficientes e hipótese de consumo identificada | Projeção volta ao orçamento; não confundir com cobrança real |
| Portal/relatório de consumo atrasado | Prazo contratado + tolerância aprovada | Fonte atualizada |
| Disco NOC | > 75% por 10 min / > 90% por 2 min | < 70% / < 85% |

Severidade depende do serviço afetado: perda de contato de um kit pode ser crítica conforme contrato, sem provar falha do alarme local. Não usar RSSI WiFi como limiar de sinal LTE. Alertas de alarme patrimonial seguem o serviço de segurança e seus próprios tempos.

## Correlação

Para IoT, aplicar o [contrato de métricas](METRICS.md) e as [metas da pesquisa](../01-architecture/IOT_MONITORING_RESEARCH.md): leituras periódicas atrasadas após 15 s, gateway sem comunicação após 90 s e política própria para detector de fumaça adormecido. Esses critérios específicos prevalecem sobre o limiar genérico do coletor. Fumaça e nível alto geram evento imediato; limites de bateria, corrente e duração da bomba dependem do inventário e perfil medido. Não definir um único limiar de tensão/SoC para todas as baterias.

Exibir separadamente comando solicitado, aceito e efeito físico. Pedido sem corrente e nível alto persistente exigem tratamento, mas não identificam sozinhos a causa. ACK não significa drenagem. Reconhecer um alerta não silencia detector nem desliga o automático. Acionamento remoto requer serviço autorizado próprio e registro auditável; o dashboard de consulta não concede permissão de comando.

Fingerprint por barco/linha lógica/tipo. Incidente de modem/SIM de A não suprime incidentes de B. Falha confirmada do hub/coletor pode agrupar notificações dependentes preservando eventos e lacunas. Falhas simultâneas na mesma operadora são hipótese de causa comum até confirmação, não diagnóstico automático de célula/operadora.

VPN ausente não significa modem desligado. Comparar sonda local, registro de dados e portal quando disponíveis. Sem evidência adicional, informar “sem comunicação; causa não determinada”. Manutenção tem responsável e prazo, silencia apenas avisos previstos e mantém coleta. Reconhecimento não é recuperação.

## Consumo e notificações

Contadores locais podem alertar antes do relatório da operadora, mas mostrar fonte e diferença. Não executar suspensão automática, troca de plano, compra de pacote ou bloqueio de tráfego crítico sem política autorizada e ensaiada. Perda de franquia pode eliminar a própria gerência remota.

Formato: “Barco [ID] sem comunicação desde [horário]. Última evidência [fonte/estado]. Verificar caminho 4G/VPN e alimentação; causa ainda não determinada.” Destinatários e envio de teste exigem canal autorizado. Nenhum envio foi realizado nesta revisão documental.

Kuma na VPS não observa de forma independente a queda do próprio host. O monitor externo de backup já implantado observa heartbeat, mas não comprova conectividade celular ou disponibilidade de cada aplicação.
