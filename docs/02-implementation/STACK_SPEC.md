# Especificação da stack de monitoramento

Estado: contrato de implantação, sem manifesto executável nesta versão. Nome proposto: `wifi-guarderia`. Host único. Diretório de estado proposto: `/var/lib/wifi-guarderia`. O domínio ainda não foi definido; não reutilizar domínios do `nocagent`.

## Serviços e persistência

| Serviço | Função | Persistência requerida | Exposição |
|---|---|---|---|
| PostgreSQL | Banco Zabbix | Volume de dados e backup lógico consistente | 5432 somente rede de dados |
| Zabbix server | SNMP/API/ICMP, processamento e alertas | Configuração e scripts versionados; estado no banco | 10051 somente se houver necessidade de sender/proxy/active agent |
| Zabbix web | Console operacional | Configuração versionada; estado no banco | Backend somente proxy/rede administrativa |
| Grafana | Dashboards históricos | Banco/volume próprio, provisioning e plugin fixado | 3000 interno |
| Uptime Kuma | Painel de disponibilidade | Volume próprio, backup consistente | 3001 interno |
| Proxy TLS | Entrada HTTPS | Certificados e configuração protegidos | Preferir acesso privado por VPN |
| WireGuard | Hub VPN | `/etc/wireguard`, permissões restritas | Host, UDP 51820 |

Não montar o socket Docker em Zabbix/Grafana/Kuma. Portainer tem privilégios de administração e deve ser restrito à rede administrativa. A forma de instalação do Portainer será registrada no inventário; não implantar uma segunda instância por engano.

## Versões

Zabbix 7.0 LTS é a linha candidata usada nas referências desta especificação; o patch exato será selecionado na implementação. PostgreSQL deve pertencer à matriz suportada pela versão Zabbix escolhida. Grafana, plugin Zabbix, Kuma, Docker, Portainer e proxy também precisam de versões compatíveis e fixadas. Não usar `latest` como única referência.

Manifesto de release obrigatório antes do deploy:

| Campo | Conteúdo obrigatório |
|---|---|
| SO/arquitetura | Versão e arquitetura observadas |
| Orquestrador | Compose ou Swarm e versão |
| Imagens | Nome, tag e digest de cada serviço |
| Compatibilidade | Zabbix ↔ PG; Grafana ↔ plugin; Kuma ↔ backup |
| Configuração | Commit Git, redes e volumes |
| Validação | IDs de testes e plano de rollback |

## Redes

Rede de dados é privada e não publica porta do banco. Rede de coleta tem saída roteada controlada para a VPN. Somente serviços web entram na rede do proxy. Se houver proxy compartilhado, somente frontends aderem à rede compartilhada; banco e coleta permanecem isolados.

Na baseline Compose, sub-redes propostas constam no [IPAM](../01-architecture/NETWORK_PLAN.md). Se Swarm for escolhido, reserva de IP fixo por task não deve ser presumida: definir SNAT/regras pela rede dedicada de coleta e restringir os serviços que podem aderir a ela. Não reutilizar exemplos Compose sem revisão.

## Configuração sensível e não sensível

| Grupo | Configuração pública possível | Dados privados |
|---|---|---|
| Identificação | Nome da stack, timezone | Host/IP real se sensível |
| Banco | Nome lógico do database | Usuário operacional e senha |
| Zabbix/Grafana | Templates, intervalos, IDs lógicos | Tokens e credenciais de coleta |
| VPN | Prefixos planejados e porta | Chaves privadas e PSKs |
| Alertas | Políticas e severidades | Tokens, e-mails e telefones reais |
| Backup | Agenda e retenção | Credenciais do storage e chave de criptografia |

Usar mecanismo de secrets suportado pelo modo escolhido ou arquivos protegidos fora do checkout, com acesso limitado ao serviço. Variáveis de ambiente não são um cofre e podem aparecer em inspeção. Recursos persistentes precisam de backup; não salvar o `.env` real no Git.

## Inicialização e saúde

O banco fica pronto antes da conexão do server/web, mas serviços devem suportar tentativas de reconexão. Healthcheck não pode depender de `curl` inexistente na imagem: testar o comando efetivamente fornecido. Distinguir processo vivo de capacidade de coletar/gravar. Monitorar fila de coleta, idade da última amostra, banco, disco e sucesso de notificações.

Serviço unhealthy não implica reinício automático pelo Compose. Configurar política de restart para saída de processo e supervisão explícita para falhas persistentes; nenhuma recuperação deve apagar volumes ou recriar configuração padrão.

## Deploy e rollback

Primeiro validar manifesto em laboratório. Em Compose, `docker compose config --quiet` verifica estrutura sem imprimir valores resolvidos; em Swarm usar validação apropriada e saída protegida. Conferir volumes, secrets e redes antes de subir.

Release: snapshot/backup → aplicar versões fixas → verificar banco e serviços → coletar alvo conhecido → testar login/alerta → testar persistência. Reverter imagem pode não reverter migração do banco; nesse caso restaurar backup compatível em ambiente separado antes de substituir produção. Critérios em [backup](../05-operations/BACKUP_RESTORE.md).

## Gate de prontidão

Não implantar até preencher modo, versões, domínio, redes reais, backup e origem de segredos. O estado “documentado” não libera os gates de laboratório ou campo.
