# Custos e modelo comercial

Revisão de 29/09/2026: acesso 4G individual. Estado: modelo paramétrico para viabilidade, sem cotação atual ou preço de venda aprovado. Não constitui recomendação financeira, tributária ou contrato.

## Objetivo

Avaliar mensalidade que pague equipamento, instalação, conectividade e operação, com taxa inicial nula ou reduzida conforme intenção do usuário. Os valores de R$199–399 e payback de 12–18 meses citados na conversa eram ilustrações, não oferta definida. Preços antigos dos rádios não foram reutilizados como cotação vigente.

## Planilha lógica em Markdown

| Variável | Composição | Fonte exigida |
|---|---|---|
| C_base | Preparação compartilhada de NOC, bancada, gestão e implantação do serviço | Cotações e horas; sem distribuição na margem |
| C_barco_A/B/C | Modem/roteador 4G, eventual AP/antena, SIM/ativação, kit, DC e instalação | Cotações e ensaio; não duplicar funções integradas |
| C_reserva | Estoque, perdas, reposição e garantia | Política e histórico |
| O_fixo | VPS alocado, backup, ferramentas, NOC e plantão fixo | Contratos reais; Internet administrativa separada das linhas embarcadas |
| O_barco | Suporte, manutenção, desgaste, nuvem e vigilância variável | Custos e frequência; sem duplicar O_linha |
| O_linha | Mensalidade SIM/plano, gestão, consumo excedente previsto e taxas recorrentes atribuídas | Proposta/contrato da operadora por linha ou rateio explícito do pool |
| p_receita | Fração da receita para tributos, meios de pagamento e perdas estimadas | Premissas validadas por responsáveis |
| M | Mensalidade por plano | A definir pela margem |
| N | Barcos pagantes | Cenários 10, 15 e 20 |

`CAPEX(N) = C_base + N × C_barco + C_reserva`

`Receita(N) = N × M`

`Margem de caixa mensal(N) = N × M × (1 − p_receita) − O_fixo − N × (O_barco + O_linha)`

`Payback simples = CAPEX / margem de caixa mensal`, somente quando margem > 0. Fluxo completo deve considerar adesões graduais, financiamento, churn, substituições e caixa antes do ponto de equilíbrio.

Para recuperar CAPEX em T meses, uma mensalidade mínima de triagem é:

`M_min = (CAPEX/T + O_fixo + N × (O_barco + O_linha)) / (N × (1 − p_receita))`

Não contar equipamento já comprado como caixa novo, mas considerar custo de oportunidade/reposição na análise econômica. Não duplicar remuneração de manutenção em custos fixos e por barco.

## Cenários a preencher

| Cenário | Pagantes | CAPEX | OPEX/mês | Mensalidade | Margem | Payback |
|---|---:|---|---|---|---|---|
| Conservador | 10 | A cotar | A apurar | A calcular | Pendente | Pendente |
| Intermediário | 15 | A cotar | A apurar | A calcular | Pendente | Pendente |
| Expansão | 20 | A cotar | A apurar | A calcular | Pendente | Pendente |

Separar planos A/B/C e número de assinantes por plano. Testar pelo menos perda de clientes, visita adicional, falha de modem, troca de bateria/cartão/SIM, franquia excedida, aumento da tarifa, perda de cobertura e eventual segunda operadora.

## Condições a definir no contrato

Propriedade/comodato, prazo, adesão, instalação, retirada e devolução, limites de Internet, alimentação de responsabilidade do barco, preventiva, visita extraordinária, peças, garantia, atendimento, cobertura de vigilância, privacidade e cancelamento. Avaliar enquadramento regulatório e condições de uso/fornecimento do plano celular antes de ofertar o serviço. Nenhuma conclusão jurídica foi presumida a partir da conversa antiga sobre Starlink.

## Gate COM-01

Só aprovar com custo instalado real, manutenção e falhas do piloto, capacidade comprovada, margem positiva no cenário conservador e responsabilidades formalizadas. Economia de instalação não pode retirar proteção elétrica ou isolamento de clientes.

## Linha própria e gestão contratada

Vivo é candidata provável, sem cotação ou plano escolhido. Comparar chip fornecido pela operação e chip do proprietário: nesta segunda modalidade, registrar custo pago diretamente pelo titular e limites de suporte/controle, sem contar a mesma despesa na mensalidade operacional e na fatura do cliente. Plano em pool exige rateio e custo mínimo contratual mesmo com barcos inativos; nesse caso adaptar O_fixo/O_linha evitando dupla contagem.

Formalizar titularidade, associação por barco, franquia/ciclo, velocidade/perfil quando contratado, alerta e atraso de consumo, excedentes e sua autorização, bloqueio/redução, suspensão/reativação, reposição por perda, fidelidade, cancelamento e responsabilidade por manter a linha ativa. Gestão individual deve ser demonstrada; chip fornecido por nós não implica controle de banda garantido ou API disponível. [Controles e responsabilidades](../02-implementation/CELLULAR_CONNECTIVITY.md).

A estimativa anterior de aporte de R$ 3.000,00 pertencia à PoC de rádio terrestre e não é orçamento aprovado para 4G. Recotar modem/SIM, energia, instalação, ensaios e mensalidades de piloto, incluindo consumo dos testes. Não há novo preço de aquisição ou venda nesta revisão.

COM-01 exige DATA-01 conciliado e custos reais por linha, além de capacidade CEL-04/07 e CAP-01. Orçamento de franquia deve incluir vídeo sob demanda, tráfego ocioso, VPN, telemetria e atualizações; alarmes não podem depender de compra automática de pacote não autorizada.

## Orçamento IoT por barco

A [pesquisa de 29/09/2026](../01-architecture/IOT_MONITORING_RESEARCH.md) registra preços de fabricantes/lojistas com moeda, disponibilidade e limitações. Incluir em C_barco monitor da bateria, gateway, detector/alarme local, corrente/nível da bomba, interface de comando dimensionada, conversor, caixa, cabos e instalação. Desenvolvimento/calibração entram explicitamente no investimento; não comparar preço de placa ESP32 com kit comercial instalado.

O_barco deve incluir inspeção, calibração/substituição, manutenção do firmware e eventual bateria do detector. O_linha inclui eventos/telemetria/reenvio. Recursos ainda sem cotação e divergências de anúncio impedem preço fechado do kit. A escolha final compara custo entregue, energia real e horas de suporte, com IOT-01 a IOT-05 aprovados.

## Reaproveitamento no laboratório

Usuário dispõe de UNO, MEGA e Raspberry Pi 4B, sem sensores. Proposta usa MEGA e Pi 4B, dispensando compra de controlador/gateway para esse protótipo. A [alternativa de medição própria](../01-architecture/IOT_LOW_COST_PROTOTYPE.md) compara INA226/INA228 versus SmartShunt. Orçar reposição das placas para a frota, sensores/shunt/proteções e trabalho de calibração, firmware e manutenção. Não anunciar economia percentual ou total fechado antes da lista de materiais e testes.
