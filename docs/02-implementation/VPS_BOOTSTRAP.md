# Preparação da VPS

Evolução consolidada em 17/09/2026: volumes/S3, restrições TCP IPv4, reboot e alertas externos concluídos no escopo testado. [Estado vigente e limites](../00-project/IMPLEMENTATION_STATUS.md). As etapas de equipamentos ainda não executadas permanecem propostas.

Estado em 16/09/2026: inventário e instalação inicial pelo Orion concluídos; Docker Swarm e serviços conferidos. Ver [conclusão](../06-validation/VPS_PHASE_COMPLETION.md). As etapas abaixo são referência para manutenção e itens ainda pendentes, não instrução para reinstalar a stack existente.

## Inventário somente leitura

Executar na VPS e guardar saída sanitizada em evidência privada:

```bash
cat /etc/os-release
uname -m
lscpu
free -h
df -hT
lsblk -f
ip -br address
ip route
ss -lntup
timedatectl status
docker version
docker compose version
docker info
docker network ls
docker volume ls
```

Comandos Docker podem falhar se não estiver instalado; isso é resultado de inventário. Não publicar interfaces/IPs reais ou saída de configuração que contenha credenciais. Não executar `docker inspect` completo indiscriminadamente, pois variáveis podem conter segredos.

## Capacidade inicial

O histórico sugeriu 2 vCPU, 4 GB RAM e aproximadamente 60 GB SSD. É uma hipótese inicial para NOC e VPN, não garantia para 20 barcos coletados a cada 5 s. Confirmar espaço disponível após SO, volumes, logs e backups temporários; manter ao menos 25% livre como meta inicial. Considerar aumento para 4 vCPU/8 GB se banco/coleta/IO disputarem recursos. Critérios de escala estão em [capacidade](../03-monitoring/CAPACITY_AND_RETENTION.md).

## SO e instalador

Ubuntu Server 24.04 LTS é a escolha do usuário. O Docker documenta suporte ao Ubuntu 24.04 em seu [guia oficial de instalação](https://docs.docker.com/engine/install/ubuntu/).

Na consulta de 12/09/2026, a [página do SetupOrion](https://oriondesign.art.br/) ainda lista Ubuntu 20.04/22.04 e servidor vazio. Portanto, compatibilidade com 24.04 não está comprovada por essa página. Verificar documentação e versão efetiva do instalador; se não confirmada, instalar Docker/Portainer seguindo os guias dos fornecedores. Não trocar o SO escolhido apenas para acomodar o script.

Registrar URL, versão/commit, hash do instalador e alterações esperadas. Não executar download encadeado ao shell. Detectar se ele instala Swarm, proxy ou serviços adicionais e registrar esse efeito antes da execução.

## Sequência de implantação

1. Inventariar host, criar snapshot protegido se aplicável e testar console de recuperação.
2. Conferir DNS, horário, atualizações necessárias e acesso SSH por chave. Testar nova sessão antes de restringir acesso antigo.
3. Definir firewall do provedor e do host, com acesso administrativo restrito e WireGuard UDP 51820.
4. Instalar Docker e Portainer pelo caminho validado. Registrar versões e modo de orquestração.
5. Definir redes e volumes sem sobrepor redes existentes; criar diretórios persistentes com proprietário específico.
6. Instalar/configurar WireGuard no host conforme [VPN](WIREGUARD.md).
7. Validar túnel, rotas e administração por nova sessão.
8. Implantar stack conforme [especificação](STACK_SPEC.md), com secrets externos e imagens fixadas.
9. Configurar coleta, backup, alarmes internos do NOC e teste de restauração.
10. Reiniciar em janela controlada e comprovar recuperação automática.

## Firewall e Docker

Manter o backend de firewall explicitamente registrado. Não assumir que regras UFW protegem portas publicadas por containers. Docker também pode afetar encaminhamento do host, relevante para WireGuard. Validar políticas de encaminhamento entre peers e bridges; não desabilitar a administração de firewall pelo Docker sem projeto substituto. Referência: [Docker e firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

## Pós-testes e retorno

VPS-01: OS e inventário aprovados. STACK-01: dependências saudáveis, login autenticado, dados persistentes e portas externas corretas. OPS-01: reboot não perde gerência ou dados. Se uma mudança retirar acesso, usar console e restaurar o conjunto anterior de regras/configuração; não repetir mudanças remotas às cegas.

## Ponto de retomada após WireGuard

Hub e notebook já implantados, com handshake/ping e SSH validados no [escopo registrado](../06-validation/NOTEBOOK_VPN_VALIDATION.md). Console Proxmox confirmado e suporte WireGuard no LXC testado. As etapas de bootstrap anteriores são referência; não reinstalar ou recriar chaves existentes. RB951G aguarda acesso do usuário. Volumes Grafana/Prometheus e restauração isolada S3 foram posteriormente validados, conforme [backup](../06-validation/BACKUP_AUTOMATION.md). Exposição e recuperação integral seguem pendentes; iniciar pelo [plano de acesso da VPS](../04-security/VPS_ACCESS_PLAN.md).
