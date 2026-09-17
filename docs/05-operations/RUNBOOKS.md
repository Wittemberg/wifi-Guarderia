# Runbooks operacionais

Estado: procedimentos de operação, com correção Prometheus já executada e registrada no [runbook específico](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md). Cada execução registra horário, diagnóstico, autorização, mudança e evidência; credenciais ficam fora do registro público.

## RB-01 — Barco sem comunicação

1. Conferir idade da coleta e saúde do próprio NOC.
2. Comparar core, AP e demais barcos; abrir incidente pai se falha compartilhada.
3. Verificar associação RF do barco na base e último evento.
4. Se associado, testar trânsito /30, LAN, rota e ACL; diferenciar DNS de conectividade IP.
5. Se não associado, verificar alimentação por informação disponível e última tensão válida, sem concluir bateria descarregada por ausência de dados.
6. Contatar responsável operacional conforme canal aprovado ou programar inspeção.
7. Após correção, comprovar associação, perda local, aplicação e retomada de coleta; encerrar com causa e duração.

Não reiniciar rádio/core automaticamente por um único timeout. Preservar evidência de flapping e queda de energia.

## RB-02 — VPN com handshake e sem acesso

Comparar AllowedIPs, rotas de ida/retorno, forwarding da VPS, regras Docker, NAT e origem real. Testar VPS→core e central NOC→VPS separadamente. Verificar MTU se ping pequeno funciona e aplicação falha. Não adicionar rota default à VPN como tentativa genérica de correção.

## RB-03 — Métrica RF não suportada

Registrar versão/pacote/modelo e resposta sanitizada; comparar com capacidade documentada. Diferenciar falta de permissão de recurso inexistente. Desativar somente o item inadequado com estado explícito; não preencher zero. Manter métricas alternativas aprovadas e atualizar contrato/template.

## RB-04 — Disco ou fila do NOC em pressão

Confirmar qual volume cresce, retenção, WAL, logs e espaço de backup temporário. Preservar dados do ensaio antes de qualquer ajuste. Reduzir frequência de itens não críticos ou ampliar disco sob plano; não apagar volume do banco. Validar redução de fila e duração de backup depois da mudança.

## RB-05 — Mudança de rota/firewall/rádio

Entrada: escopo concreto autorizado, backup, console/porta de recuperação e alvo correto. Registrar antes/depois previsto e pós-teste. Aplicar um equipamento ou caminho por vez. Não alterar simultaneamente core e hub quando a sessão depende deles.

Se pós-teste falhar, restaurar configuração anterior capturada. Usar Safe Mode/reversão temporizada somente após validar o comportamento no RouterOS real; não assumir que uma sessão perdida recuperará qualquer mudança. Escalonar para acesso local se rollback não puder ser confirmado.

## RB-06 — Reinício ou atualização de stack

Conferir backup, versões e compatibilidade de migração; anunciar janela pelo processo aprovado. Aplicar release fixada, verificar persistência, login, coleta e alertas. Reinício de processo não é suficiente como aceite. Se banco foi migrado, rollback exige restauração compatível, conforme [backup](BACKUP_RESTORE.md).

## RB-07 — Incidente de credencial

Revogar credencial/peer afetado, preservar logs sanitizados e verificar escopo de acesso. Rotacionar dependências comprometidas sem publicar novos valores. Confirmar que a identidade antiga falha e a nova opera com menor privilégio. Avaliar impacto nos dados e encaminhar ao responsável.

## RB-08 — Retirada de um barco

Validar proprietário/ordem de retirada; revogar credenciais e acesso remoto; retirar associação/VLAN/rota conforme inventário; encerrar monitoração mantendo histórico no prazo aplicável. Remover segredos locais durante recolhimento do kit. Não reutilizar IP/identidade até baixa confirmada. Dados e microSD seguem processo de devolução/eliminação aprovado.

## RB-09 — Falha ou oscilação das WANs da central NOC

Procedimento futuro para a [variante dual-WAN](../02-implementation/NOC_DUAL_WAN.md), ainda não implantada. Registrar interface física, endereços/lease, gateway, estado das quatro sondas /32, defaults e próximo salto efetivo. Diferenciar falha do modem, upstream, uma sonda e indisponibilidade de todas as rotas de uma WAN.

Na perda total, defaults devem ficar inativas, sem receber `disabled=yes`. Não corrigir ausência de Internet desabilitando rotas, nem limpar globalmente conntrack como reação automática. Conferir se cada sonda usa a WAN prevista; um ping genérico pode sair pelo outro link. Se houver oscilação, preservar horários e contagem das trocas antes de alterar parâmetros sob RB-05.

Após retorno, testar novas conexões, DNS e caminho administrativo até o core, além do handshake. Registrar impacto em sessões anteriores e retomar a coleta. Se a mudança de configuração causar perda de acesso, usar recuperação local e backup conforme RB-05. Aceite pelos testes WAN-01 a WAN-07.

## RB-10 — Acesso administrativo pelo notebook

Caminho validado em 16/09/2026: notebook 10.250.0.10 → hub 10.250.0.1 → SSH TCP 5822. No notebook Windows, usar a identidade SSH indicada pelo usuário com opção -i; caminho exato no registro privado notebook-access-preferences.json. Nova sessão confirmada pelo usuário, inclusive após reboot. A conta root registra o acesso atual, não uma alteração da política de contas nominais. Não há acesso à RB951G/core comprovado por esse teste.

Para diagnóstico, consultar estado/idade do handshake, contadores e rota específica; confirmar que o cliente envia o destino da VPS pelo túnel. A indicação de túnel ativo no aplicativo não substitui handshake/tráfego. Testar ICMP e uma nova sessão SSH separadamente; falha de ping pode exigir verificar firewall do cliente antes de concluir falha do túnel. Não divulgar chaves privadas em saídas de diagnóstico.

Se o hub falhar, o notebook também perde esse caminho; usar console Proxmox ou SSH de recuperação conforme disponibilidade. Não restringir o acesso existente sem revisão e retorno preparados. Cadastro, limites e retorno estão na [validação do notebook](../06-validation/NOTEBOOK_VPN_VALIDATION.md).


## RB-11 — Backup falhou, envelheceu ou objeto expirou

Conferir status, resultado do serviço systemd e correspondência entre o último arquivo local e o registro S3, conforme [procedimento](BACKUP_RESTORE.md). Diferenciar falha de geração/criptografia, IAM/rede, upload, download/hash e expiração esperada. A rotina sinaliza erro após tentativa falha ou idade local de pelo menos 26 horas; o monitor externo SES/Telegram notifica falha, idade da verificação S3 e ausência de heartbeat conforme o registro de alertas.

O S3 tem expiração de sete dias configurada pelo usuário; a retenção longa 7/4/3 é local. Não considerar ausência de objeto antigo como falha automática de backup sem conferir o prazo e a existência de cópia recente. Após o prazo informado pelo S3, verificar a exclusão e registrar horário; AccessDenied não é prova de ausência. Preservar a última cópia válida durante investigação e não apagar volumes ou credenciais para tentar corrigir o job.

## RB-12 — Manutenção das restrições de acesso

Política implantada e aprovada por TCP IPv4 antes e depois de reboot. Conferir labels Traefik, guarderia-panel-firewall.service, guarderia-host-firewall.service e regras efetivas, além de DNS/TLS do notebook. Retorno limitado ao componente que falhou, com console disponível. [Painéis](../06-validation/VPS_ACCESS_VALIDATION.md), [infraestrutura](../06-validation/VPS_HOST_ACCESS_VALIDATION.md).

Não repetir os testes externos ou logins sem nova alteração/falha. Não considerar regras IPv6 presentes como ensaio IPv6 externo. RPC/Swarm continuam em execução; o filtro controla a entrada pública.

## RB-13 — Reboot e retorno da VPS

Ensaio controlado concluído, com pós-testes locais, externos e logins aprovados. Para nova mudança que exija reboot, registrar novo escopo/backup e situação anterior, comparar o boot_id operacional e confirmar retorno; o identificador do sandbox não representa a VPS. [Procedimento e recuperação](../06-validation/VPS_REBOOT_VALIDATION.md).

## RB-14 — Alertas externos de backup

SES e Telegram ativos e recebimento confirmado. Conferir heartbeat, estado da Lambda/EventBridge, permissões, idade da última verificação S3 e entrega por canal. Ausência de sinal não identifica sozinha queda da VPS. Para suspender, primeiro desativar a agenda AWS; parar somente o heartbeat provoca alerta. Comandos, retorno e limites em [alertas](../06-validation/BACKUP_ALERTS.md).
