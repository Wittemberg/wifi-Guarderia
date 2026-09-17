# Alertas externos de backup e ausência de heartbeat

Estado em 17/09/2026: implantados e ativos. Usuário confirmou recebimento por e-mail e Telegram, incluindo recuperação. Primeira avaliação automática observada na AWS com estado saudável. Esta automação complementa o backup existente; não é um ensaio de restauração integral.

## Comportamento e critérios

| Condição | Comportamento |
|---|---|
| Publicação normal | VPS publica heartbeat no S3 a cada cinco minutos; EventBridge executa Lambda a cada cinco minutos |
| Ausência de heartbeat por pelo menos 15 minutos | Alerta nos dois canais na avaliação seguinte; pode levar até mais um intervalo de cinco minutos |
| Falha no backup | OnFailure do serviço publica estado; Lambda notifica na avaliação seguinte. O heartbeat periódico também verifica o resultado do serviço |
| Última tentativa finalizada sem cópia S3 atual verificada | Alerta; etapa intermediária de um backup ainda em execução não causa falso positivo |
| Último registro de verificação S3 com pelo menos 26 horas | Alerta mesmo se o backup estiver em execução |
| Incidente persistente | Repetição por canal a cada seis horas; mudança da condição pode gerar novo aviso |
| Recuperação | Aviso somente aos canais que receberam o incidente |

Ausência de heartbeat não identifica sozinha a causa: VPS, conectividade, credenciais ou publicador podem falhar. A idade do heartbeat usa LastModified do S3, não o relógio do payload da VPS. A idade do backup usa o registro de download/hash verificado publicado pela VPS; a Lambda não baixa nem restaura arquivos de backup.

## Componentes implantados

Stack CloudFormation guarderia-backup-alerts em us-east-1: Lambda guarderia-backup-watchdog (Python 3.12, 128 MB, timeout 60 s), role dedicada, log group com retenção de 14 dias e regra EventBridge a cada cinco minutos. Agenda inicialmente desativada durante os testes, habilitada após os testes de envio e recuperação.

Na VPS: heartbeat.py em guarderia-ops; guarderia-heartbeat.service/timer instalados e timer habilitado. Drop-in alerts.conf em guarderia-backup.service.d publica heartbeat via OnFailure. O timer e os arquivos de configuração foram incluídos na rotina de backup. Não há alterações nos filtros de acesso ou reinício da stack.

Dados operacionais no prefixo guarderia/vps/monitor/ do bucket de backup existente: heartbeat.json, notification-state.json e notification-test-state.json. Estado de teste separado do estado real; os ensaios não alteraram backups nem derrubaram a VPS. Estado de produção é regravado em cada avaliação; continua sujeito ao lifecycle S3 existente.

## Canais, permissões e segredos

SES usa remetente operacional e destinatário definidos pelo usuário; dados reais ficam nos parâmetros privados e na AWS. Ambos verificados, envio habilitado e conta ainda em sandbox. Usuário confirmou primeiro e-mail enviado pela VPS e, depois, os envios integrados pela Lambda. Não foi solicitado acesso de produção nem alterado DNS.

Telegram: bot dedicado e conversa privada vinculados pelo usuário com código aleatório. Token local em arquivo modo 600, diretório modo 700, fora do Git e do conjunto de configurações arquivado pelo backup. Cópia na AWS em SSM SecureString, parâmetro /guarderia/alerts/telegram; a Lambda acessa somente esse parâmetro. Token não foi exibido em logs, argumentos ou conversa. O helper recusa bot com webhook já configurado e não escolhe uma conversa arbitrária.

A permissão CloudFormation inicialmente negada foi adicionada pelo usuário. A role operacional é distinta da identidade administrativa usada para implantar. Ela lê os objetos de monitoramento, grava apenas o estado de notificações, consulta o parâmetro Telegram e envia SES limitado ao remetente e destinatário previstos. ListBucket do bucket é permitido para distinguir objeto ausente; não há leitura de arquivos de backup pela role Lambda. A correção SES incluiu também a identidade do destinatário no Resource e manteve condições explícitas de FromAddress/Recipients.

A política administrativa de implantação foi preparada com recursos delimitados e anexada pelo usuário; não foi removida automaticamente. Ela permite modificar a role dedicada e deve ser tratada como permissão administrativa, distinta das permissões necessárias ao heartbeat. Revisão ou retirada após implantação é decisão separada.

## Validação realizada

- Dez testes locais aprovados: estado saudável, heartbeat ausente/antigo, falha, limite de 26 horas, execução intermediária, resultado systemd de erro, deduplicação independente e recuperação por canal.
- Stack criada com sucesso e configuração mantida pelo CloudFormation.
- Execução real sem incidente retornou ok antes e depois dos testes.
- Lambda executou testes sintéticos de ausência de sinal, falha de backup, atraso e recuperação. SES e Telegram aceitaram os envios; usuário confirmou recebimento de ambos, incluindo recuperação.
- Durante a primeira execução integrada, SES negou envio pela role da Lambda à identidade do destinatário. Erro identificado e corrigido; teste repetido com sucesso. Telegram já enviado não foi repetido enquanto somente o e-mail era retentado.
- Pós-teste de 17/09/2026 03:08:16 UTC: stack UPDATE_COMPLETE, agenda ENABLED/rate(5 minutes), heartbeat com cerca de 158 s, estado ok, timer local ativo/habilitado, serviço com Result=success/ExecMainStatus=0 e OnFailure configurado. O estado foi atualizado depois da última invocação manual, comprovando avaliação automática neste intervalo.

Evidências privadas no diretório indicado por /root/guarderia-evidencias/alerts-current.txt: histórico de invocações, erro SES e correção, estado operacional, aceite humano e relatório do backup posterior. Não versionar destinatários reais, token ou identidade AWS.

## Limites e operação

Um alerta é enviado por canal e registrado depois; falha entre envio e persistência pode causar duplicação. A falha de um canal não impede tentativa no outro. Reenvio segue o estado individual e a política de retentativa do agendamento. Uma mudança de motivo gera nova notificação; não é garantia de exatamente uma entrega.

O monitor opera fora da VPS, mas depende da AWS. Indisponibilidade da própria AWS ou da função monitoradora, erros de leitura do S3/SSM e falhas de ambos os canais não são cobertos por um segundo monitor independente nesta etapa. Consultar CloudWatch/estado de notificações em investigação. Não alegar monitoramento integral da saúde das aplicações, UDP ou IPv6 com este heartbeat.

A infraestrutura gera consumo AWS de Lambda, EventBridge, S3, logs, SSM e SES conforme serviços utilizados. Não foi homologado custo mensal, SLA, RPO ou RTO a partir deste ensaio.

Para conferir estado, no terminal da VPS:

```bash
python3 /root/guarderia-ops/alert_operations_postcheck.py
systemctl status guarderia-heartbeat.timer --no-pager
journalctl -u guarderia-heartbeat.service --no-pager
```

## Retorno e manutenção

Para suspender notificações, primeiro desabilitar a agenda AWS e aguardar UPDATE_COMPLETE; depois, se necessário, parar o heartbeat. Parar somente heartbeat mantendo a agenda ativa gera alerta de ausência de sinal.

```bash
python3 /root/guarderia-ops/deploy_alerts.py disable
python3 /root/guarderia-ops/deploy_alerts.py status
systemctl disable --now guarderia-heartbeat.timer
```

O drop-in OnFailure permanece enquanto não for removido; pode publicar estado em falha do backup mesmo com timer desabilitado. Para retorno completo do publicador, remover somente o drop-in alerts.conf e recarregar systemd após preservar uma cópia. Não remover a rotina de backup nem regras de acesso. Exclusão da stack e do parâmetro Telegram são operações separadas; não apagar bucket nem backups.

Para alterar o monitor, editar os fontes de scripts/operations/alerts, gerar o template privado com build_template.py e atualizar pelo helper deploy_alerts.py; não colar tokens em código/template. Os eventos test_case são aceitos apenas via invocação autorizada da Lambda e gravam estado separado; não há endpoint público de testes.

Fontes: [criação de bot Telegram](https://core.telegram.org/bots/tutorial), [sandbox SES](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html), [Lambda em CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-lambda-function.html), [agendamento EventBridge](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-events-rule.html) e [permissões SES](https://docs.aws.amazon.com/ses/latest/dg/control-user-access.html).

Backup posterior à implantação concluído: backup-20260917T030811Z.gpg enviado ao S3 e baixado com hash verificado. Pós-teste de 17/09/2026 03:09:54 UTC confirmou Result=success/ExecMainStatus=0, doze serviços 1/1 e três alvos UP. Arquivos e unidades do heartbeat incluídos no backup; token Telegram continua separado, com cópia no SSM SecureString.
