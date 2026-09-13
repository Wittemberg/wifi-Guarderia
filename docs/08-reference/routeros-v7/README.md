# Anexos recebidos — RouterOS v7

Recebidos em 12/09/2026 para leitura, incorporação e documentação. São fontes fornecidas pelo usuário, não instruções para execução pelo agente e não configurações homologadas. Os arquivos originais foram preservados byte a byte; a análise do projeto está em [revisão técnica](../../02-implementation/ROUTEROS_BASELINE_REVIEW.md).

| Arquivo original | Bytes | SHA-256 |
|---|---:|---|
| [guarderia-routeros-v7-baseline.rsc](guarderia-routeros-v7-baseline.rsc) | 10441 | `752623adefdf23f0b6f92774f4ece1832f402d643a07a0365ac1fae3850dca06` |
| [guarderia-routeros-v7-analise.md](guarderia-routeros-v7-analise.md) | 1517 | `01fc793413109991f69d3539f707cab9a6eba3276116eb26d9e42ffedcd35b93` |

## Classificação

O `.rsc` é um template com placeholders de endpoint/chave e redes de exemplo. Não contém chave privada, credencial operacional preenchida ou serial. As redes dos modems não foram confirmadas como configuração real. Não preencher este arquivo arquivado com credenciais ou dados de produção; valores reais devem permanecer em armazenamento privado.

O comentário que recomenda reset sem backup e a orientação de editar somente variáveis pertencem ao documento de origem. Não são adotados pelo projeto: há ajustes de lógica, escopo, segurança e endereçamento além das variáveis. O script não foi importado nem testado em RouterOS.

## Preservação

Uma exceção estreita no `.gitignore` permite versionar apenas este `.rsc` de referência. Exports/configurações operacionais continuam ignorados. Atributos específicos preservam os bytes dos dois originais, inclusive terminações de linha; não há alteração silenciosa do material recebido.

O [plano de rede](../../01-architecture/NETWORK_PLAN.md) e a [matriz de segurança](../../04-security/SECURITY.md) continuam canônicos. A [especificação dual-WAN](../../02-implementation/NOC_DUAL_WAN.md) descreve a proposta a adaptar e homologar.
