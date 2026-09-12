# Baseline corporativa Witteberg — adaptação WiFi Guarderia

Esta é a baseline corporativa adotada pelo projeto. Origem: [padrões no nocagent](https://github.com/Wittemberg/nocagent/tree/e5ce6e3f9a84ca368472f771ef54f72e824b5a7c/witteberg-development-standards), consultados em 12/09/2026. Conteúdo local é síntese adaptada; não é cópia integral nem nova versão oficial dos padrões corporativos.

## Princípios

Recuperação automática de falhas transitórias quando segura, diagnóstico que identifica impacto e responsável, persistência de estado relevante e preservação do que já foi validado. Ausência de dado deve aparecer claramente; nunca entregar artefato ou sucesso fictício.

## Prioridades

| Nível | Significado na Guarderia |
|---|---|
| P0 | Impede operação segura, confiabilidade ou liberação do requisito afetado |
| P1 | Relevante à qualidade/continuidade, com impacto delimitado |
| P2 | Refinamento que não impede o fluxo principal |

Severidade operacional de um incidente depende do alcance; não é sinônimo automático do número de prioridade de desenvolvimento.

## Documentos normativos locais

- [Engenharia, persistência e segurança](ENGINEERING.md)
- [UX, estados e escrita](UX_AND_WRITING.md)
- [Checklist de entrega](RELEASE_CHECKLIST.md)

Os padrões de componentes web aplicam-se a futuros painéis customizados; não exigem construir frontend nesta fase. Qualquer divergência necessária deve ser registrada em ADR com motivo e testes.
