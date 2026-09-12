# Custos e modelo comercial

Estado: modelo paramétrico para viabilidade, sem cotação atual ou preço de venda aprovado. Não constitui recomendação financeira, tributária ou contrato.

## Objetivo

Avaliar mensalidade que pague equipamento, instalação, conectividade e operação, com taxa inicial nula ou reduzida conforme intenção do usuário. Os valores de R$199–399 e payback de 12–18 meses citados na conversa eram ilustrações, não oferta definida. Preços antigos dos rádios não foram reutilizados como cotação vigente.

## Planilha lógica em Markdown

| Variável | Composição | Fonte exigida |
|---|---|---|
| C_base | Core, setores, switch, energia, montagem, instalação | Cotações e horas |
| C_barco_A/B/C | Rádio, kit, DC, montagem, instalação por alternativa | Cotações e ensaio |
| C_reserva | Estoque, perdas, reposição e garantia | Política e histórico |
| O_fixo | ISP, VPS alocado, backup, ferramentas, plantão fixo | Contratos reais |
| O_barco | Suporte, manutenção, desgaste, nuvem e vigilância variável | Custos e frequência |
| p_receita | Fração da receita para tributos, meios de pagamento e perdas estimadas | Premissas validadas por responsáveis |
| M | Mensalidade por plano | A definir pela margem |
| N | Barcos pagantes | Cenários 10, 15 e 20 |

`CAPEX(N) = C_base + N × C_barco + C_reserva`

`Receita(N) = N × M`

`Margem de caixa mensal(N) = N × M × (1 − p_receita) − O_fixo − N × O_barco`

`Payback simples = CAPEX / margem de caixa mensal`, somente quando margem > 0. Fluxo completo deve considerar adesões graduais, financiamento, churn, substituições e caixa antes do ponto de equilíbrio.

Para recuperar CAPEX em T meses, uma mensalidade mínima de triagem é:

`M_min = (CAPEX/T + O_fixo + N × O_barco) / (N × (1 − p_receita))`

Não contar equipamento já comprado como caixa novo, mas considerar custo de oportunidade/reposição na análise econômica. Não duplicar remuneração de manutenção em custos fixos e por barco.

## Cenários a preencher

| Cenário | Pagantes | CAPEX | OPEX/mês | Mensalidade | Margem | Payback |
|---|---:|---|---|---|---|---|
| Conservador | 10 | A cotar | A apurar | A calcular | Pendente | Pendente |
| Intermediário | 15 | A cotar | A apurar | A calcular | Pendente | Pendente |
| Expansão | 20 | A cotar | A apurar | A calcular | Pendente | Pendente |

Separar planos A/B/C e número de assinantes por plano. Testar pelo menos perda de clientes, visita adicional, falha de rádio, troca de bateria/cartão e necessidade de segundo setor.

## Condições a definir no contrato

Propriedade/comodato, prazo, adesão, instalação, retirada e devolução, limites de Internet, alimentação de responsabilidade do barco, preventiva, visita extraordinária, peças, garantia, atendimento, cobertura de vigilância, privacidade e cancelamento. Avaliar enquadramento regulatório e condições de uso/revenda do provedor antes de ofertar o serviço. Nenhuma conclusão jurídica foi presumida a partir da conversa antiga sobre Starlink.

## Gate COM-01

Só aprovar com custo instalado real, manutenção e falhas do piloto, capacidade comprovada, margem positiva no cenário conservador e responsabilidades formalizadas. Economia de instalação não pode retirar proteção elétrica ou isolamento de clientes.
