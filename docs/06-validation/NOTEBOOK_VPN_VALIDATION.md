# Validação do acesso notebook ↔ VPS

Registro histórico: observações e pendências abaixo correspondem à etapa original. Migração, S3, restrições de acesso, reboot e alertas foram posteriormente executados; consultar o [estado consolidado vigente](../00-project/IMPLEMENTATION_STATUS.md) antes de tratar uma pendência deste registro como atual.

Data: 16/09/2026. Escopo concluído: cadastro do notebook no hub WireGuard e acesso SSH pela VPN. Não equivale à homologação da central NOC, do core ou da fase F2 inteira.

## Origem e autorização

O usuário informou endpoint 204.157.108.99:51820, endereço 10.250.0.10/32 e porta local 52134; forneceu a chave pública do notebook para cadastro. Console Proxmox e acesso SSH à VPS haviam sido confirmados. Após o teste, confirmou que a nova sessão SSH em 10.250.0.1:5822 funcionou. Em seguida, reafirmou não ter acesso à RB951G e solicitou atualização documental, commit e push. Nenhuma chave ou endereço público de origem do notebook integra este registro.

## Implementação observada

| Item | Resultado |
|---|---|
| Hub | WireGuard no host LXC, wg0, 10.250.0.1/32, UDP 51820 |
| Peer implantado | Notebook de recuperação, AllowedIPs 10.250.0.10/32 |
| Rota VPS → notebook | 10.250.0.10/32 por wg0, origem selecionada 10.250.0.1 |
| Persistência configurada | /etc/wireguard/wg0.conf com modo 600; wg-quick@wg0 habilitado no boot |
| Aplicação | Peer e rota adicionados sem reiniciar a interface |
| Escopo preservado | Sem mudança de firewall, NAT, rota default ou redes de LAN |
| Recuperação preparada | Backup anterior da configuração, rotas e regras IPv4/IPv6 em armazenamento privado |

Identificador do backup: `wireguard-preflight/notebook-20260916T200122Z` (20:01:22 UTC, 17:01:22 America/Sao_Paulo). Contém dados restritos e não está no Git. O horário identifica o backup; não é apresentado como timestamp exato dos testes posteriores.

## Evidências e limites

| Verificação em 16/09/2026 | Origem | Resultado e alcance |
|---|---|---|
| Handshake | Consulta wg show na VPS | Último handshake com idade de 2 s no instante consultado; tráfego recebido e enviado |
| ICMP VPS → notebook | ping pela wg0, 3 envios | 3 respostas; 0% de perda nessa amostra; RTT mínimo/médio/máximo 15,950/20,795/29,934 ms |
| Administração notebook → VPS | Confirmação do usuário após executar SSH | Nova sessão em 10.250.0.1:5822 funcionando |
| Serviços do host | Consulta systemctl após cadastro | SSH, Docker e WireGuard ativos; wg-quick habilitado |
| Stack | Consulta docker service ls após cadastro | 12 serviços com réplicas 1/1 |
| Prometheus | Registro anterior da etapa VPS | Três alvos UP na validação anterior; a API não foi consultada novamente no cadastro do notebook |

O handshake comprova alcance externo do endpoint UDP a partir desse notebook. Não comprova todos os caminhos de firewall, outros provedores ou troca de WAN. A amostra ICMP não é SLA nem teste prolongado. O SSH confirma acesso à VPS; não confirma painéis web pela VPN, acesso ao core, DNS interno ou PMTU. Configuração salva e serviço habilitado não comprovam recuperação após reboot.

## Estado dos critérios

- VPN-01: parcial; hub/notebook validados, RB951G e RB750Gr3 ausentes, comportamento CGNAT/troca de WAN não ensaiado.
- VPN-02: parcial; rota /32 e retorno notebook ↔ VPS comprovados; LANs, encaminhamento entre peers e origem da coleta container pendentes.
- VPN-03: pendente; notebook cadastrado não homologa recuperação do core ou independência da central NOC.
- SEC-03/04, OPS-01 e BAK-01: não homologados por este teste. Portas públicas, revogação/privilégios, reboot e restauração exigem ensaios próprios.

## Retomada

A RB951G permanece inacessível ao usuário em 16/09/2026. Quando houver acesso: inventariar interfaces, endereços, rotas e WANs; confirmar LAN real e ausência de sobreposição; obter backup protegido e caminho de recuperação; gerar chave exclusiva na RB; configurar inicialmente apenas 10.250.0.1 ↔ 10.250.0.2 e validar nova sessão administrativa. Integrar a RB750Gr3 depois. Não anunciar a LAN proposta 10.21.0.0/24 sem conferência.

Enquanto isso, permanecem tarefas independentes de revisão de exposição, persistência Grafana/Prometheus, backups/restauração, VIPs Swarm e abrangência do Node Exporter. Esta atualização documental não executa essas mudanças.

## Retorno preparado

Se for necessário desfazer o cadastro, conferir primeiro se houve alterações posteriores. Remover somente o peer do notebook da interface ativa, excluir sua rota 10.250.0.10/32 por wg0 e restaurar a configuração anterior a partir do backup protegido. Preservar hub, SSH, stack e regras Docker. O retorno específico do notebook foi descrito, mas não foi executado como ensaio.

Referências: [procedimento WireGuard](../02-implementation/WIREGUARD.md), [homologação](HOMOLOGATION.md), [backup](../05-operations/BACKUP_RESTORE.md) e [roadmap](../00-project/ROADMAP.md).
