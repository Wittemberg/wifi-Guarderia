# Riscos, lacunas e decisões pendentes

## Pendências

| ID | Informação/decisão | Quem resolve | Bloqueia |
|---|---|---|---|
| OPEN-01 | Parcial: IP, CPU visível, disco e arquitetura inventariados; Docker reconhece 9 CPUs/8 GiB e está em execução; console confirmado e WireGuard validado com notebook; confirmar recursos garantidos | Responsável técnico | Dimensionamento e recuperação integral |
| OPEN-02 | Parcial: serviços e portas inventariados; Docker Swarm e Traefik instalados; restrições TCP IPv4/reboot validados; faltam UDP/IPv6 externo, segregação interna, falha rpc_pipefs e diagnóstico dos VIPs | Responsável técnico | Instalação sem conflito |
| OPEN-03 | Parcial: awecloudsolution.com e A/CNAMEs publicados, resolução conferida na VPS; HTTPS inicial validado para Zabbix/Grafana/Kuma/Portainer; SSH por IP VPN confirmado; sete nomes HTTPS, restrições e logins pela VPN validados após reboot; renovação ACME e revisão integral pendentes | Responsável técnico | TLS e exposição controlada |
| OPEN-04 | Parcialmente resolvida: RB750r2 central NOC em RouterOS/RouterBOOT 7.23.7; inventário da RB750Gr3 ainda pendente | Responsável técnico | Provisionamento do core; RB750r2 inventariada; VPN funcional confirmada pelo usuário, carga e expansão pendentes |
| OPEN-05 | Inventário de rede recebido; definir segregação administrativa, backup e integração; exemplo WAN1 do template conflita com a LAN ativa | Responsável técnico | IPAM e rotas |
| OPEN-06 | Modelos/SKUs, aquisição, homologação aplicável e garantia dos rádios | Responsável técnico | Compra/instalação |
| OPEN-07 | Mapa da área, altura, obstáculos, maré, energia na margem | Visita técnica | RF e montagem |
| OPEN-08 | Banco de baterias, química, cargas, autonomia desejada e energia solar | Proprietário + instalador | Kit embarcado |
| OPEN-09 | Modelos de central, sensores, sirenes, sinalizador e câmeras | Responsável técnico | Custo e compatibilidade |
| OPEN-10 | Upload/download real, franquia e condições do provedor | Responsável técnico + provedor | Capacidade/comercialização |
| OPEN-11 | Imagens/digests da instalação registrados; substituir tags mutáveis e validar compatibilidade/plugin no manifesto de manutenção | Responsável técnico | Stack executável |
| OPEN-12 | VLAN por estação, credenciais por barco, coleta AX e portas reais | Laboratório | Isolamento e métricas |
| OPEN-13 | Parcial: alertas de backup SES/Telegram ativos, destinatário definido e recebimento confirmado. Plantão, tempos de atendimento e alertas de equipamentos pendentes | Operação + cliente | Alertas de produção |
| OPEN-14 | Parcial: S3 diário/restauração isolada validados; chave externa confirmada pelo usuário; expiração de sete dias configurada pelo usuário e observada em dois objetos. Falta exclusão efetiva, revisão completa do lifecycle, teste da chave externa e recuperação integral | Responsável técnico | Homologação integral BAK-01 e RPO/RTO |
| OPEN-15 | Custos, contrato, tributos, vigilância e licença do projeto | Titular + especialistas | Oferta comercial |
| OPEN-16 | WAN1 estática inventariada; confirmar provedor/modem e segundo link na porta WAN2 reservada | Responsável técnico | Variante dual-WAN executável |
| OPEN-17 | Adaptar variáveis/escopos, parâmetros, ACLs e rotas do template RouterOS recebido | Responsável técnico + laboratório | ROS-01 e WAN-01 a WAN-07 |

## Matriz de riscos

| Risco | Impacto | Tratamento | Critério de liberação |
|---|---|---|---|
| Nulos de antena durante rotação | Falha de conectividade | Testar 360° e outra posição/rádio se necessário | RF-03 |
| Maresia/condensação/UV | Corrosão e indisponibilidade | Materiais compatíveis, montagem e inspeção | OPS-02 |
| Alimentação inadequada/descarga | Perda de serviço e dano | Projeto DC e medição, proteção independente | ENE-01 |
| PoE incompatível | Dano a rádio | Conferência tensão, padrão e polaridade | HW-01 |
| Todo gerenciamento passa pela VPS | Perda de observação/administração | Console, backups e operação local autônoma | BAK-01/VPN-03 |
| Um core, um AP e uma WAN | Falha comum a todos | Assumir SPOFs na PoC; estoque e evolução | COM-01 |
| Ausência de dado aparece normal | Diagnóstico incorreto | Estado sem dados, idade e erro explícitos | MON-02 |
| LANs separadas sem ACL real | Acesso entre clientes | Isolamento L2/L3, anti-spoof e teste | SEC-01/02 |
| Scripts/containers sem versão fixa | Deriva e quebra de compatibilidade | Manifesto, backup e rollback | STACK-01 |
| Firewall Docker diverge do host | Gerência exposta/rota quebrada | Teste externo e reboot do daemon | SEC-03/OPS-01 |
| Escala aumenta ocupação RF | Perda e latência sob vídeo | Medir airtime e concorrência; novos setores | CAP-01 |
| Mensalidade insuficiente | Serviço inviável | CAPEX/OPEX, reposição, tributos e inadimplência | COM-01 |
| Import parcial ou aplicação do template ao equipamento errado | Perda de acesso e exposição de gerência | Revisão, adaptação, dry-run, backup e recuperação local | ROS-01, SEC-03/04 |

## Limite da conclusão

A arquitetura é uma proposta fundamentada. Não há garantia de cobertura, autonomia, número de setores ou rentabilidade até execução dos testes correspondentes.

## Dependência e limites atuais — 17/09/2026

RB750r2 inventariada e em uso como gateway; OPEN-05 requer desenho incremental e acesso de recuperação. Na VPS, volumes, restauração isolada S3, restrições TCP IPv4, reboot e alertas externos já têm aceite no escopo registrado. Próximo passo independente é preparar recuperação integral em ambiente separado. [Estado](IMPLEMENTATION_STATUS.md).

S3 tem janela de sete dias e versionamento observado desabilitado; a retenção longa é local e não sobrevive à perda da VPS. Exclusão futura e escopo completo do lifecycle ainda não conferidos. Alertas SES/Telegram estão ativos, mas dependem da AWS e não substituem teste de recuperação ou acompanhamento operacional.

Exceção de NAT local do Prometheus não identifica individualmente o Grafana. UDP externo, IPv6 externo, revogação/privilégios, renovação ACME e segurança de campo seguem pendentes. A unidade run-rpc_pipefs.mount já apresentava falha antes do reboot; não atribuí-la às mudanças sem investigação.
