# Memória do projeto

Atualizada em 29/09/2026. Fonte do estado vigente: [implementações](../../docs/00-project/IMPLEMENTATION_STATUS.md). Os números abaixo são resultados datados, não nova consulta. Não guardar credenciais ou resultados presumidos.

## Topologia vigente — confirmação de 29/09/2026

Usuário retirou a central terrestre de distribuição por dificuldade de posicionamento de antenas e passagem de infraestrutura na costa. Cada barco terá modem 4G e chip próprios. Chips poderão ser fornecidos pela operação com gestão individual contratada; Vivo é candidata provável, sem contratação ou cobertura homologadas. NOC/VPS administrativos existentes permanecem. RB750Gr3 não é core obrigatório; mANTBox e uplink 5 GHz do wAP saíram do projeto. Reaproveitamento depende de avaliação.

Proposta técnica: LAN 10.20.N.0/24 e peer 10.250.0.(100+N)/32 por barco (N=1–20), Internet direta pelo 4G, VPN apenas de gerência/coleta, ACL no hub/pontas e funções locais de alarme/gravação. Modelo, APN, energia, franquia e recursos de portal/API pendentes. Distinguir velocidade, franquia e QoS; não presumir gestão disponível por fornecer o SIM. RF-01 a RF-05 substituídos; CEL-01 a CEL-07, SIM-01 e DATA-01 não executados. ADR-022/023 e documentos ativos revisados; nenhuma mudança operacional, compra ou ativação de linha nesta revisão. Orçamento antigo de R$ 3.000,00 precisa de recotação. [Procedimento celular](../../docs/02-implementation/CELLULAR_CONNECTIVITY.md).

## IoT — pesquisa de 29/09/2026

Complemento do inventário de bancada: LM2596 ajustável com display confirmado; módulo GSM/GPRS informado como “SIMBOL800L”, possivelmente SIM800L, identificação da placa ainda pendente. Conversor é candidato a ensaio, sem capacidade contínua homologada. Se SIM800L, uso 2G separado, sem substituir 4G. Não presumir alimentação comum Pi/modem nem saída de 3 A sustentada; consultar o protótipo antes de orientar ligações.

Usuário confirmou métricas de bateria, fumaça e bomba no NOC, com acionamento remoto da bomba se possível. Barcos geralmente 12 V, baterias veiculares comuns ou estacionárias e bombas de potência variável. Inventariar química/Ah/bancos e corrente nominal/partida por barco; não assumir um único relé para a frota.

[Pesquisa documentada](../../docs/01-architecture/IOT_MONITORING_RESEARCH.md): candidatos SmartShunt IP65 via VE.Direct, gateway ESP32 ou Cerbo GX, DFC 421 UN com central/sirene local ou Shelly Plus Smoke, corrente da bomba e boia independente de nível alto. Preços são referências consultadas, sem orçamento instalado. SoC exige calibração, não deriva apenas da tensão; corrente não comprova drenagem. Remoto é demanda temporizada adicional, sem bloquear automático/manual local. Broker, serviço de comandos, firmware e painéis ainda não implantados. REQ-31–34, ADR-024 e IOT-01–05 registrados; nenhum ensaio IoT executado.

## Contexto e confirmações do usuário

Em 29/09/2026, usuário confirmou possuir Arduino UNO, Arduino MEGA e Raspberry Pi 4 Model B, **sem sensores**, para laboratório/campo. [Protótipo econômico](../../docs/01-architecture/IOT_LOW_COST_PROTOTYPE.md): proposta MEGA para aquisição/temporização, Pi 4B gateway MQTT e UNO auxiliar; avaliar INA226/INA228 com shunt versus SmartShunt. Não comprar controlador/gateway para iniciar sem necessidade. Sensores, revisões de placas, fontes, instalação e calibração pendentes; nenhum firmware ou ensaio executado. ADR-025 registrado; consumo do Pi 4B é referência de catálogo, não medição. SoC próprio exige sincronização, persistência e calibração.

WiFi Guarderia Vitória: hipótese de 10–20 barcos; os 50–100 m da margem são contexto original, não critério de cobertura 4G. Preparar NOC antes da PoC. RB750Gr3 disponível e RB750r2 (hEX lite) da central NOC atualizada para RouterOS/RouterBOOT 7.23.7; inventário recebido em 21/09/2026: gateway ativo, WAN1 estática, LAN com DHCP/DNS/NAT e WAN2 reservada; aquela coleta ainda não continha WireGuard. A VPN da RB750r2 foi confirmada funcional pelo usuário em 22/09/2026. Dual-WAN é proposta e segundo link não confirmado. Cobertura celular, energia, capacidade, câmeras/alarme, custos e contrato continuam em validação.

Pasta local e repositório oficial Wittemberg/wifi-Guarderia preservados. nocagent e padrões Witteberg são referências, sem runtime AG Kit instalado. Usuário autoriza trabalho operacional por etapa; autorização não implica commit/push ou divulgação de segredos.

## Estado operacional consolidado

- Stack NOC em Swarm instalada e operacional; doze serviços 1/1 e três alvos Prometheus UP no pós-teste de 17/09/2026 03:09:54 UTC. Coleta usa DNS das tarefas; VIPs ainda exigem diagnóstico. Abrangência do Node Exporter não homologada.
- Grafana/Prometheus migrados para volumes nomeados guarderia_grafana_data e guarderia_prometheus_data; recriação validada e manifestos locais/Portainer reconciliados. Zero dashboards observados no inventário Grafana; não inventar painéis configurados.
- Backup AES-256 local/S3 diário às 03h15 de São Paulo, atraso aleatório de até cinco minutos; download/hash e restauração isolada S3 ensaiados. PG15/Zabbix com 207 tabelas públicas no ensaio. Último conjunto documentado: backup-20260917T030811Z.gpg. Chave externa copiada pelo usuário, ainda não usada em restauração.
- Retenção local 7 diários/4 semanais/3 mensais; S3 sete dias configurados pelo usuário e expiração observada em dois objetos. Exclusão efetiva/escopo integral não conferidos; versionamento observado desabilitado. Não alterar lifecycle por inferência.
- WireGuard hub 10.250.0.1/32, notebook 10.250.0.10/32 e RB750r2 10.250.0.2 ativos. A funcionalidade da VPN da RB750r2 foi confirmada pelo usuário em 22/09/2026. SSH TCP 5822 e sete nomes HTTPS pela VPN, quatro logins e console Proxmox foram confirmados para o notebook. Não inferir rotas de LAN, serviços de gerência da RB, failover ou recuperação sem evidência própria.
- Sete routers Traefik restritos por origem; quatro portas de painéis e portas TCP/UDP de infraestrutura filtradas. Exceção gateway NAT Docker /32 somente no Prometheus para o datasource existente. Testes públicos TCP IPv4 de nove portas e sete nomes, inclusive cabeçalhos forjados, aprovados. Sessões SSH públicas anteriores foram preservadas durante a transição; novas conexões exigem VPN no caminho testado.
- Reboot controlado concluído: boot_id operacional mudou, pós-testes automáticos passaram, usuário repetiu testes externos e logins. Não solicitar repetição sem nova causa. O boot_id do sandbox difere do operacional; consultar fora do sandbox para validar reboot. Falha run-rpc_pipefs.mount já existia antes.
- Alertas SES/Telegram ativos: stack guarderia-backup-alerts, Lambda guarderia-backup-watchdog, EventBridge e heartbeat a cada cinco minutos. Ausência de sinal por 15 min e registro de verificação S3 com 26 h, além de falhas, geram alerta; recuperação por canal. Dez testes locais, testes integrados e recebimento nos dois canais confirmados; primeira execução automática saudável observada.

## Operação e recuperação

Evidências privadas por marcadores em guarderia-evidencias: access-current.txt (painéis), host-access-current.txt (infraestrutura), reboot-current.txt e alerts-current.txt. Retornos e limites nos respectivos registros de validação. Timers transitórios de reversão de acesso foram cancelados após confirmação; não presumir que ainda estão ativos.

Token Telegram em arquivo privado /root/.config/guarderia-alerts/telegram.json modo 600 e SSM SecureString /guarderia/alerts/telegram. Destinatários e identidade AWS apenas em configuração privada. Nunca pedir chave/token pelo chat. Política administrativa de implantação foi adicionada pelo usuário; não removê-la nem ampliá-la sem escopo próprio.

Preferência persistente: notebook Windows; sempre incluir -i com o caminho exato registrado em /root/guarderia-evidencias/notebook-access-preferences.json nos comandos SSH/SCP enviados ao usuário. Isso é caminho da identidade, não conteúdo da chave. Registro privado notebook-access-preferences.json. Para documentação sanitizada, não publicar comandos incompletos sem a identidade.

## Próximo passo e limites

Preparar recuperação integral em ambiente separado com chave externa e critérios de aceite. Reboot e alertas já concluídos não são próximas etapas pendentes. UDP externo, IPv6 externo, renovação ACME, revisão de privilégios, recuperação TLS/bancos integral, exclusão S3, diagnóstico de VIPs/Node Exporter e integração de equipamentos ainda pendentes. Não homologar F2/BAK-01/OPS-01/SEC-03/04 inteiros apenas pelos ensaios parciais.

Preservar arquivos e alterações existentes; segredos fora do Git. Não anunciar LAN de RB não conferida, antena 360°, SNR/CCQ não suportado, isolamento apenas por sub-rede, telemetria de campo ou percentuais sem evidência. Ver [requisitos](../../docs/00-project/REQUIREMENTS.md) e [riscos](../../docs/00-project/RISKS_AND_OPEN_ITEMS.md).

## Inventário atual da central NOC

Em 21/09/2026, o usuário confirmou navegação na Internet através da RB750r2 e operação plena como gateway. NOC-02 tem aceite funcional do usuário; não tratar a ausência de nome no arquivo teste-dns como falha ou impedimento de uso. A VPN WireGuard da RB foi confirmada funcional pelo usuário em 22/09/2026. Failover, rotas de LAN, políticas de serviços e recuperação permanecem etapas distintas e pendentes de evidência.

Modelo observado RB750r2 (hEX lite), revisão r3; 64 MiB RAM, 16 MiB flash, CPU 850 MHz; RouterOS/RouterBOOT 7.23.7. Treze anexos analisados; três amostras ICMP 5/5, sem comprovação de resolução DNS no arquivo teste-dns. Fontes no [inventário](../../docs/01-architecture/NOC_ROUTER_INVENTORY.md); originais fora do Git. LAN 10.21.0.0/24 é reserva futura, não rede em uso. Integração incremental, preservando DHCP/NAT e acesso local; não resetar/importar template. Exemplo WAN1 do template conflita com a LAN atual. Nenhum serviço remoto alterado nesta revisão.
