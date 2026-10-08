# Requisitos e rastreabilidade

Revisão de 29/09/2026: topologia 4G individual confirmada; implementação embarcada e gestão de linhas pendentes. Requisitos e testes de enlace terrestre foram substituídos com rastreabilidade abaixo.

**Estados:** C = confirmado pelo usuário; P = proposta técnica; V = depende de validação. Prioridades P0/P1/P2 seguem a [baseline](../../witteberg-development-standards/README.md). Consultar a homologação para o estado atual: revisões documentais realizadas, HW-01, VPS-01 e STACK-01 parciais; instalação da stack e coleta interna concluídas, VPN-01/02 parciais pelo notebook e pela funcionalidade confirmada da RB750r2; homologação integral pendente.

| ID | Requisito verificável | Origem/estado | Prioridade | Evidência de aceite |
|---|---|---|---|---|
| REQ-01 | Projetar crescimento de 10 para 20 barcos | C | P0 | CAP-01: inventário, capacidade e custos para 20 |
| REQ-02 | Validar cobertura 4G no fundeio sob movimento, obstrução e horários distintos; substitui enlace terrestre 50/100 m | C/V | P0 | CEL-02/03/04/05 |
| REQ-03 | Cada barco tem modem 4G e SIM próprios, com LAN local e gerência simultâneas; substitui wAP dual-radio obrigatório | C/V | P0 | CEL-01, LAN-01, VPN-01/02 |
| REQ-04 | Preservar VPS/RB750r2 existentes; avaliar reaproveitamento da RB750Gr3 sem core terrestre obrigatório | C/P/V | P1 | HW-01: inventário e adequação ao novo papel |
| REQ-05 | Acesso administrativo funciona com CGNAT na central NOC e em cada linha celular quando presente | C/V | P0 | VPN-01 a VPN-03 |
| REQ-06 | Usar VPS existente com Ubuntu 24.04 e Docker/Portainer | C/V | P0 | VPS-01, STACK-01 |
| REQ-07 | Avaliar compatibilidade SetupOrion antes de executar | C/V | P0 | VPS-01: decisão e versão registrada |
| REQ-08 | Monitorar antes do primeiro teste embarcado | C | P0 | MON-01 e MON-02 anteriores a CEL-02 |
| REQ-09 | Isolar barcos entre si, inclusive caminhos L2 e IPv6 | P/V | P0 | SEC-01, SEC-02 |
| REQ-10 | Equipamentos de rede não expõem gerência à Internet | P/V | P0 | SEC-03: teste externo IPv4/IPv6 |
| REQ-11 | Gerência e telemetria sobrevivem a reboot/redeploy | P/V | P0 | OPS-01 e BAK-01 |
| REQ-12 | Não apresentar dado ausente como zero ou normal | Baseline/P | P0 | MON-02: perda de coleta induzida |
| REQ-13 | Documentar consumo, proteção e autonomia por kit | Demanda/C/V | P0 | ENE-01: ensaio e cálculo medido |
| REQ-14 | Alarme local funciona sem WAN e sem VPS | P/V | P0 | SECUR-01 |
| REQ-15 | Câmeras gravam localmente e permitem consulta sob demanda | Demanda/P/V | P1 | VIDEO-01 |
| REQ-16 | Avaliar serviço sem taxa inicial e mensalidade sustentável | C/V | P1 | COM-01: orçamento e margem |
| REQ-17 | Definir preventiva e visitas extraordinárias | Demanda/C/V | P1 | OPS-02 e COM-01 |
| REQ-18 | Coleta diferencia LAN, registro celular, sessão de dados, Internet, VPN e serviço | P/V | P0 | MON-03: falhas por camada |
| REQ-19 | Recuperação exige backup, sequência e verificação reais | Baseline/P | P0 | BAK-01, OPS-01 |
| REQ-20 | Versionar documentação na pasta e GitHub definidos | C | P0 | DOC-01: links, Git e SHA remoto |
| REQ-21 | Usar nocagent e Witteberg como referência rastreável | C | P1 | DOC-02: análise e mapeamento |
| REQ-22 | Vigia terceirizado é opção separada da operação de rede | Demanda/P | P1 | SECUR-01, COM-01: responsabilidades |
| REQ-23 | Avaliar WAN1 preferencial/WAN2 backup na central NOC, recuperando rotas sem desabilitá-las por script | Anexos/P/V | P1 | WAN-01 a WAN-07 |
| REQ-24 | Corrigir e validar o template recebido antes de qualquer import operacional | Anexos/P/V | P0 | DOC-03, ROS-01, SEC-03 e SEC-04 |
| REQ-25 | Integrar o gateway ativo da central NOC preservando LAN, DHCP, DNS e Internet | Coletas/C/V | P0 | NOC-01/02, VPN-01/02/03 e OPS-01 |
| REQ-26 | Não depender de central terrestre, core ou enlace WiFi na costa para entregar Internet aos barcos | C/V | P0 | CEL-07, VPN-03 |
| REQ-27 | Oferecer chips fornecidos pela operação com gestão individual contratada; Vivo permanece candidata | C/V | P0 | SIM-01, COM-01 |
| REQ-28 | Medir consumo por linha/ciclo, distinguir franquia de velocidade e validar políticas de alerta/controle | C/P/V | P0 | DATA-01, SIM-01, CEL-04 |
| REQ-29 | Peer e LAN exclusivos por barco, túnel iniciado a bordo e reconexão após mudança de IP/queda celular | P/V | P0 | VPN-01/02/03, CEL-06, SEC-01/02 |
| REQ-30 | Vídeo sob demanda, telemetria e atualizações cabem no orçamento de dados; funções locais continuam sem SIM/WAN | P/V | P0 | DATA-01, SECUR-01, VIDEO-01, ENE-01 |
| REQ-31 | Monitorar tensão, corrente e estado de carga válido por barco, com precisão/consumo verificados | Usuário/C/V | P0 | IOT-01, IOT-05 |
| REQ-32 | Detectar fumaça com alarme local e evento no NOC; distinguir limitações de supervisão | Usuário/C/V | P0 | IOT-02, IOT-05 |
| REQ-33 | Monitorar funcionamento da bomba e permitir acionamento remoto quando viável, preservando automático local | Usuário/C/V | P0 | IOT-03, IOT-04 |
| REQ-34 | Telemetria IoT por barco com origem/idade, entrega de eventos, baixo consumo e comandos isolados | Usuário/C/P/V | P0 | IOT-04, IOT-05, DATA-01, SEC-01/04 |

## Requisitos não funcionais propostos

- Falha da Internet da central NOC não deve interromper Internet própria dos barcos ou coleta na VPS.
- Falha da VPS deve preservar Internet local e funcionamento autônomo de alarme/gravação; haverá lacuna na observação central.
- Especificações e inventário público não contêm identificação pessoal ou segredos.
- Coleta de PoC tem resolução pretendida de 5 s para celular/tráfego em ensaio limitado por orçamento de dados e sonda ICMP local de 1 s durante ensaio controlado; suporte e custo serão medidos.
- Metas de aplicação, perda, recuperação e latência são metas de homologação propostas em [PoC](../06-validation/POC_PLAN.md), não SLA comercial.

## Mudança de requisito

Registrar motivo, impacto, decisão e teste afetado. Requisito removido permanece no histórico como substituído; não apagar evidências de uma reprovação.

## Evidência operacional consolidada — 17/09/2026

REQ-05/06/08/10/11/18/19 têm avanços medidos: stack e coleta interna, VPN notebook, volumes nomeados, backup S3/restauração isolada, restrições públicas TCP IPv4, reboot controlado e alertas SES/Telegram. [Mapa de implementações](IMPLEMENTATION_STATUS.md) e [homologação](../06-validation/HOMOLOGATION.md).

REQ-11/19 permanecem parciais pela recuperação integral e teste da chave externa, não por falta de reboot. REQ-05/10 não homologam RBs, UDP/IPv6 externo, revogação ou isolamento de campo. Alertas de backup ativos não equivalem a templates/coleta de equipamentos. Retenção local 7/4/3 e S3 sete dias são políticas distintas; exclusão efetiva, RPO/RTO e cobertura integral do lifecycle ainda em validação.

## Rastreabilidade da mudança — 29/09/2026

REQ-02 original (50/100 m por enlace WiFi) e REQ-03 original (wAP ax cliente/AP) estão substituídos pela redação celular, sem aceite retroativo. RF-01 a RF-05 ficam retirados/não executados na matriz; CEL-01 a CEL-07, SIM-01 e DATA-01 recebem os novos critérios. REQ-04 deixa de exigir RB750Gr3 como core. ADR-022/023 registra motivo e consequências. Nenhuma evidência VPS/NOC é evidência de cobertura ou contrato móvel.

## Alternativa de implementação com placas disponíveis

Usuário confirmou possuir UNO, MEGA e Raspberry Pi 4B, sem sensores, para testes. Avaliar reaproveitamento e INA226/INA228 conforme ADR-025, mantendo integralmente REQ-31–34; menor preço de hardware não reduz os critérios de qualidade, energia, alarme local ou independência da bomba. Revisões e pinagem das interfaces pendentes. [Procedimento de protótipo](../01-architecture/IOT_LOW_COST_PROTOTYPE.md).

Complemento do inventário: LM2596 com display e módulo GSM/GPRS possivelmente SIM800L. Reaproveitamento condicionado a ENE-01/IOT-05; modem 2G, se confirmado, não satisfaz REQ-03 nem substitui o ensaio 4G. Nenhuma alteração nos critérios de aceite.
