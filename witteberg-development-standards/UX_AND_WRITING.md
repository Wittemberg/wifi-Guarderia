# UX, estados e escrita

Adaptação dos padrões `frontend/*` e `components/*` do `nocagent`. Aplicação: dashboards configurados agora e eventuais interfaces próprias no futuro.

## Apresentação

PT-BR; zoom de referência 100%; validar desktop amplo, notebook, tablet e celular. Texto e ações devem caber no container sem exigir redução de zoom. Layouts em grade ajustam colunas; não esconder conteúdo para mascarar overflow. Cor reforça texto, nunca é o único indicador.

## Estados

| Estado técnico | Texto principal |
|---|---|
| healthy/online | Normal |
| degraded/warning | Atenção |
| down/critical | Problema |
| unknown/stale | Sem dados / Dados desatualizados |
| maintenance | Em manutenção |
| unsupported | Não suportado neste equipamento |
| reconnecting | Reconectando |

Mostrar horário da última coleta e detalhes de erro acessíveis. Reconhecer incidente não muda estado do equipamento. Ações mostram carregando, concluído ou falhou com orientação.

## Linguagem

Mensagem deve dizer o que houve, o impacto, o que fazer e quem age. Preferir “Sem comunicação com a base” com evidência a “Erro no sistema”. Deixar OID, interface e stacktrace sanitizado nos detalhes técnicos, sem competir com a tarefa do operador.

## Ações e formulários

Rótulos específicos, uma ação principal por contexto, foco de teclado preservado, campos com label real e confirmação de salvamento. Modais responsivos; ações destrutivas têm consequência clara. Interfaces aprovadas não são redesenhadas durante mudanças não relacionadas.

Não exibir dados fictícios para preencher cards. Um painel sem equipamento cadastrado deve explicar o estado e o próximo passo.
