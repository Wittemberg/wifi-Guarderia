# Orientações do projeto

## Leitura inicial

Leia [README](README.md), [memória](.agents/memory/MEMORY.md), [requisitos](docs/00-project/REQUIREMENTS.md) e o documento do domínio que será alterado. A baseline corporativa está em [witteberg-development-standards](witteberg-development-standards/README.md).

## Regras de trabalho

- Documentação e comunicação em português do Brasil; UTF-8; caminhos relativos nos documentos versionados.
- Distinguir confirmado pelo usuário, proposta técnica, pendente de validação e resultado medido. Documento concluído não significa serviço implantado.
- Não produzir telemetria fictícia, sucesso presumido, OID inventado, disponibilidade calculada a partir de uma porta TCP ou capacidade de hardware não observada.
- Preservar a pasta local e o repositório oficial. Não copiar dados privados do projeto de referência.
- Alterações relevantes devem atualizar requisitos, decisões, procedimentos, homologação e changelog afetados no mesmo conjunto.
- Segredos, chaves, exports reais, dumps, imagens de câmeras e identificação de clientes não entram no Git.
- Autorizações já dadas pelo usuário continuam válidas dentro do seu escopo. Preparação documental e versionamento não autorizam implantação em produção ou envio de mensagens a terceiros.
- Antes de mudar rotas, firewall, rádio ou energia de equipamentos em uso: inventário, backup protegido, plano concreto, acesso de recuperação e pós-teste. Registrar o escopo autorizado.
- Não executar scripts de terceiros diretamente do download. Examinar versão, conteúdo e efeito no host antes da instalação.
- Usar testes proporcionais: links e consistência para Markdown; laboratório e campo para rede. Não marcar homologação sem evidência.
- Subagentes somente quando solicitados pelo usuário ou por uma instrução aplicável; este arquivo não exige delegação.

## Limites da adaptação

A pasta `.agents` contém orientações de projeto em Markdown. Não instala AG Kit, hooks, MCP, plugins ou runtime Antigravity. Regras e skills do `nocagent` foram usadas como referências seletivas; não prevalecem sobre instruções do usuário ou do ambiente.
