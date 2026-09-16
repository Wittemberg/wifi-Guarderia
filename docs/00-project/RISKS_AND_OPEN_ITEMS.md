# Riscos, lacunas e decisões pendentes

## Pendências

| ID | Informação/decisão | Quem resolve | Bloqueia |
|---|---|---|---|
| OPEN-01 | Parcial: IP, CPU visível, disco e arquitetura inventariados; Docker reconhece 9 CPUs/8 GiB e está em execução; console confirmado e WireGuard validado com notebook; confirmar recursos garantidos | Responsável técnico | Dimensionamento e recuperação integral |
| OPEN-02 | Parcial: serviços e portas inventariados; Docker Swarm e Traefik instalados; revisar exposição, segregação de redes, rpcbind e falha dos VIPs | Responsável técnico | Instalação sem conflito |
| OPEN-03 | Parcial: awecloudsolution.com e A/CNAMEs publicados, resolução conferida na VPS; HTTPS inicial validado para Zabbix/Grafana/Kuma/Portainer; SSH por IP VPN confirmado; concluir DNS/TLS dos novos nomes e painéis via VPN | Responsável técnico | TLS e exposição controlada |
| OPEN-04 | Parcialmente resolvida: RB951G central NOC em RouterOS/RouterBOOT 7.23.5; inventário da RB750Gr3 ainda pendente | Responsável técnico | Provisionamento do core; RB951G aguarda acesso do usuário e inventário de rede |
| OPEN-05 | Acesso à RB951G ainda indisponível; inventariar redes existentes da central NOC, provedor e VPNs para conferir sobreposições | Responsável técnico | IPAM e rotas |
| OPEN-06 | Modelos/SKUs, aquisição, homologação aplicável e garantia dos rádios | Responsável técnico | Compra/instalação |
| OPEN-07 | Mapa da área, altura, obstáculos, maré, energia na margem | Visita técnica | RF e montagem |
| OPEN-08 | Banco de baterias, química, cargas, autonomia desejada e energia solar | Proprietário + instalador | Kit embarcado |
| OPEN-09 | Modelos de central, sensores, sirenes, sinalizador e câmeras | Responsável técnico | Custo e compatibilidade |
| OPEN-10 | Upload/download real, franquia e condições do provedor | Responsável técnico + provedor | Capacidade/comercialização |
| OPEN-11 | Imagens/digests da instalação registrados; substituir tags mutáveis e validar compatibilidade/plugin no manifesto de manutenção | Responsável técnico | Stack executável |
| OPEN-12 | VLAN por estação, credenciais por barco, coleta AX e portas reais | Laboratório | Isolamento e métricas |
| OPEN-13 | Destinatários/canais/plantão e tempos de atendimento | Operação + cliente | Alertas de produção |
| OPEN-14 | Destino off-site, retenção aprovada, chaves e verba de backup | Responsável técnico | Recuperação |
| OPEN-15 | Custos, contrato, tributos, vigilância e licença do projeto | Titular + especialistas | Oferta comercial |
| OPEN-16 | Confirmar duas WANs da central NOC, modems, portas, IPs/gateways e modo estático/DHCP/PPPoE | Responsável técnico | Variante dual-WAN executável |
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

## Dependência atual — 16/09/2026

Hub/notebook conectados e SSH confirmado; OPEN-05 impede preparar a configuração real da RB951G. Não há chave/peer da RB, LAN conferida ou core integrado. Revisões de exposição, persistência e backup da VPS podem ser preparadas independentemente. Console confirmado e backups locais não resolvem OPEN-14 nem homologam restauração. Ver [roadmap](ROADMAP.md) e [validação](../06-validation/NOTEBOOK_VPN_VALIDATION.md).
