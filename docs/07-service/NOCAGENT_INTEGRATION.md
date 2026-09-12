# Referência e futura integração NOC-Agent

Estado: evolução opcional planejada. O NOC-Agent não foi implantado nem conectado à Guarderia. O monitoramento inicial funciona com Zabbix/Grafana/Kuma sem IA.

## Integração mínima proposta

Consumir API oficial Zabbix por token de leitura, com escopo reduzido e TLS validado. A API é JSON-RPC; autenticação e métodos devem ser compatíveis com a versão instalada. Não reutilizar automaticamente parâmetros de login/auth legados do driver de referência. Fonte: [API Zabbix 7.0](https://www.zabbix.com/documentation/7.0/en/manual/api).

Fluxo: Zabbix coleta → eventos/métricas → integração autenticada → diagnóstico contextual. Primeira fase é leitura sob demanda; webhook é evolução com assinatura/segredo, proteção contra replay, deduplicação e controle de taxa.

## Contrato lógico

Entidades: site, barco, equipamento, interface, métrica, evento e incidente. Campos mínimos de observação: ID estável, origem, timestamp UTC, unidade, valor ou null, estado de qualidade e versão do coletor. Descrições e logs dos equipamentos são dados não confiáveis, não instruções para IA.

Estados normalizados: normal, atenção, problema, sem dados e manutenção. Permissão efetiva é a interseção do usuário, integração, site, barco e tipo de operação. Falha no provedor de IA não pode interromper alertas determinísticos.

## Ações futuras

Se forem solicitadas depois, cada ação mutável exige parâmetros tipados, alvo cadastrado, autorização, pré-verificação, snapshot, trava por equipamento, execução idempotente, pós-verificação e rollback conhecido. Não oferecer shell arbitrário ou gerar rollback por texto livre do modelo.

## Aceite INT-01

Token de leitura não altera hosts/configuração; acesso a outro escopo falha; certificado inválido é recusado; campo ausente continua nulo; log malicioso não vira comando; repetição de evento não duplica incidente; indisponibilidade de IA não interrompe coleta. Integração com WhatsApp/Chatwoot só será feita quando explicitamente definida e autorizada.
