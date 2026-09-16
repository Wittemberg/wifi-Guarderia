# Backup e restauração

Estado: política de backup integral e restauração ainda não homologada. Na correção Prometheus foram criadas cópias protegidas da configuração, conforme [procedimento de retorno](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md); elas não substituem backup dos bancos/volumes. Responsável: administrador.

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

Retenção proposta para backups: 7 diários, 4 semanais e 3 mensais, ajustada ao volume e necessidade. Manter cópia fora da VPS e testar chave de recuperação. Snapshot do provedor é complementar, não única cópia.

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
