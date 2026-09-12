# Contribuição e versionamento

## Fluxo

O checkout local e `origin` devem apontar para `Wittemberg/wifi-Guarderia`. O primeiro commit estabelece a baseline documental em `main`. Mudanças posteriores relevantes usam `feature/<assunto>`, `docs/<assunto>` ou `fix/<assunto>`, com revisão antes de integração.

1. Inspecionar `git status` e preservar alterações alheias.
2. Ler o documento canônico do domínio e mapear referências.
3. Alterar o menor escopo que resolva o requisito.
4. Revisar links relativos, endereçamento, estados e comandos.
5. Verificar `git diff --check` e ausência de segredos.
6. Atualizar o changelog e os registros de validação afetados.
7. Fazer commit descritivo, por exemplo `docs: define plano de coleta da PoC`.
8. Fazer push sem força e confirmar que o SHA remoto corresponde ao local.

## Fonte da verdade

Requisitos: `docs/00-project/REQUIREMENTS.md`; IPAM: `docs/01-architecture/NETWORK_PLAN.md`; decisões: `docs/01-architecture/DECISIONS.md`; estado: `docs/06-validation/HOMOLOGATION.md`. Outros documentos apontam para essas fontes e não criam alternativas silenciosas.

## Evidências

Dados medidos exigem origem, horário, unidade, equipamento e versão. Resultados sintéticos pertencem somente a testes explicitamente identificados, nunca a relatórios de operação. Evidências privadas são referenciadas por identificador e hash, sem URL pública ou credencial.

## Entrega

Informar problema resolvido, comportamento final, validações executadas, limitações e commit. Publicação no GitHub não deve disparar implantação na VPS nesta fase. A primeira entrega é exclusivamente documental.
