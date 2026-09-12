# Workflow de verificação

## Documentação

- Conferir Markdown UTF-8, títulos, blocos de código e links locais.
- Validar endereços, /30, VLANs, gateways e rotas de retorno.
- Conferir requisitos contra matriz de testes.
- Revisar credenciais, dados pessoais, afirmações de implantação e fontes.
- Executar `git diff --check`; revisar o conteúdo staged antes de commit.

## Infraestrutura futura

Executar bancada e campo correspondentes à alteração. Testar falhas e retorno, não somente o caminho feliz. Registrar resultado, timestamp e origem; não preencher a homologação por dedução.

## Git

Após commit/push, comparar SHA local e remoto e conferir working tree limpa. Não usar force-push para contornar divergência. Não escrever sucesso de publicação antes da confirmação do Git.
