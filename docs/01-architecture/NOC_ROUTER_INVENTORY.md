# Inventário do MikroTik da central NOC

Registro recebido em 12/09/2026. Fonte: saídas de `/system resource print`, `/system package print` e `/system routerboard print` fornecidas pelo usuário. Não houve consulta remota pelo agente. O número de série foi omitido da documentação pública.

## Estado e próxima etapa

**RB951G-2HnD atualizada e pronta para configuração assim que a VPS estiver configurada**, conforme informado pelo usuário. RouterOS e RouterBOOT estão na versão 7.23.5. Isso registra a atualização do equipamento, não a implantação de WireGuard, firewall ou rotas do projeto.

“Central NOC” designa o local administrativo e sua RB951G; os serviços centrais de monitoramento ficam na VPS. Identidade atual observada no prompt: `RB951G`. Identidade proposta para o projeto: `GV-NOC-01`, ainda não aplicada.

## Recursos observados

| Campo | Valor fornecido |
|---|---|
| Modelo / board-name | RB951G-2HnD |
| Plataforma | MikroTik |
| Arquitetura | mipsbe |
| RouterOS | 7.23.5 (long-term) |
| Build-time | 2026-09-04 05:32:46; timezone não informado na saída |
| CPU | MIPS 74Kc V4.12 |
| Núcleos / frequência | 1 / 600 MHz |
| Carga CPU na amostra | 2% |
| Memória total / livre | 128,0 MiB / 84,1 MiB |
| Armazenamento total / livre | 128,0 MiB / 108,3 MiB |
| Uptime na amostra | 4 min 8 s |
| Setores gravados desde reboot | 20 |
| Setores gravados acumulados | 16.226.443 |
| Bad blocks reportados | 0,1% |

CPU, memória livre e uptime são valores pontuais, não indicadores de capacidade sob carga do projeto. O indicador de bad blocks fica registrado para comparação em inventários posteriores; esta amostra isolada não constitui diagnóstico de falha ou teste de integridade.

## Pacotes

| Pacote | Estado conforme saída | Versão | Build-time | Tamanho |
|---|---|---|---|---|
| wireless | Sem flags X/A | 7.23.5 | 2026-09-04 05:32:46 | 1388,1 KiB |
| routeros | Sem flags X/A | 7.23.5 | 2026-09-04 05:32:46 | 10,9 MiB |
| calea | XA — desabilitado/disponível | Não informada | Não informado | 20,1 KiB |
| gps | XA — desabilitado/disponível | Não informada | Não informado | 24,1 KiB |
| iot | XA — desabilitado/disponível | Não informada | Não informado | 788,1 KiB |
| openflow | XA — desabilitado/disponível | Não informada | Não informado | 76,1 KiB |
| tr069-client | XA — desabilitado/disponível | Não informada | Não informado | 120,1 KiB |
| ups | XA — desabilitado/disponível | Não informada | Não informado | 44,1 KiB |
| user-manager | XA — desabilitado/disponível | Não informada | Não informado | 372,1 KiB |

A legenda fornecida define X como DISABLED e A como AVAILABLE. Não considerar os itens XA como funcionalidades configuradas para o projeto. O pacote `wireless` desta RB não é o `wifi-qcom` dos rádios AX candidatos.

## RouterBOARD / RouterBOOT

| Campo | Valor fornecido |
|---|---|
| routerboard | yes |
| firmware-type | ar9344 |
| factory-firmware | 3.17 |
| current-firmware | 7.23.5 |
| upgrade-firmware | 7.23.5 |

## Pendências delimitadas

1. Configurar a VPS e disponibilizar o endpoint WireGuard.
2. Conferir interfaces, endereçamento existente, acesso de recuperação e backup da RB951G antes da mudança.
3. Aplicar configuração da central NOC conforme [provisionamento](../02-implementation/MIKROTIK_PROVISIONING.md) e [WireGuard](../02-implementation/WIREGUARD.md).
4. Executar testes VPN-01/02/03 e medir recursos sob carga real.

O inventário da RB750Gr3 do core permanece pendente. A atualização desta RB951G não encerra HW-01 para todos os equipamentos.
