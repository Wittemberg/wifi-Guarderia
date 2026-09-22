# Plano executado: acesso administrativo da VPS pela VPN

Estado: execução autorizada e restrições dos sete painéis e quatro portas implantadas em 16/09/2026; pós-testes locais, teste externo IPv4 e HTTPS pela VPN aprovados; logins pós-mudança nos quatro consoles confirmados pelo usuário. Veja a [validação e retorno](../06-validation/VPS_ACCESS_VALIDATION.md). O restante descreve o plano utilizado. Requisitos: REQ-05/10/11/19; testes SEC-03/04 e preservação de VPN-01/02. A integração da RB750r2 continua dependente de acesso ao equipamento.

## Objetivo e motivo da prioridade

Validar os painéis administrativos pelo notebook conectado ao WireGuard e restringir sua exposição pública. A VPS já tem stack, persistência, backup externo e restauração isolada testados. SSH pela VPN foi confirmado pelo usuário, mas isso não comprova acesso web nem bloqueio da gerência pública. Esta etapa pode avançar sem a RB750r2 e trata OPEN-02/03.

## Base conhecida e pontos a conferir

| Item | Base disponível | Conferência necessária antes da mudança |
|---|---|---|
| Recuperação | Console Proxmox confirmado anteriormente; SSH notebook → 10.250.0.1:5822 testado | Disponibilidade atual do console e nova sessão SSH |
| VPN | Hub 10.250.0.1 e notebook 10.250.0.10 cadastrados | Handshake, rota e tráfego atuais |
| Aplicações | Grafana, Zabbix web, Kuma e Portainer em Swarm/Traefik | Rotas HTTP/TLS, autenticação, publicação direta e origem vista pelo proxy |
| Backup | Rotina diária S3 e restauração isolada validadas | Última cópia bem-sucedida, chave acessível e configurações imediatamente anteriores |
| Portas | Inventário histórico registra 80/443, 3111, 8181, 9191, 9100, 10051 e portas Swarm | Listeners atuais, modo host/ingress, finalidade e acesso efetivo por IPv4/IPv6 |
| DNS/TLS | Domínios e HTTPS iniciais registrados | Resolução pelo notebook e certificado válido pelo caminho VPN |

O inventário histórico não é uma nova sondagem. Não declarar uma porta pública aberta ou fechada somente por listener local ou regra em arquivo.

## Sequência de execução proposta

1. **Auditoria somente leitura:** capturar portas, serviços, redes, publicações Swarm, regras efetivas do host e configuração Traefik. Mapear cada URL/porta à aplicação e identificar caminhos que contornam o proxy. Registrar dados privados fora do Git.
2. **Matriz de acesso e retorno:** classificar gerência, tráfego interno, VPN e eventuais serviços públicos intencionais. Preparar diferenças concretas por componente, backups e comandos de retorno. Revalidar console e nova sessão SSH antes de qualquer restrição.
3. **Validação web pela VPN:** acessar os painéis com os nomes TLS corretos. Avaliar resolução específica no notebook ou DNS privado; não substituir certificado válido por acesso inseguro ao IP. Verificar login humano e funções básicas, além de HTTP 200.
4. **Aplicação por serviço:** após escopo concreto autorizado, começar pelo Portainer e avançar para os outros consoles. Fechar publicações diretas administrativas quando o caminho VPN correspondente estiver comprovado. Preservar coleta interna, WireGuard e renovação de certificados.
5. **Pós-teste e persistência:** testar pela VPN e de uma origem realmente externa, incluindo tentativa de contornar o proxy. Conferir manifests/definições Portainer para manter a política em futuros deploys. Mudança adicional que recrie serviço deve preservar os volumes e ter pós-teste próprio.

A política de acesso deve se basear na origem observada. Antes de adotar IPAllowList, conferir como o Traefik obtém o endereço do cliente e tratar cabeçalhos encaminhados somente conforme a cadeia confiável real. Não presumir que o proxy enxerga o IP WireGuard após o caminho Swarm. [Referência Traefik](https://doc.traefik.io/traefik/v3.5/reference/routing-configuration/http/middlewares/ipallowlist/).

Docker implementa publicação de portas e filtragem próprias; uma regra apenas em UFW não comprova restrição de portas publicadas. A escolha de onde aplicar as regras depende do backend efetivo e da topologia observada. [Referência Docker](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

## Fluxos a preservar

- UDP 51820 para conectar os peers autorizados ao hub.
- SSH de recuperação durante a transição, seguido de revisão específica de sua exposição.
- Comunicação privada entre aplicações, bancos e coletores; três alvos Prometheus como referência de não regressão.
- HTTPS de saída para AWS S3 e dependências necessárias.
- Fluxos usados na emissão/renovação ACME conforme o desafio realmente configurado. Não fechar 80/443 globalmente sem essa conferência.

Não presumir que a página de status pública do Kuma foi solicitada; separar esse possível uso do console administrativo na matriz. Não abrir redes de RBs ou alterar IPAM para executar esta etapa.

## Critérios de aceite

| Verificação | Evidência exigida |
|---|---|
| Acesso autorizado | Nova sessão SSH e login nos consoles pela VPN, TLS válido |
| Restrição pública | Teste de origem externa sem VPN, por domínio e porta direta, com resultado esperado por serviço |
| IPv6 | Endereçamento/listeners conferidos; quando houver caminho IPv6 público, testar a política equivalente |
| Proxy | Origem autorizada reconhecida e tentativa de cabeçalho forjado não liberando acesso |
| Não regressão | Serviços esperados ativos, coleta Prometheus saudável, bancos acessíveis somente pelos fluxos previstos e backup S3 funcionando |
| Recuperação | Configuração anterior íntegra, acesso de console disponível e retorno documentado por mudança |

Recusar a mudança ou executar o retorno preparado se uma nova sessão administrativa falhar, a origem legítima não puder ser distinguida ou houver quebra de coleta. Não improvisar liberação ampla do overlay como solução.

## Trabalho que permanece separado

Retenção S3 de sete dias foi informada pelo usuário, com expiração observada em dois objetos; a exclusão futura ainda não foi ensaiada. Reboot e alertas de backup foram posteriormente concluídos, conforme o [estado atual](../00-project/IMPLEMENTATION_STATUS.md). Recuperação integral da VPS, teste usando a chave externa, diagnóstico dos VIPs e abrangência do Node Exporter continuam pendentes. Esses pontos constam em [riscos e lacunas](../00-project/RISKS_AND_OPEN_ITEMS.md) e [backup](../06-validation/BACKUP_AUTOMATION.md). O plano foi executado mediante autorização posterior do usuário; SEC-03/04 integrais permanecem parciais pelos critérios fora do escopo validado.
