# Runbooks operacionais

Estado: procedimentos planejados. Cada execução registra responsável, horário UTC, equipamento, diagnóstico, autorização existente, mudança, resultado e evidência. Credenciais ficam no cofre, nunca no registro público.

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
