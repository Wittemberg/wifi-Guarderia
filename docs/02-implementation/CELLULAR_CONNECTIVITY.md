# Conectividade 4G e gestão individual de linhas

Revisão de 29/09/2026. **Confirmado pelo usuário:** modem e chip próprios em cada barco, sem distribuição terrestre; possibilidade de a operação fornecer os chips com gestão individual pelo contrato da operadora. **Provável:** Vivo. **Pendente:** operadora, produto/plano, preço, cobertura, modem, APN, recursos de gestão e contratação. Nada aqui representa compra, ativação ou capacidade já disponível.

## Kit e critérios de seleção

Preferir, como proposta técnica, roteador 4G integrado que atenda LAN, firewall, VPN, telemetria e alimentação; alternativamente, modem separado mais roteador VPN. Um modem simples sem cliente VPN e sem roteamento gerenciável não atende sozinho. Avaliar por modelo/firmware: bandas LTE do local, SIM, interfaces, antenas/conectores, ventilação, consumo e pico de transmissão, recuperação após queda, atualizações, backup e acesso local de manutenção. Não há marca/SKU aprovado.

AP WiFi local pode ser integrado ou separado, conforme cobertura interna e compatibilidade do alarme/câmeras. Antena LTE externa só entra no kit se o levantamento indicar necessidade; compatibilidade, montagem e perdas de cabo devem ser verificadas. A retirada da infraestrutura na costa não dispensa avaliação de sinal e montagem a bordo.

## Duas modalidades de chip

| Modalidade | Gestão e responsabilidade | Condição |
|---|---|---|
| Fornecido pela operação | Operação contrata, associa linha ao barco e acompanha consumo, cobrança e suporte | Recursos e delegações individuais formalizados com a operadora |
| Fornecido pelo proprietário | Titular mantém plano, pagamento e autoriza o uso/suporte | Registrar limites de visibilidade; acesso ao portal e controle da linha não são presumidos |

Cada barco mantém seu SIM identificado mesmo que o contrato ofereça franquia agrupada. Se houver pool, exigir visibilidade e política por linha e explicitar impacto de consumo excessivo sobre as demais. Não presumir que toda linha terá franquia dedicada no contrato.

## O que significa controle de banda

| Controle | Onde pode existir | Verificação exigida |
|---|---|---|
| Franquia, consumo e ciclo | Portal/relatório/API da operadora, conforme contrato | Unidade, atraso, data de corte, pool ou franquia individual |
| Limite de velocidade | Perfil contratado da linha e/ou filas no roteador | Disponibilidade contratual e teste sob carga; velocidade configurada não é garantia do acesso 4G |
| Priorização de alarme/gerência | Roteador local | Capacidade real e comportamento sob saturação; QoS não cria cobertura ou franquia |
| Bloqueio, suspensão, reativação e troca de plano | Canal contratado da operadora | Prazo, permissões, rastreabilidade e impacto em acesso remoto |
| Alertas de consumo | NOC e/ou operadora | Limiar aprovado, fonte, atraso e destinatário autorizado |

Não prometer API, APN privada, IP fixo, velocidade mínima, bloqueio instantâneo ou franquia ilimitada sem confirmação. Operação manual pelo portal é aceitável na PoC, com registro; automação é evolução posterior. Contratar modalidade compatível com uso em roteador, câmeras, VPN e eventual fornecimento do serviço, após revisão das condições pelo responsável comercial.

## Cadastro protegido

Relacionar `boat_id`, `asset_id`, `line_id` lógico, operadora, plano, ciclo, franquia, titularidade, custo e referência do contrato. ICCID/IMSI, número da linha, IMEI, PIN/PUK, APN com credenciais, credenciais do portal e dados do titular ficam somente em inventário privado/cofre. Git e dashboards públicos usam IDs lógicos. Trocar SIM/modem não muda a identidade do barco nem autoriza reutilizar sua chave em outro equipamento.

## Provisionamento e retorno

1. Inventariar kit/linha e conferir uso permitido, cobertura preliminar, bandas, APN e acesso UDP ao endpoint. Mapa comercial é triagem, não aceite de campo.
2. Preparar backup, porta de recuperação e plano por equipamento; ativar um SIM piloto no escopo autorizado.
3. Validar registro 4G, sessão de dados, DNS/NTP, Internet e contadores com orçamento de dados do ensaio.
4. Configurar LAN, firewall, NAT WAN e peer exclusivo conforme [IPAM](../01-architecture/NETWORK_PLAN.md) e [WireGuard](WIREGUARD.md).
5. Aplicar política de consumo/velocidade proposta, comparar com portal e testar fila, alertas e impacto em vídeo/alarme.
6. Ensaiar perda de cobertura, mudança de endereço, retorno após reboot e suspensão/reativação em linha de teste autorizada. Não bloquear remotamente a única conexão sem recuperação local combinada.
7. Restaurar configuração anterior ou retirar apenas o cadastro piloto se o pós-teste falhar; confirmar acesso existente no NOC/VPS. Preservar evidências e atribuição da linha.

Revogação da VPN e cancelamento do SIM são ações distintas. Na retirada, encerrar cobrança/contrato da linha ou devolver ao titular conforme ordem autorizada, revogar o peer e remover rotas/ACLs daquele barco sem afetar os demais.

## Aceite

CEL-01 a CEL-07, SIM-01, DATA-01, VPN-01/02/03, MON-01/02/03, SEC-01/02/03/04, ENE-01 e COM-01 conforme [PoC](../06-validation/POC_PLAN.md) e [homologação](../06-validation/HOMOLOGATION.md). Gestão individual só é entregue depois de demonstrar leitura e alteração autorizada de uma linha sem impacto indevido nas outras.
