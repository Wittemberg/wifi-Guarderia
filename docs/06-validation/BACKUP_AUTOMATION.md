# Backup automático e restauração isolada

Execução iniciada em 16/09/2026, horário de São Paulo. Escopo autorizado: consolidar a migração de Grafana/Prometheus, automatizar backups e testar recuperação. Destino externo informado pelo usuário: bucket `wifi-guarderia-bkp`, região `us-east-1`.

## Implementado e medido

- Migração anterior confirmada: Grafana usa `guarderia_grafana_data` e Prometheus usa `guarderia_prometheus_data`. Ambos passaram por recriação de tarefa; banco Grafana íntegro e três alvos Prometheus UP no pós-teste da migração. Contagens Grafana: zero dashboards no banco, um usuário e um datasource; não afirmar existência de dashboards configurados.
- Manifesto local e arquivo da stack monitor no volume do Portainer reconciliados com os volumes, restrição ao nó atual, ordem stop-first e imagens efetivas por digest. Arquivos anteriores protegidos; não houve redeploy integral da stack. A interface autenticada do Portainer não foi testada nesta migração; o login de produção foi posteriormente confirmado nas etapas de acesso e reboot.
- Backup local criptografado com GPG/AES-256. A chave de recuperação fica em arquivo privado separado, modo 600, e não integra o arquivo enviado. O usuário confirmou a cópia da chave para fora da VPS; o conteúdo dessa cópia externa não foi recebido nem testado pelo assistente.
- Cinco volumes capturados com processos pausados e retomados em finally; PostgreSQL 14 e 15 com dumps lógicos e objetos globais. A captura é consistente por serviço, não um snapshot simultâneo de toda a stack. TSDB inclui WAL/head.
- Configurações de monitoramento, WireGuard, manifestos, automação, inventários de serviços e regras/rotas incluídos. Estado interno do Swarm, imagens Docker completas, host inteiro e equipamentos RouterOS não integram uma imagem recuperável de VPS.
- Cada arquivo do conjunto tem tamanho e SHA-256 no manifesto interno. Antes de aceitar o backup, a rotina descriptografa o arquivo, valida sua integridade criptográfica e confere todos os hashes. Uma cópia com corrupção induzida foi rejeitada.
- Exclusão de cópias antigas limitada ao diretório e aos arquivos reconhecidos da rotina, após uma nova cópia validada. Retenção por união dos últimos sete dias com cópia, quatro semanas com cópia e três meses com cópia; vários backups no mesmo dia podem ser consolidados no mais recente. Não representa sete execuções se houver dias sem backup.
- Serviço `guarderia-backup.service` e timer diário às 03h15 de São Paulo, com até cinco minutos de atraso aleatório e recuperação de disparo perdido. O teste isolado precisa passar antes de instalar o timer. A rotina usa trava para evitar duas operações simultâneas.

## Primeiro conjunto e resultados

Identificador: `backup-20260916T235826Z.gpg`. Arquivo criptografado de **191.322.479 bytes**, 19 arquivos internos de dados/configuração, mais o manifesto. Duração medida do backup: **77,601 s**. Hash e recibo completos permanecem privados. A retenção pode substituir este conjunto por uma execução posterior do mesmo dia; o relatório preserva a evidência histórica do ensaio.

| Serviço | Pausa de captura medida |
|---|---:|
| Grafana | 0,945 s |
| Prometheus | 0,426 s |
| Kuma | 0,098 s |
| Portainer | 0,099 s |
| Traefik | 0,089 s |

Esses intervalos são tempos de pausa do processo na primeira captura; não são medição de indisponibilidade externa ou garantia de duração futura.

| Componente restaurado | Resultado |
|---|---|
| Grafana | Inicialização/reinício isolados e banco SQLite íntegro |
| Prometheus | Inicialização/reinício isolados e TSDB com séries carregadas |
| Kuma | Inicialização/reinício isolados e banco SQLite íntegro |
| Portainer | Inicialização/reinício isolados e API de status respondendo |
| PostgreSQL 14 | Um banco restaurado, zero tabelas públicas |
| PostgreSQL 15/Zabbix | Dois bancos restaurados, zero e 207 tabelas públicas |
| Certificados Traefik | Sete pares certificado/chave compatíveis e não expirados |

Ensaio final completo: **71,683 s**, com as imagens locais de produção, rede none, sem portas publicadas, dados extraídos em diretórios próprios e remoção dos contêineres ao final. Foi corrigida a espera do PostgreSQL para exigir prontidão em TCP local: a primeira tentativa encontrou o servidor temporário da inicialização e falhou durante sua parada. A repetição passou. Nenhum banco de produção foi usado como destino.

Neste ensaio de restauração isolada, não foram testados login humano, notificações reais, aplicação Zabbix conectada ao banco restaurado, negociação TLS dos certificados restaurados, reconstrução integral da VPS, reboot ou recuperação de imagens. Em produção, logins e reboot foram posteriormente validados em [ensaio próprio](VPS_REBOOT_VALIDATION.md), e notificações em [alertas](BACKUP_ALERTS.md); isso não valida essas funções nos componentes restaurados. O ensaio posterior com origem S3 está registrado abaixo. Os tempos medidos não homologam RTO integral nem RPO de 24 horas.

## AWS: envio diário ativado e restauração isolada validada

AWS CLI 2.36.47 instalada em diretório local após validação da assinatura oficial e fingerprint `FB5DB77FD5C118B80511ADA8A6310ACC4672475C`. O instalador foi lido antes da execução.

Envio diário ativo para o prefixo `guarderia/vps/` do bucket informado. A política permite leitura de configuração do bucket, listagem do prefixo e escrita/leitura de objetos para validar download; não permite apagar objetos nem alterar a política do bucket. A rotina exige bloqueio público ativo, confere região, usa TLS e envia somente arquivo GPG e recibo. Após upload, baixa o arquivo e compara SHA-256. Versionamento é observado e registrado; lifecycle remoto não é alterado.

O usuário configurou o perfil `guarderia-backup` diretamente no terminal e aplicou a política solicitada. A falha inicial de GetPublicAccessBlock foi resolvida. Nenhuma credencial foi recebida pelo chat. O bucket foi consultado na região us-east-1, com os quatro controles de bloqueio público ativos. Versionamento observado: **Disabled**. O assistente não alterou o lifecycle; posteriormente o usuário configurou a expiração da versão atual em sete dias, com evidência descrita abaixo. A política da identidade não autoriza excluir objetos nem alterar configurações do bucket.

Em 17/09/2026 00:26:46 UTC (16/09 21:26:46 em São Paulo), o arquivo `backup-20260917T000351Z.gpg` foi enviado ao prefixo acordado. A cópia baixada do S3 correspondeu ao SHA-256 local; o recibo também foi enviado. A restauração isolada partiu de novo download do S3 e repetiu com sucesso os sete componentes da tabela anterior. Descriptografia/restauração/verificações levaram **69,659 s**, sem incluir o download do S3. A chave usada no ensaio foi a cópia local; não houve teste da chave guardada no notebook.

O envio diário foi habilitado depois desse ensaio. O job diário gera e verifica um novo backup local, envia arquivo criptografado/recibo ao S3 e baixa o arquivo para conferir SHA-256. Falha externa faz o job falhar, preservando a cópia local válida. A cópia externa da chave foi confirmada pelo usuário. A retenção externa de sete dias foi posteriormente configurada pelo usuário. A exclusão efetiva, a decisão sobre versionamento, o teste com a chave externa e a reconstrução integral da VPS continuam sem homologação.


## Evidências e limites de homologação

Recibos, status, relatório de restauração e teste negativo ficam privados em `guarderia-backups`; evidências da migração/reconciliação ficam em `guarderia-evidencias`. Caminhos operacionais completos constam no [procedimento](../05-operations/BACKUP_RESTORE.md).

BAK-01 e REQ-19 continuam parciais. OPS-01/REQ-11 têm recriação de Grafana/Prometheus e reboot controlado validados; rollback/recuperação integral continuam pendentes. F2 não está homologada. Integração das RBs e segurança além do escopo TCP IPv4 testado continuam pendentes.

Fontes: [backup Grafana](https://grafana.com/docs/grafana/latest/administration/back-up-grafana/), [instalação e assinatura AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), [práticas de segurança S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html).

Pós-teste em 17/09/2026 00:06:59 UTC (16/09 21:06:59 de São Paulo): execução pelo systemd com Result=success/ExecMainStatus=0, timer enabled/active, 12 serviços 1/1, três alvos UP/sem erro, SSH/Docker/WireGuard ativos e nenhum contêiner temporário de teste. Segunda cópia válida: backup-20260917T000351Z.gpg.

Atualização de custódia: o usuário confirmou a cópia da chave de recuperação para fora da VPS. O conteúdo da cópia externa não foi recebido nem conferido pelo assistente; teste de recuperação usando essa cópia continua pendente. As permissões usadas no upload/download foram posteriormente validadas.

## Validação do ciclo automático completo

Pós-teste de 17/09/2026 00:30:40 UTC (16/09 21:30:40 de São Paulo): serviço systemd encerrado com Result=success e ExecMainStatus=0. O novo conjunto `backup-20260917T002847Z.gpg`, com 195330522 bytes criptografados, foi gerado pelo serviço, enviado ao S3 e baixado com SHA-256 correspondente. Status local registra offsite=true para esse mesmo arquivo. Timer enabled/active; 12 serviços 1/1, três alvos UP sem erro, SSH/Docker/WireGuard ativos e nenhum contêiner de teste restante. Evidência privada: postcheck.json, s3-last.json e recibo do conjunto.

## Retenção externa de sete dias — confirmação e consulta

**Confirmado pelo usuário:** configurou no bucket a expiração da versão atual do objeto após sete dias. **Observado por API em 17/09/2026 00:38:06 UTC (16/09 21:38:06 de São Paulo):** HeadObject retornou uma expiração associada ao lifecycle para o arquivo criptografado e seu recibo.

| Objeto consultado | Última modificação no S3 (UTC) | Expiração informada pelo S3 (UTC) |
|---|---|---|
| backup-20260917T002847Z.gpg | 17/09/2026 00:30:12 | 25/09/2026 00:00:00 |
| backup-20260917T002847Z.json | 17/09/2026 00:30:39 | 25/09/2026 00:00:00 |

A data observada é compatível com sete dias e o arredondamento para a meia-noite UTC seguinte usado pelo S3. A remoção é assíncrona: não prometer exclusão exatamente 168 horas após upload. [Cálculo de prazo](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html), [expiração S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html).

GetBucketVersioning retornou sem status de versionamento, mantendo a observação de bucket não versionado. Nesse estado, a expiração remove o objeto permanentemente. Se o versionamento for habilitado no futuro, será necessário revisar versões não atuais; a regra de expiração da versão atual não substitui essa política.

**Limites:** GetBucketLifecycleConfiguration retornou AccessDenied. Não foram inspecionados todos os filtros, regras, tags ou ações do bucket. A evidência confirma expiração nos dois objetos consultados e a informação de sete dias vem do usuário; não comprova cobertura de todos os objetos nem exclusão futura. Não foi solicitada ampliação de permissão para concluir esta atualização documental. Registro privado: retention-audit.json.

A política local permanece 7 diários/4 semanais/3 mensais por união de períodos com cópia, enquanto o S3 mantém a janela curta de sete dias informada. Cópias semanais/mensais locais não têm retenção longa equivalente no S3. Após perda da VPS, o planejamento de recuperação depende das cópias externas ainda disponíveis; retenção não equivale a RPO ou garantia de sete backups válidos.

Restrições de acesso, reboot e alertas foram posteriormente concluídos. Próximo passo independente da RB951G: preparar recuperação integral em ambiente separado. [Estado consolidado](../00-project/IMPLEMENTATION_STATUS.md). F2 e BAK-01 continuam parciais.

Ciclo posterior à restrição dos painéis: backup-20260917T010621Z.gpg enviado e baixado do S3 com hash verificado; pós-teste de 17/09/2026 01:08:02 UTC confirmou Result=success/ExecMainStatus=0, doze serviços 1/1 e três alvos UP. Unidade systemd do filtro incluída no backup. Teste externo IPv4 e HTTPS pela VPN posteriormente aprovados conforme saída enviada pelo usuário; logins pós-mudança nos quatro consoles confirmados pelo usuário.

Backup posterior aos filtros: backup-20260917T014109Z.gpg gerado, enviado e baixado do S3 com hash verificado. Pós-teste de 17/09/2026 01:42:50 UTC: systemd Result=success/ExecMainStatus=0, doze serviços 1/1 e três alvos UP. Esse ciclo não cancela a reversão automática dos filtros nem substitui nova sessão SSH pela VPN.

Atualização de 17/09/2026: alertas SES/Telegram implantados e ativos na AWS, com heartbeat local e avaliação externa a cada cinco minutos. Ausência de sinal por 15 minutos e última verificação S3 com pelo menos 26 horas geram alerta; falha de backup também detectada. Dez testes locais e ensaios sintéticos integrados aprovados, recuperação recebida e ambos os canais confirmados pelo usuário. Primeira avaliação automática saudável observada. Pendências anteriores de cadastro e permissões foram resolvidas; não tratar registros históricos de preparação como estado atual.

Backup posterior à implantação concluído: backup-20260917T030811Z.gpg enviado ao S3 e baixado com hash verificado. Pós-teste de 17/09/2026 03:09:54 UTC confirmou Result=success/ExecMainStatus=0, doze serviços 1/1 e três alvos UP. Arquivos e unidades do heartbeat incluídos no backup; token Telegram continua separado, com cópia no SSM SecureString.
