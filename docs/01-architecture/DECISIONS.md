# Registros de decisão de arquitetura

Data da baseline: 12/09/2026. “Adotado para especificação” significa direção documental, sem homologação implícita de hardware.

## ADR-001 — Reaproveitar infraestrutura disponível

**Atualização 29/09/2026:** papel obrigatório de core RB750Gr3 substituído pelo ADR-022; NOC/VPS preservados. Texto original abaixo.

**Status:** confirmado pelo usuário para RBs e VPS. **Contexto:** reduzir desembolso inicial. **Decisão:** RB750Gr3 no core, RB750r2 na central NOC e VPS existente. **Consequência:** medir CPU, RAM e throughput com firewall, VPN e coleta ativos; substituição somente se a medição demonstrar insuficiência.

## ADR-002 — WireGuard com hub público

**Atualização 29/09/2026:** hub mantido; expansão por peer embarcado individual conforme ADR-022. VPN NOC confirmada em 22/09. Texto original abaixo.

**Status:** parcialmente implementado em 16/09/2026 (hub e notebook); RBs pendentes. **Contexto:** CGNAT nos dois locais. **Decisão:** peers central NOC/core iniciam túneis até VPS; WireGuard no host. **Alternativas:** conexão IPv6 direta ou CHR. **Consequência:** VPS é ponto único de gerenciamento; Internet local não depende dela. Console e restauração documentados são obrigatórios.

## ADR-003 — Ubuntu 24.04 e Docker/Portainer

**Status:** implementado em 16/09/2026. **Decisão:** Docker Swarm instalado pelo usuário via Orion, substituindo a proposta inicial Compose. Serviços e digests registrados no fechamento da etapa; manifestos Grafana/Prometheus reconciliados e recriação de suas tarefas validada; compatibilidade geral e recuperação integral seguem pendentes. **Consequência:** não misturar semântica de secrets, labels e dependências entre modos.

## ADR-004 — Coleta antes do rádio em campo

**Status:** confirmado pelo usuário. **Decisão:** Zabbix/PostgreSQL, Grafana e Kuma antes da PoC. **Alternativa descartada nesta fase:** testar e instalar observabilidade depois. **Consequência:** maior preparo inicial, com evidências desde o primeiro ensaio.

## ADR-005 — Dois rádios no wAP ax

**Status em 29/09/2026: substituído pelo ADR-022.** A candidatura abaixo pertence ao enlace terrestre retirado.

**Status:** candidato à PoC. **Decisão:** 5 GHz cliente e 2,4 GHz AP local; mANTBox como base. **Consequência:** simplifica kit e alimentação, porém não comprova cobertura em toda orientação. Reprovação RF pode exigir reposicionamento ou outro conjunto de antenas.

## ADR-006 — Roteamento por barco e trânsito segregado

**Status em 29/09/2026: substituído pelo ADR-022.** LAN exclusiva mantida; /30/VLAN de transporte e NAT central saem do desenho.

**Status:** proposta de engenharia desta baseline. **Decisão:** LAN /24 por barco, trânsito /30 em VLAN atribuída por estação, sem NAT no wAP. **Contexto:** gerência direta e defesa contra tráfego lateral. **Consequência:** rotas e ACLs devem ser criadas em conjunto. Compatibilidade e autenticação por estação são gate de laboratório.

## ADR-007 — Separar vídeo e NOC

**Status:** adotado para especificação. **Decisão:** gravação embarcada e acesso sob demanda. **Consequência:** VPS não dimensionada como NVR/relay de vídeo; nuvem do fabricante pode consumir upload e franquia e deve ser medida.

## ADR-008 — Métricas por capacidade e origem

**Status:** baseline corporativa adaptada. **Decisão:** sem dados inventados; campos não suportados têm estado próprio; cada medição registra origem e tempo. **Consequência:** SNR/CCQ indisponível não bloqueia sozinho a PoC se perda, RSSI, taxa e aplicação forem medidos; a lacuna fica explícita.

## ADR-009 — Automação restrita e integração opcional

**Status:** adotado para especificação. **Decisão:** recuperação de processos é determinística; alterações de rede não são autoexecutadas por IA nesta fase. NOC-Agent começa futuramente por leitura. **Consequência:** disponibilidade não depende de LLM/Chatwoot; sem copiar runtime ou stack do repositório de referência.

## ADR-010 — Evidências protegidas e Git documental

**Status:** adotado para especificação. **Decisão:** repositório recebe documentos e futuros templates sanitizados; arquivos reais e chaves ficam em armazenamento privado. **Consequência:** hash e identificador permitem rastrear evidência sem publicar dados de clientes. A retenção depende da classificação.

## ADR-011 — Capacidade e custos são hipóteses mensuráveis

**Status:** adotado para especificação. **Decisão:** dimensionamento inicial da conversa é ponto de partida; aprovação exige carga real, retenção e orçamento. **Consequência:** não converter número de barcos em garantia de capacidade nem preços históricos em cotação vigente.

## ADR-012 — Avaliar redundância WAN da central NOC

**Status:** proposta, dependente de inventário e laboratório. **Contexto:** anexos fornecidos pelo usuário descrevem duas WANs estáticas e recuperação recursiva. **Decisão proposta:** WAN1 preferencial e WAN2 backup na RB750r2, com duas sondas por WAN, sem scripts que desabilitem defaults. Preservar o IPAM e separar essa atribuição de portas da RB750Gr3. **Alternativa:** manter uma WAN enquanto não houver segundo link confirmado. **Consequência:** adaptar sintaxe, segurança e rotas VPN antes de importar; medir recuperação de sessões e WireGuard. Trata-se de comportamento determinístico do roteamento, não de ação por IA. Ver [especificação e testes](../02-implementation/NOC_DUAL_WAN.md).

## ADR-013 — Domínio e aliases da Guarderia

**Data:** 15/09/2026. **Status:** domínio awecloudsolution.com e preferência por CNAME confirmados; nomes publicados pelo usuário e resolução A/CNAME conferida na VPS (TTL 300 s). **Decisão:** um A para vps-guarderia e aliases por serviço com sufixo guarderia, conforme [plano DNS](../02-implementation/DOMAINS_AND_DNS.md). **Consequência:** centralizar mudança de IP, manter administração restrita pela VPN e validar DNS, proxy e TLS separadamente.

## ADR-014 — Coleta Prometheus pela rede interna

Em 16/09/2026, adotados os nomes DNS das tarefas Swarm para coleta dos três serviços de monitoramento, removendo dependência de DNS público/TLS. IPs virtuais recusaram conexão; tarefas responderam. Ver [procedimento](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md). Diagnóstico da rede virtual permanece pendente.

## ADR-015 — WireGuard por marcos de acesso

**Atualização 29/09/2026:** preservar marcos executados de notebook/NOC; etapa futura do core substituída por peers embarcados. Texto original histórico abaixo.

**Data:** 16/09/2026. **Status:** parcialmente implementado. **Plano inicial:** hub → RB750r2 → core. **Ajuste autorizado:** como o usuário não tinha acesso à RB750r2, ativar o hub após confirmação de console e antecipar o notebook de recuperação, mantendo a integração da central NOC antes do core. **Resultado:** notebook ↔ VPS com handshake/ping observados e SSH confirmado pelo usuário; configuração persistida e backup privado.

**Consequência:** o próximo marco depende de acesso à RB750r2, inventário real de LAN/rotas e backup/recuperação. Não anunciar LANs propostas nem considerar que o notebook dá acesso a RBs ausentes. Restrição de gerência exige revisão dos caminhos públicos e dos painéis pela VPN, com pós-teste específico. Persistência testada e restauração continuam requisitos de F2. Ver [procedimento](../02-implementation/WIREGUARD.md) e [evidências](../06-validation/NOTEBOOK_VPN_VALIDATION.md).

## ADR-016 — Persistência explícita e restauração isolada

Data: 16/09/2026. Auditoria/backups, migração de produção e ensaios isolados executados; estado atualizado em BACKUP_AUTOMATION. Adotar volumes nomeados para Grafana/Prometheus, preservando dados atuais antes de substituir tarefas. Testar backups com as imagens instaladas, sem rede externa ou volumes produtivos graváveis. Cópias locais são preparação, não substituem off-site. Evitar deploy integral do YAML Orion sem comparar o serviço ativo. [Plano e retorno](../06-validation/PERSISTENCE_BACKUP_AUDIT.md).

## ADR-017 — Backup local criptografado com cópia S3 separada

Data: 16/09/2026. Implementado localmente: capturas consistentes por serviço, dumps PostgreSQL, criptografia GPG/AES-256, validação por descriptografia/hash e timer diário. Cópia S3 autorizada no escopo de backup; bucket/região informados pelo usuário e permissões do perfil validadas; envio diário ativado após teste de restauração a partir do S3. Segregar arquivo criptografado da chave de recuperação e não declarar off-site antes de upload/download verificado. Retenção local 7 diários/4 semanais/3 mensais por união de períodos; retenção S3 de sete dias configurada pelo usuário e expiração prevista observada em dois objetos; custódia externa da chave confirmada pelo usuário e teste dessa cópia externa pendente. Falhas registradas localmente não equivalem a notificação externa. [Implementação e limites](../06-validation/BACKUP_AUTOMATION.md).


## ADR-018 — Retenção local e externa com janelas diferentes

Data: 16/09/2026, horário de São Paulo. **Confirmado pelo usuário:** expiração da versão atual no S3 em sete dias. **Observado:** HeadObject indicou expiração no backup e no recibo; consulta completa do lifecycle negada e bucket sem versionamento habilitado. **Decisão registrada:** manter a política local implantada 7 diários/4 semanais/3 mensais e a janela externa informada pelo usuário, sem presumir cópias semanais/mensais longas fora da VPS. **Consequência:** perda do host limita a recuperação aos backups ainda existentes no S3; acompanhar falhas/idade e validar a exclusão futura. A configuração de lifecycle não foi aplicada pelo assistente. [Evidência canônica](../06-validation/BACKUP_AUTOMATION.md).

## ADR-019 — Priorizar gerência da VPS pela VPN antes de nova dependência de campo

Status: implantado e validado no escopo TCP IPv4/VPN, com evolução após reboot; teste externo IPv4 e HTTPS pós-mudança aprovados conforme saída do notebook; logins pós-mudança nos quatro consoles confirmados pelo usuário. [Resultados e limites](../06-validation/VPS_ACCESS_VALIDATION.md). A justificativa e a sequência originalmente propostas seguem abaixo. A RB750r2 ainda depende de acesso do usuário; notebook/VPS e backup externo já permitem preparar a revisão de exposição. Iniciar por auditoria somente leitura e acesso web/TLS pela VPN, depois preparar restrições por serviço com retorno e pós-teste. SSH pela VPN não comprova proteção dos painéis. [Plano concreto](../04-security/VPS_ACCESS_PLAN.md).

Execução posterior: restrições públicas de SSH, Swarm, rpcbind e Zabbix 10051 mantidas após confirmação de nova sessão VPN e console; reversão automática cancelada; ensaio externo TCP IPv4 aprovado conforme saída do notebook, com SSH e HTTPS preservados pela VPN. [Inventário, política e retorno](../06-validation/VPS_HOST_ACCESS_VALIDATION.md). Não considerar o aceite anterior dos painéis como aceite desta mudança.

Ensaio de reboot executado: novo boot confirmado e pós-testes locais aprovados; SSH VPN confirmado pelo usuário. Testes externos TCP IPv4 e scripts VPN após reboot aprovados conforme saídas do notebook; logins nos quatro consoles confirmados pelo usuário; aceite funcional do reboot concluído no escopo testado. [Plano e recuperação](../06-validation/VPS_REBOOT_VALIDATION.md).

## ADR-020 — Monitor externo de backup por SES e Telegram

Data: 17/09/2026. Implementado e ativo por autorização do usuário. Heartbeat da VPS no S3 e Lambda/EventBridge a cada cinco minutos; ausência de sinal por 15 minutos, falhas e verificação S3 com 26 horas geram avisos, com recuperação por canal. Estado de testes separado do real. Bot vinculado privadamente, token em SSM SecureString, role de execução delimitada e sem chave AWS da VPS na Lambda. Dez testes locais e ensaios integrados aprovados; recebimento e recuperação confirmados pelo usuário. [Implementação, retorno e limites](../06-validation/BACKUP_ALERTS.md).

Consequências: não depende da VPS para avaliar ausência de heartbeat, mas depende da AWS e não identifica automaticamente a causa da ausência. Não substitui monitor independente da AWS, acompanhamento de custos ou recuperação integral. A política administrativa usada na implantação permaneceu na identidade do perfil; revisão de privilégios é trabalho separado.

## ADR-021 — Preservar o gateway ativo durante integração

**Status:** direção de implementação em 21/09/2026. **Contexto:** RB750r2 já fornece conectividade da central NOC. **Decisão:** integrar WireGuard e eventual segunda WAN incrementalmente, preservando LAN/DHCP/NAT atuais; manter 10.21.0.0/24 como reserva administrativa futura até definir segregação. Usar modelo e versão observados, sem presumir throughput ou velocidade negociada. **Consequência:** backup/acesso local, análise de sobreposição e pós-testes obrigatórios; não aplicar reset/template integral. Validar NOC-01/02, VPN-01/02/03 e SEC-03/04.

## ADR-022 — Internet 4G independente por barco

**Data:** 29/09/2026. **Status:** topologia confirmada pelo usuário; detalhamento de VPN/kit proposto, implantação pendente. **Motivo:** dificuldade de posicionar antenas e passar infraestrutura na costa. **Decisão:** retirar central terrestre de distribuição, provedor fixo compartilhado, base mANTBox e transporte 5 GHz. Cada barco terá modem/SIM próprios; NOC/VPS mantêm administração/observabilidade. RB750Gr3 fica disponível para uso a avaliar.

**Proposta técnica:** LAN e chave/peer exclusivos por barco, Internet direta pela linha local e VPN somente para gerência/coleta. Modem/roteador integrado se atender; roteador/AP complementar se necessário. NAT na WAN do kit, isolamento no hub e nas pontas, funções de segurança locais. Não encaminhar default de Internet nem vídeo contínuo pela VPS.

**Consequências:** troca do IPAM de trânsito por peers `.101–.120`, revisão de rotas/ACLs, energia, lista de materiais, coleta LTE e orçamento de dados. SIM próprio não elimina congestionamento/falha comum de operadora. RF-01 a RF-05 substituídos por CEL-01 a CEL-07; sem aceite transferido. VLANs antigas não são removidas de equipamentos por decisão documental. **Alternativa retirada:** continuar a distribuição costeira. **Liberação:** PoC celular, VPN, isolamento, energia e capacidade medidos.

## ADR-023 — Chips fornecidos pela operação com gestão individual contratada

**Data:** 29/09/2026. **Status:** possibilidade de fornecimento e objetivo de controle confirmados pelo usuário; operadora/plano/recursos pendentes. **Direção provável:** Vivo, sem contrato ou cobertura homologados. **Decisão:** manter identidade da linha por barco e contratar gestão individual verificável. Chip do proprietário permanece modalidade com visibilidade/controle limitados ao que for autorizado.

**Consequências:** distinguir franquia, velocidade e QoS local; portal/API, pool, limites e suspensão dependem do contrato. Consumo local é estimativa a conciliar com a operadora; controle não implica velocidade garantida. Custos recorrentes entram por linha, sem usar orçamento antigo dos rádios. Definir titularidade, ciclo, excedentes, cancelamento, suporte e proteção de identificadores. **Liberação:** SIM-01, DATA-01 e COM-01, sem compra ou ação em linhas reais nesta revisão.

## ADR-024 — Telemetria embarcada e atuação independente da conectividade

**Data:** 29/09/2026. **Confirmado:** bateria, fumaça e bomba com métricas no NOC; acionamento remoto da bomba se viável; barcos geralmente 12 V, baterias veiculares/estacionárias e bombas variadas. **Proposta:** SmartShunt IP65 e gateway local, detector com alarme local e corrente/nível da bomba; comparação ESP32 versus gateway comercial. [Pesquisa e fontes](IOT_MONITORING_RESEARCH.md).

Não homologado nem comprado. SoC deve ser calculado e calibrado, sem inferência só por tensão. Remoto adiciona comando temporizado, sem poder bloquear automático local; corrente e água confirmam efeitos distintos. Telemetria/comandos têm autorização por barco, identidade, idade, deduplicação e expiração. Metas de 1 s local, 5 s de publicação e latência no NOC são propostas a medir; funções locais independem de 4G. Liberação por IOT-01 a IOT-05, energia, isolamento e orçamento instalado.

## ADR-025 — Avaliar placas disponíveis e medição de bateria própria

**Data:** 29/09/2026. **Confirmado:** usuário possui UNO, MEGA e Raspberry Pi 4 Model B, sem sensores, para laboratório/campo. **Proposta:** reutilizar as placas, avaliar INA226/INA228 com shunt apropriado contra SmartShunt e comparar consumo/custo instalado. Propor MEGA para aquisição/temporização e Pi 4B como gateway; UNO auxiliar. Pico é alternativa futura, não disponível confirmada. Não escolher pinagem nem prometer custo/precisão antes de inventário e calibração. [Plano do protótipo](IOT_LOW_COST_PROTOTYPE.md). REQ-31–34 e IOT-01–05 continuam vigentes; nenhuma implementação ou atuação realizada.

Complemento ADR-025: usuário acrescentou LM2596 ajustável com display e módulo GSM/GPRS identificado no chat como “SIMBOL800L”. Avaliar conversor em bancada; identidade SIM800L é hipótese. Se confirmada, manter apenas ensaio 2G separado, sem substituir o 4G previsto em REQ-03. Não presumir alimentação compartilhada Pi/modem, capacidade contínua de 3 A ou comando por SMS.
