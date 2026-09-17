# Backup e restauração

Estado: backup local criptografado e restauração isolada implantados; envio diário S3 e restauração isolada a partir dele validados; recuperação integral ainda não homologada. Na correção Prometheus foram criadas cópias protegidas da configuração, conforme [procedimento de retorno](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md); elas não substituem backup dos bancos/volumes. Responsável: administrador.

## Objetivos de recuperação

Metas iniciais sujeitas a ensaio: configurações e NOC com RPO de 24 h; RTO do NOC de 4 h depois da disponibilidade de VPS substituta e credenciais. Mudança de configuração exige backup antes e depois, reduzindo perda entre backups diários. Esses objetivos não equivalem a SLA de vigilância ou de Internet.

## Escopo

| Componente | Conteúdo | Frequência | Método |
|---|---|---|---|
| PostgreSQL Zabbix | Configuração, usuários, métricas e eventos | Diária e antes de upgrade | Dump lógico consistente, versão compatível |
| Grafana | Banco/config, dashboards, provisioning, plugins | Diária e antes de mudança | Backup consistente conforme backend |
| Kuma | Banco e configuração | Diária | Método suportado pela versão; parar para cópia se necessário |
| WireGuard | Configuração, pares e chaves | Diária e toda mudança | Cópia cifrada com permissões preservadas |
| RouterOS | Export revisado e backup protegido | Antes/depois de mudança e diário quando automatizado | Export legível + backup compatível com equipamento |
| Host/orquestração | Manifestos, firewall, versões, rede, volumes | Toda mudança | Git sanitizado + cópia privada dos valores reais |
| Evidências PoC | Dados brutos, marcações, relatórios | Ao fim de cada sessão | Arquivo privado com hash e metadados |

Retenção local implantada: união de 7 diários, 4 semanais e 3 mensais por períodos com cópia válida. Retenção S3: expiração da versão atual em sete dias, configurada pelo usuário, com cabeçalhos de expiração conferidos em um backup e seu recibo. As cópias semanais/mensais longas são locais. Snapshot do provedor é complementar, não única cópia. [Evidências e limites](../06-validation/BACKUP_AUTOMATION.md#retenção-externa-de-sete-dias--confirmação-e-consulta).

## Execução do backup do banco

Identificar exatamente container/serviço e database; não selecionar o primeiro container cujo nome contenha `postgres`. Executar `pg_dump` com formato custom e credencial segura. Há duas opções válidas: gravar no volume de backup montado no container ou transferir explicitamente o arquivo do container para o host. Não presumir que `/tmp` dentro do container é `/tmp` no host.

Não usar PTY/TTY para despejar binário em stdout. Se houver transferência binária, usar mecanismo que preserve bytes e conferir hash de origem/destino. Registrar código de saída, tamanho, início/fim, versão do cliente e destino. Testar listagem de conteúdo com `pg_restore --list`; isso não substitui restauração real.

## Integridade e armazenamento

Enviar cópia cifrada para destino privado com credencial de menor privilégio. Calcular SHA-256 e conferir após transferência. Reter último backup válido mesmo se o job diário falhar. Não rotacionar todas as cópias antes de confirmar nova cópia íntegra. Monitorar idade, integridade, ausência e falha de transferência.

Um arquivo maior que zero não comprova restauração. Nunca colocar dump, `.env`, backup RouterOS ou chave em Git; a cópia sanitizada de configuração não substitui backup completo.

## Restauração BAK-01 em ambiente isolado

1. Selecionar cópia e manifesto de versões; validar checksum, acesso e chave.
2. Preparar destino isolado sem conectar clientes nem enviar notificações reais.
3. Restaurar serviços base e redes usando manifesto correspondente.
4. Restaurar banco em database vazio/isolado compatível e verificar erros.
5. Restaurar Grafana/Kuma e configuração, respeitando consistência do backend.
6. Restaurar secrets/WireGuard de forma protegida; evitar duas instâncias ativas com a mesma identidade.
7. Verificar login, hosts/templates, eventos, dashboards, retenção e uma coleta de alvo de teste autorizado.
8. Validar reinício e persistência; medir tempo total e ponto mais recente recuperado.
9. Registrar hashes, versões, resultados e desvios de RPO/RTO. Só depois planejar eventual substituição do ambiente operacional.

## Recuperação de equipamento

Validar modelo/versão antes de restaurar backup binário RouterOS. Para modelo diferente, reconstruir configuração a partir de template/export revisado em bancada. Reconciliar MAC, chaves, certificados, interfaces e VLANs. Testar recuperação local antes de enviar equipamento ao barco.

## Frequência de ensaio

Primeira restauração antes da PoC; repetir trimestralmente e após mudanças de banco/backup. Resultado reprovado deixa prontidão operacional pendente, mesmo que o job diário esteja verde.

## Backups locais WireGuard existentes — 16/09/2026

A preparação do hub salvou regras IPv4/IPv6, rotas e inventário em armazenamento privado. Antes de cadastrar o notebook, foram copiados novamente wg0.conf, rotas e regras; identificador `wireguard-preflight/notebook-20260916T200122Z`. A configuração ativa foi persistida com modo 600; serviço habilitado no boot.

Essas cópias locais não comprovam cifragem off-site, agendamento diário, backup pós-mudança independente ou restauração. A cópia anterior ao notebook restaura o estado sem esse peer; conferir mudanças posteriores antes de usá-la. Essas cópias históricas isoladamente não homologam BAK-01; os ensaios posteriores de restauração estão registrados abaixo, e RPO/RTO integrais seguem pendentes. Ver [retorno específico e evidências](../06-validation/NOTEBOOK_VPN_VALIDATION.md).

Auditoria e primeiro ensaio executados em 16/09/2026: backups locais de configuração, SQLite e PostgreSQL produzidos, restauração dos bancos e inicialização/reinício das cópias Grafana/Kuma validados. BAK-01 parcial; backup integral e off-site pendentes. Essa foi a condição da auditoria inicial; volumes de Grafana/Prometheus posteriormente corrigidos. [Resultados, plano de migração e limites](../06-validation/PERSISTENCE_BACKUP_AUDIT.md).


## Rotina implantada — 16/09/2026

[Resultados medidos e limites](../06-validation/BACKUP_AUTOMATION.md). Implementação sanitizada: [backup](../../scripts/operations/guarderia_backup.py), [envio S3](../../scripts/operations/guarderia_s3.py), [serviço](../../scripts/operations/guarderia-backup.service) e [timer](../../scripts/operations/guarderia-backup.timer).

Na VPS, script executável em `/root/guarderia-ops/backup.py`; arquivos privados em `/root/guarderia-backups`. Chave em `recovery.key`, modo 600; não imprimir, versionar ou enviar junto ao arquivo criptografado. O usuário confirmou que guardou uma cópia fora da VPS. Ainda falta testar a recuperação com essa cópia externa; o ensaio automatizado usou a chave local.

Comandos de operação, como root:

```bash
systemctl list-timers guarderia-backup.timer
systemctl start guarderia-backup.service
journalctl -u guarderia-backup.service --no-pager -n 60
python3 /root/guarderia-ops/backup.py status
python3 /root/guarderia-ops/backup.py verify
python3 /root/guarderia-ops/backup.py restore-test
```

O comando status retorna erro se a última tentativa falhou ou a última cópia válida tem 26 horas ou mais. Não há notificação externa configurada. O timer executa às 03h15 de São Paulo, com variação de até cinco minutos. Restauração é um ensaio explícito; não é executada diariamente. Repetir trimestralmente e após mudanças relevantes.

A rotina pausa individualmente Grafana, Prometheus, Kuma, Portainer e Traefik para capturar seus volumes, retomando cada processo após a cópia. Limite da cópia pausada: 45 segundos; a primeira execução ficou abaixo de um segundo por serviço. Dump PostgreSQL usa banco online. Em erro, conjuntos incompletos permanecem privados para diagnóstico e não entram na retenção de cópias válidas; revisar espaço e resíduos de ensaios falhos.

O status local registra sucesso apenas após descriptografia e conferência do manifesto. Se o envio S3 estiver habilitado e falhar, o job retorna falha, preservando a cópia local válida. Retenção local remove somente arquivos com recibos reconhecidos no diretório archives; nunca usar prune em volumes de produção como limpeza de backup.

## Configuração S3 implantada

Destino informado: `s3://wifi-guarderia-bkp/guarderia/vps/`, região `us-east-1`. Configuração privada sem segredos em `/root/guarderia-ops/s3-config.json`; perfil `guarderia-backup`. Política de permissões preparada em `/root/guarderia-ops/aws-backup-policy.json`.

Configurar a identidade diretamente no terminal da VPS, sem colar chaves em chat:

```bash
/root/.local/bin/aws configure --profile guarderia-backup
```

Usar região us-east-1. Preferir credenciais temporárias gerenciadas quando disponíveis; credencial temporária inserida manualmente expira e exige renovação para execução não assistida. O perfil foi configurado pelo usuário e validado no envio/download. A política não autoriza apagar objetos nem configurar lifecycle. O envio diário está habilitado após comparação de SHA-256 e restauração isolada a partir do S3.

```bash
python3 /root/guarderia-ops/s3_backup.py
```

O script não envia recovery.key. Conferir a exclusão futura e o alcance da regra de sete dias, decidir sobre versionamento e testar a chave externa antes de homologar BAK-01. A restauração externa foi testada a partir de download do S3. Para repetir o ensaio, usar `python3 /root/guarderia-ops/s3_backup.py --restore-test`. Preservar a região e os digests registrados; sem imagens locais, a reconstrução também depende de acesso aos registries.

Atualização de custódia: o usuário confirmou a cópia da chave de recuperação para fora da VPS. O conteúdo da cópia externa não foi recebido nem conferido pelo assistente; teste de recuperação usando essa cópia continua pendente. As permissões de envio/download foram validadas. O bucket foi observado com versionamento desabilitado; a expiração de sete dias foi configurada pelo usuário. Arquivos externos são expirados pelo lifecycle S3, independentemente da rotação local. GetBucketLifecycleConfiguration foi negado, mas HeadObject mostrou expiração no backup e no recibo; não afirmar que a exclusão já ocorreu.


## Verificação operacional da retenção

Depois do prazo de expiração informado pelo S3, conferir a ausência do objeto por uma consulta autorizada e registrar a evidência; erro de autorização não comprova exclusão. Conferir também que há cópia recente válida. Não antecipar a validação apagando backups manualmente. O cabeçalho de expiração observado em 16/09 de São Paulo indica 25/09/2026 00:00 UTC para o conjunto consultado; a remoção pode ocorrer depois.

Se uploads falharem durante a janela externa, a quantidade de pontos recuperáveis pode diminuir até não haver cópia no S3. O timer e o status de falha existem; alertas SES/Telegram externos foram implantados e validados conforme [operação](../06-validation/BACKUP_ALERTS.md). Acompanhar idade e resultado do job conforme RB-11 em [runbooks](RUNBOOKS.md), sem anunciar RPO de 24 horas como homologado.

A configuração arquivada inclui a unidade guarderia-panel-firewall.service, além dos scripts operacionais, manifestos e snapshots das regras. Em recuperação, reconciliar caminhos, interfaces e origens autorizadas antes de habilitar o filtro; backup não implica teste de reboot. [Retorno da mudança](../06-validation/VPS_ACCESS_VALIDATION.md).
