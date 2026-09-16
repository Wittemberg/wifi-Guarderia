# Inventário da VPS

Coleta: 15/09/2026, America/Sao_Paulo (16/09/2026 UTC). Origem: consultas somente leitura executadas diretamente na VPS nesta sessão. Inventário inicial histórico, anterior à implantação; atualizações posteriores estão ao final. O resumo abaixo transcreve resultados observados, não é um benchmark.

| Item | Resultado medido/observado |
|---|---|
| Sistema | Ubuntu 24.04.5 LTS, x86_64 |
| Virtualização | LXC, identificado por `systemd-detect-virt` |
| Kernel compartilhado | `6.17.13-2-pve` |
| CPU visível | Intel Xeon E5-2673 v4 @ 2.30 GHz; 9 CPUs disponíveis ao processo |
| Cgroup CPU | `cpu.max`: `max 100000`; não comprova capacidade dedicada |
| RAM visível | `free -h`: 377 GiB totais, cerca de 143 GiB disponíveis; pode refletir o host |
| Cgroup memória | `memory.max`: `max`; `memory.current`: 409518080 bytes no instante da consulta |
| Limite contratado | RAM e recursos garantidos pelo provedor ainda não confirmados |
| Swap visível | 0 B |
| Disco raiz | ZFS, 100 GB totais, 1,2 GB usados, 99 GB disponíveis segundo `df -hT` |
| Rede | IPv4 público `204.157.108.99` e rota padrão configurados; IPv6 link-local observado, sem IPv6 global na saída |
| DNS | Resolução de `example.com` funcionou; posteriormente A e cinco CNAMEs do projeto conferidos com `dig`, conforme o plano de DNS |
| Horário | Chrony sincronizado, stratum 3, leap normal; desvio instantâneo de aproximadamente 62 microssegundos |
| Ferramentas da stack | Docker, Podman, Portainer e `wg` não encontrados no PATH; socket Docker ausente |
| WireGuard | Diretório `/etc/wireguard` ausente; forwarding IPv4/IPv6 em 0 |
| Dispositivo TUN | `/dev/net/tun` ausente; isso isoladamente não determina suporte a WireGuard no kernel |
| Firewall | nftables com input/forward/output em ACCEPT; iptables e ip6tables com políticas ACCEPT e sem restrições nas saídas consultadas |
| SSH efetivo | TCP 5822; root permitido, chave habilitada, senha e teclado interativo desabilitados |
| Falha systemd | `run-rpc_pipefs.mount` em falha |

## Serviços e portas

SSH e rpcbind escutavam em todas as interfaces IPv4/IPv6: TCP 5822 e TCP/UDP 111, respectivamente. DNS local, Chrony e Postfix escutavam em loopback nas portas observadas 53, 323 e 25. Serviços ativos incluíam SSH, Fail2Ban, Chrony, rpcbind, Postfix e serviços básicos do sistema. Fail2Ban ativo não comprova eficácia das regras.

Não foram observados listeners da stack planejada. Não houve sondagem externa: exposição efetiva depende também do firewall do provedor. O inventário não aprova SEC-03.

## Evidência e reprodução

Consultados `uname`, `lscpu`, `nproc`, `free`, `df`, `systemd-detect-virt`, arquivos de cgroup, `ip`, `ss`, `systemctl`, `command -v`, `dpkg-query`, `nft`, `iptables`, `ip6tables`, `sysctl`, `resolvectl`, `chronyc` e `sshd -T`. Consultas de rede/systemd bloqueadas pelo sandbox foram repetidas com acesso autorizado. `ufw` não foi encontrado como comando; a consulta de pacotes não foi usada como prova de firewall ativo.

O IP público está documentado por ser destino do DNS publicado. Gateway e detalhes de endereçamento ficam no registro privado `vps-2026-09-15.txt`, fora do Git, conforme a [classificação de dados](../04-security/SECURITY.md). O registro privado contém um resumo do endereçamento, não um dump integral dos comandos.

## Pendências atuais após as atualizações de 16/09

- Confirmar RAM/CPU garantidas pelo provedor; console Proxmox já confirmado pelo usuário.
- Suporte Docker/WireGuard no LXC comprovado no escopo implantado; validar capacidade e abrangência das métricas de host.
- Investigar rpcbind e a montagem em falha; definir necessidade antes de alterar serviços.
- Revisar exposição com preservação do SSH pela VPN e teste externo posterior.
- Fixar manifesto de manutenção, revisar persistência e ensaiar backup/restauração/reboot.

VPS-01 permanece parcial. Capacidade para 20 barcos depende de carga, coleta e retenção medidas. Consulte [preparação](../02-implementation/VPS_BOOTSTRAP.md) e [homologação](../06-validation/HOMOLOGATION.md).

## Atualização — instalação concluída em 16/09/2026

O inventário de 15/09 acima é histórico anterior à instalação. Docker 29.8.1/Swarm ativo, 12 serviços 1/1; 9 CPUs e 8 GiB reconhecidos pelo Docker. A RAM de 377 GiB exibida por free não deve ser usada como capacidade da VPS. Disco após instalação: 95 GB livres. PostgreSQL 14 e 15 separados; Zabbix 7.4, Grafana 13.2.2, Kuma, Portainer, Traefik, Prometheus, cAdvisor e Node Exporter observados.

IPv4 forwarding passou a 1; iptables INPUT ACCEPT, FORWARD DROP com chains Docker e DOCKER-USER vazia. Foram publicadas portas 80/443, 3111, 8181, 9191, 9100 e 10051, além de listeners Swarm 2377/7946 e UDP 4789. Exposição externa e necessidade de cada porta ainda não homologadas. rpcbind e a montagem em falha persistiam. wg não encontrado.

Grafana sem montagem em /var/lib/grafana e Prometheus com volume anônimo exigem revisão de persistência. Node Exporter sem mounts/args de host exige validar abrangência da coleta. Três alvos Prometheus internos UP após correção. Veja [conclusão e imagens](../06-validation/VPS_PHASE_COMPLETION.md).

## Atualização — hub e notebook em 16/09/2026

Wireguard-tools instalado; wg0 ativo em 10.250.0.1/32, UDP 51820, serviço habilitado no boot. Notebook 10.250.0.10/32 cadastrado e rota /32 persistida pelo procedimento wg-quick. Handshake e ping 3/3 observados; SSH à VPS pela VPN confirmado pelo usuário. Configuração modo 600 e backup privado. Sem alteração de firewall/NAT/default no cadastro. SSH/Docker ativos e 12 serviços Swarm 1/1 no pós-teste; Prometheus não foi consultado novamente nessa operação.

RBs ainda não integradas; reboot, restauração e restrições públicas pendentes. Ver [registro detalhado](../06-validation/NOTEBOOK_VPN_VALIDATION.md).

Auditoria de persistência em 16/09/2026 confirmou ausência de volume de dados Grafana e volume anônimo Prometheus; ambos ainda sem correção aplicada. Bancos e aplicações restaurados somente em ambiente isolado; [inventário de volumes e resultados](../06-validation/PERSISTENCE_BACKUP_AUDIT.md).
