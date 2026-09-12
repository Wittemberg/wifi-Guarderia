# Checklist de entrega

Adaptação de `checklists/NEW-PROJECT.md`, `RELEASE.md` e `FRONTEND-REVIEW.md` da referência.

## Baseline documental

- [ ] Requisitos, arquitetura e fonte da verdade definidos.
- [ ] Stack e configurações pendentes explicitadas.
- [ ] Persistência, segurança e isolamento especificados.
- [ ] Coleta, logs e alertas têm origem e tratamento de erro.
- [ ] Backup, rollback e critérios de produção definidos.
- [ ] Referências e versão do snapshot registradas.
- [ ] Links, IPAM e Git revisados.

## Implantação futura

- [ ] Manifesto fixado e compatível com orquestrador real.
- [ ] Segredos externos e portas públicas testadas.
- [ ] Migração/backup/restore aprovados.
- [ ] Healthchecks e coleta real funcionais.
- [ ] Reboot/redeploy preserva configuração e dados.
- [ ] Isolamento e falhas ensaiados.
- [ ] Testes de campo aprovados para o escopo entregue.
- [ ] Painéis responsivos e legíveis em 100% quando aplicável.
- [ ] Aceite humano e limitações registrados.

Este checklist é modelo de processo. A execução real está na [homologação](../docs/06-validation/HOMOLOGATION.md), não nas caixas deste arquivo.
