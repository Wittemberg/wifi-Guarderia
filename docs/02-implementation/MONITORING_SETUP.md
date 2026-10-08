# Configuração inicial do monitoramento

Estado em 16/09/2026: serviços instalados e coleta complementar Prometheus concluída, conforme [procedimento](../03-monitoring/PROMETHEUS_INTERNAL_COLLECTION.md). Este roteiro continua aplicável aos templates, alertas e integração Zabbix/Grafana ainda não homologados; integração das RBs à VPN, inventário e conta de leitura permanecem dependências para equipamentos. O túnel do notebook e seu SSH à VPS estão validados, sem comprovar coleta remota de equipamentos.

## Ordem de configuração

1. Registrar versões de Zabbix, banco, Grafana/plugin e Kuma no manifesto.
2. Configurar relógios e timezone de apresentação; criar usuários/papéis mínimos.
3. Cadastrar VPS, RB da central NOC, roteador/modem 4G e dispositivos do barco de bancada com IDs do inventário.
4. Validar conexão SNMPv3/API e capacidade real antes de associar template.
5. Habilitar recursos/interfaces e descoberta controlada, excluindo interfaces irrelevantes ou voláteis.
6. Criar coleta celular mestre e itens dependentes quando necessário, com erro/estado explícito.
7. Configurar sondas para LAN, Internet celular e peer do barco, distinguindo local de remoto.
8. Aplicar retenção e revisar volume estimado antes do perfil de 5 s.
9. Criar dependências de alertas e manutenção com início/fim.
10. Criar dashboards e canal de notificação de teste autorizado.
11. Exportar templates/provisioning sanitizados para Git e fazer backup dos valores privados.
12. Executar MON-01/02/03 e teste de restart antes de mover o kit 4G para campo.

## Organização Zabbix proposta

Grupos: `Guarderia/Infraestrutura`, `Guarderia/Barcos`, `Guarderia/NOC` e `Guarderia/Administracao`. Tags: `site=GV`, `role=modem|router|ap_local|boat|noc|admin` e `boat=001` quando aplicável. Não usar nome de pessoa/embarcação como label público.

Templates lógicos a elaborar: base RouterOS por SNMP, modem LTE por capacidade, sonda ICMP, host Linux/NOC e aplicação Zabbix. Nome/versão exatos dos templates serão definidos após seleção dos oficiais disponíveis e revisão. Não duplicar itens já expostos por template confiável.

## Coletor celular

Contrato mínimo: timeout limitado, sem chamadas sobrepostas por dispositivo, agenda persistente/configurada, credencial por referência, verificação TLS, validação de payload e erro sanitizado. Conservar registro celular, RSRP/RSRQ/SINR e contadores conforme suporte do modelo; SIM/célula reais ficam privados. Recurso não suportado é identificado; falha de autenticação não vira fallback silencioso.

Antes de desenvolver coletor, verificar se template/mecanismo oficial da versão já atende. Se não atender, registrar necessidade e gerar implementação pequena com testes de payload real sanitizado, timeout e reset de contador. Não enviar segredo para item dependente ou frontend.

## Sondas

Zabbix deve registrar enviados/recebidos para perda, janela e timeout. Ferramenta ICMP dentro de container pode precisar de permissão específica; conceder somente capacidade necessária depois de testar a imagem, sem `privileged` genérico.

Sonda local da PoC grava a bordo para separar LAN, Internet celular e VPN. Sem esse host, a sonda central mede o caminho combinado e não comprova causa de uma perda de comunicação.

## Grafana e Kuma

Plugin Zabbix fixado e compatível; token de leitura armazenado no servidor. Proibir acesso anônimo. Dashboards usam datasource real, estados sem dados, legenda de unidade e marcações da PoC. Não reconstruir alarmes diferentes no Grafana sem motivo, para evitar múltiplas fontes de incidentes.

Kuma monitora alvos e serviços mínimos com nomes lógicos. Página pública desabilitada por padrão; exposição depende de revisão de quais informações podem ser mostradas. Notificações duplicadas de Kuma/Zabbix devem ser evitadas.

## Aceite

MON-01: valor coincide com fonte direta e preserva unidade/origem. MON-02: credencial inválida, campo ausente e coletor parado aparecem corretamente. MON-03: corte da WAN produz incidente de caminho e preserva a distinção entre LAN, registro celular, Internet, VPN e aplicação. Em seguida, OPS-01 e BAK-01 validam persistência e recuperação.

## Integração de consumo por linha — proposta de 29/09/2026

Cadastrar `line_id` lógico e operadora sem ICCID/IMSI público. Na PoC, importar relatório ou registrar leitura manual datada; API só após contratação e validação. Persistir ciclo, fonte, unidade, atraso e baseline de contadores. Testar DATA-01 e SIM-01 separadamente da coleta de rede. Definir intervalo de operação conforme orçamento de dados e medir overhead de coleta/VPN antes de habilitar 5 s em campo.
