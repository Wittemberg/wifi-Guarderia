# Alertas, painéis e estados operacionais

Estado: política inicial proposta, a calibrar no piloto. Destinatários, plantão e canais reais permanecem em `OPEN-13`.

## Painéis

| Painel | Público | Conteúdo |
|---|---|---|
| Operação diária | Operador | Internet, core, AP e barcos; idade do dado e incidentes |
| PoC RF | Técnico | RSSI, taxa, perda local, throughput e marcações de orientação |
| Diagnóstico WAN/VPN | Técnico | Sonda VPS/core, handshake, perda externa e tráfego |
| Saúde NOC | Técnico | Filas, erros de coleta, DB, disco, backups e notificações |
| Histórico do barco | Operador autorizado | Eventos e métricas do barco, sem dados de outros clientes |

Aplicar o [padrão de apresentação](../../witteberg-development-standards/UX_AND_WRITING.md). Sem dados e manutenção precisam ser visualmente distintos de normal. Toda visualização informa última atualização, período e origem. A linha do RSSI deve deixar lacunas onde não houve coleta.

## Regras propostas

| Condição | Janela de disparo | Severidade operacional | Recuperação |
|---|---|---|---|
| Coletor sem atualização | > 3 intervalos + tolerância de 15 s | P1; P0 se central inteira cega | 3 coletas válidas |
| Core inacessível por sonda | 3 falhas consecutivas em 30 s | P0 | 3 sucessos consecutivos |
| AP inacessível com core acessível | 3 falhas consecutivas | P0 compartilhado | 3 sucessos |
| Barco inacessível com caminho comum saudável | 3 falhas consecutivas | P1; elevar conforme contrato | 3 sucessos |
| Perda local > 2% | Janela de 5 min com sondas suficientes | P1 | < 1% por 10 min |
| RSSI abaixo de −75 dBm | 60 s de dados válidos | P1 técnico | Acima de −70 dBm por 120 s |
| Disco NOC > 75% / > 90% | 10 min / 2 min | P1 / P0 | < 70% / < 85% |
| Backup sem sucesso > 26 h | Uma avaliação confirmada | P1; P0 se nenhuma cópia válida | Backup íntegro confirmado |
| Falha de entrega de alerta | Retry limitado com backoff | P1/P0 conforme impacto | Entrega confirmada |

Limiares de rádio são valores iniciais de investigação, não limites físicos universais. Alarmes de invasão/incêndio são eventos da solução de segurança e não devem herdar debounce de monitoramento de rede.

## Correlação e deduplicação

Fingerprints por site/equipamento/tipo. Se core/WAN cair, gerar incidente pai e suprimir tempestade de notificações dos barcos dependentes, preservando suas métricas e eventos. A queda da VPN não prova que todos os barcos desligaram. Confirmação de camada local exige sonda local ou visita.

Manutenção silencia somente notificação conforme política, com início/fim e responsável; coleta continua. Reconhecimento não encerra o incidente. Recuperação confirmada encerra condição e registra duração. Cooldown inicial de 10 min para repetição do mesmo aviso, sem suprimir agravamento.

## Notificação

Mensagem deve dizer evento, impacto, evidência, última observação e responsável pela próxima ação. Exemplo de formato, sem dados medidos: “Barco [ID] sem comunicação. Última coleta [horário]; base [estado]. Operação deve verificar alimentação e rádio.” Nunca incluir segredo, imagem ou telefone de outro cliente.

Configurar primeiro um canal de teste autorizado pelo usuário, registrar entrega e falha, e só depois ativar destinatários operacionais. Nenhuma notificação foi enviada nesta fase documental.

## Disponibilidade do monitoramento

Kuma na mesma VPS não detecta sua própria indisponibilidade de forma independente. Monitor externo autorizado ou checagem fora da VPS deve supervisionar o NOC; origem e destinatário ainda a definir. Sem essa segunda observação, registrar a limitação no aceite.
