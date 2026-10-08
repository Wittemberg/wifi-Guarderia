# Riscos, lacunas e decisões pendentes

Revisão de 29/09/2026: distribuição costeira retirada; riscos de cobertura, linha e dados substituem base/enlace compartilhado. Não houve levantamento celular nesta revisão.

## Pendências

| ID | Informação/decisão | Quem resolve | Bloqueia |
|---|---|---|---|
| OPEN-01 | Parcial: IP, CPU visível, disco e arquitetura inventariados; Docker reconhece 9 CPUs/8 GiB e está em execução; console confirmado e WireGuard validado com notebook; confirmar recursos garantidos | Responsável técnico | Dimensionamento e recuperação integral |
| OPEN-02 | Parcial: serviços e portas inventariados; Docker Swarm e Traefik instalados; restrições TCP IPv4/reboot validados; faltam UDP/IPv6 externo, segregação interna, falha rpc_pipefs e diagnóstico dos VIPs | Responsável técnico | Instalação sem conflito |
| OPEN-03 | Parcial: awecloudsolution.com e A/CNAMEs publicados, resolução conferida na VPS; HTTPS inicial validado para Zabbix/Grafana/Kuma/Portainer; SSH por IP VPN confirmado; sete nomes HTTPS, restrições e logins pela VPN validados após reboot; renovação ACME e revisão integral pendentes | Responsável técnico | TLS e exposição controlada |
| OPEN-04 | Parcialmente resolvida: RB750r2 central NOC em RouterOS/RouterBOOT 7.23.7; inventário da RB750Gr3 ainda pendente | Responsável técnico | Avaliação de reaproveitamento; RB750r2 inventariada e VPN confirmada; kit 4G ainda a selecionar |
| OPEN-05 | Inventário de rede recebido; definir segregação administrativa, backup e integração; exemplo WAN1 do template conflita com a LAN ativa | Responsável técnico | IPAM e rotas |
| OPEN-06 | Modelo de modem/roteador 4G, eventual AP/antena, bandas, VPN, telemetria, homologação aplicável e garantia | Responsável técnico | Compra/instalação |
| OPEN-07 | Cobertura celular no fundeio, horários, movimento, obstáculos e posição do kit | Visita técnica | CEL-02/03 e montagem |
| OPEN-08 | Banco de baterias, química, cargas, autonomia desejada e energia solar | Proprietário + instalador | Kit embarcado |
| OPEN-09 | Modelos de central, sensores, sirenes, sinalizador e câmeras | Responsável técnico | Custo e compatibilidade |
| OPEN-10 | Operadora/plano (Vivo provável), APN, upload/download real, franquia/ciclo, gestão individual, custos e condições de fornecimento | Responsável técnico + provedor | Capacidade/comercialização |
| OPEN-11 | Imagens/digests da instalação registrados; substituir tags mutáveis e validar compatibilidade/plugin no manifesto de manutenção | Responsável técnico | Stack executável |
| OPEN-12 | Peer/chave por barco, isolamento no hub/kit, coleta LTE suportada, controle da linha e portas reais | Laboratório | Isolamento e métricas |
| OPEN-13 | Parcial: alertas de backup SES/Telegram ativos, destinatário definido e recebimento confirmado. Plantão, tempos de atendimento e alertas de equipamentos pendentes | Operação + cliente | Alertas de produção |
| OPEN-14 | Parcial: S3 diário/restauração isolada validados; chave externa confirmada pelo usuário; expiração de sete dias configurada pelo usuário e observada em dois objetos. Falta exclusão efetiva, revisão completa do lifecycle, teste da chave externa e recuperação integral | Responsável técnico | Homologação integral BAK-01 e RPO/RTO |
| OPEN-15 | Custos, contrato, tributos, vigilância e licença do projeto | Titular + especialistas | Oferta comercial |
| OPEN-16 | WAN1 estática inventariada; confirmar provedor/modem e segundo link na porta WAN2 reservada | Responsável técnico | Variante dual-WAN executável |
| OPEN-17 | Adaptar variáveis/escopos, parâmetros, ACLs e rotas do template RouterOS recebido | Responsável técnico + laboratório | ROS-01 e WAN-01 a WAN-07 |

### Novas pendências celulares

- OPEN-18: titularidade dos chips, portal/API disponível, política individual em eventual pool, velocidade/franquia, atraso de consumo, excedentes, suspensão e cancelamento — responsável comercial + operadora; bloqueia SIM-01/DATA-01/COM-01.
- OPEN-19: modelo final, recuperação local, telemetria LTE e energia em pico; antena/roteador complementar somente se necessários — responsável técnico + laboratório; bloqueia CEL-01/06 e ENE-01.
- OPEN-20: orçamento de dados da PoC, demanda e prazos das aplicações, critérios de cobertura e ciclo completo de conciliação — operação + cliente; bloqueia aceite de campo e expansão.

## Matriz de riscos

| Risco | Impacto | Tratamento | Critério de liberação |
|---|---|---|---|
| Cobertura celular fraca/variável no fundeio | Perda de acesso e alertas remotos | Medir horários, movimento e posições; avaliar antena/operadora conforme resultado | CEL-02/03/05 |
| Maresia/condensação/UV | Corrosão e indisponibilidade | Materiais compatíveis, montagem e inspeção | OPS-02 |
| Alimentação inadequada/descarga | Perda de serviço e dano | Projeto DC e medição, proteção independente | ENE-01 |
| PoE incompatível | Dano ao kit | Conferência tensão, padrão e polaridade | HW-01 |
| Todo gerenciamento passa pela VPS | Perda de observação/administração | Console, backups e operação local autônoma | BAK-01/VPN-03 |
| Mesma operadora/célula em vários barcos | Falha ou congestionamento comum | Medir concorrência e avaliar diversidade se necessária | CEL-07, CAP-01 |
| Ausência de dado aparece normal | Diagnóstico incorreto | Estado sem dados, idade e erro explícitos | MON-02 |
| Peers no mesmo hub sem ACL | Acesso entre barcos e ao NOC | Chave/prefixo exclusivo, filtro no hub/pontas e teste IPv6 | SEC-01/02 |
| Scripts/containers sem versão fixa | Deriva e quebra de compatibilidade | Manifesto, backup e rollback | STACK-01 |
| Firewall Docker diverge do host | Gerência exposta/rota quebrada | Teste externo e reboot do daemon | SEC-03/OPS-01 |
| Franquia excedida ou linha bloqueada | Custo e perda de gerência/alertas | Medir dados, conciliar ciclo e testar controles individuais | DATA-01, SIM-01 |
| Mensalidade insuficiente | Serviço inviável | CAPEX/OPEX, reposição, tributos e inadimplência | COM-01 |
| Import parcial ou aplicação do template ao equipamento errado | Perda de acesso e exposição de gerência | Revisão, adaptação, dry-run, backup e recuperação local | ROS-01, SEC-03/04 |

## Limite da conclusão

A arquitetura é uma proposta fundamentada. Não há garantia de cobertura, autonomia, capacidade celular ou rentabilidade até execução dos testes correspondentes.

## Dependência e limites atuais — 17/09/2026

RB750r2 inventariada e em uso como gateway; OPEN-05 requer desenho incremental e acesso de recuperação. Na VPS, volumes, restauração isolada S3, restrições TCP IPv4, reboot e alertas externos já têm aceite no escopo registrado. Próximo passo independente é preparar recuperação integral em ambiente separado. [Estado](IMPLEMENTATION_STATUS.md).

S3 tem janela de sete dias e versionamento observado desabilitado; a retenção longa é local e não sobrevive à perda da VPS. Exclusão futura e escopo completo do lifecycle ainda não conferidos. Alertas SES/Telegram estão ativos, mas dependem da AWS e não substituem teste de recuperação ou acompanhamento operacional.

Exceção de NAT local do Prometheus não identifica individualmente o Grafana. UDP externo, IPv6 externo, revogação/privilégios, renovação ACME e segurança de campo seguem pendentes. A unidade run-rpc_pipefs.mount já apresentava falha antes do reboot; não atribuí-la às mudanças sem investigação.

## Pesquisa IoT — novas pendências de 29/09/2026

- OPEN-21: geralmente 12 V e baterias veiculares/estacionárias confirmados; inventariar química/modelo/Ah, banco de partida/serviço, correntes e alimentação protegida por barco. Bloqueia shunt, calibração e IOT-01.
- OPEN-22: potência da bomba varia; levantar nominal/partida, automático e comando manual/interface do fabricante antes de dimensionar relé/contator e tempo de comando. Bloqueia IOT-03/04; atuação remota é solicitação confirmada, não autorização de alteração elétrica.
- OPEN-23: decidir gateway próprio versus comercial, condições de instalação do detector, alarme local e interfaces/caixa adequadas ao ambiente; cotar custo instalado e desenvolvimento. Bloqueia compra em lote.
- OPEN-24: broker/ingestão MQTT, ACL por barco, buffer/idade e serviço separado de comandos ainda não existem no escopo validado; testar IOT-02/04/05 e atualizar capacidade/franquia.

Riscos concretos: SoC incorreto por configuração/bypass, alarme de fumaça confundido com ppm, motor energizado confundido com drenagem, comando antigo reproduzido na reconexão e falha do gateway afetando automático. Tratamentos e testes na [pesquisa IoT](../01-architecture/IOT_MONITORING_RESEARCH.md).

- OPEN-25: UNO, MEGA e Pi 4B confirmados disponíveis, sem sensores; conferir revisões, fontes/interfaces e orçamento dos componentes. Necessário para pinagem, bibliotecas e fonte; variante INA226/INA228 exige calibração e SoC próprio, com ensaios de reset/USB/terra e consumo antes de comparar custo instalado.
