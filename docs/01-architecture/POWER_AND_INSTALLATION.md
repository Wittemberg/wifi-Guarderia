# Alimentação, instalação e ambiente marítimo

Estado: requisitos de projeto e ensaio. Sem inspeção da embarcação não há capacidade de bateria, bitola ou fusível final aprovado.

## Compatibilidade elétrica do kit 4G

Revisão de 29/09/2026: medir modem/roteador 4G, eventual roteador VPN/AP separado, alarme, câmeras e armazenamento. Modelo e faixa DC/PoE ainda pendentes; não reutilizar os consumos de mANTBox/wAP do projeto anterior. Conferir tensão, polaridade, corrente de pico, conversor e fonte conforme SKU real antes de energizar. Incluir transmissão celular intensa, registro/reconexão e atualização no ensaio.

## Diagrama funcional

```text
Banco DC da embarcação
  → proteção próxima à origem
  → seccionamento e proteção contra descarga conforme projeto
  → conversão DC/DC estabilizada adequada à carga
      → modem/roteador 4G e AP local, se separado (entradas compatíveis)
      → central/backup próprio
      → câmeras
      → sirenes/sinalizador (considerar pico)
```

O circuito deve ter polaridade identificada, terminação firme, proteção de contatos e possibilidade de manutenção sem desligar circuitos essenciais da embarcação. Instalação elétrica final deve ser dimensionada por profissional competente para o local e o banco de baterias utilizado.

## Dimensionamento paramétrico

Para cada dispositivo registrar potência em repouso, operação e pico, horas de uso, tensão e eficiência do conversor. Para cargas contínuas:

`Energia diária na bateria (Wh) = Σ(Pcarga × horas / eficiência)`

`Capacidade nominal (Ah) = Energia do período / (Vnominal × fração utilizável × fator de envelhecimento)`

A eficiência deve ser incluída uma única vez. Registrar limite de descarga recomendado para a química real, temperatura, envelhecimento e consumo preexistente do barco. Não reservar toda a bateria de partida para o sistema. Calcular queda de tensão com comprimento de ida e volta e corrente máxima; dimensionar proteção pela capacidade dos condutores e equipamento.

**Exemplo exclusivamente matemático:** carga hipotética de 9 W contínuos e conversão de 90% exige 240 Wh/dia na bateria; a 12 V equivale a 20 Ah/dia antes da limitação de descarga e demais cargas. Isso não dimensiona alarme/câmeras nem constitui medição de modem em uso.

## Solar e backup

Painel solar é opção, não requisito confirmado. Dimensionar pela energia diária total, insolação efetiva, perdas do controlador e dias de autonomia, incluindo sombreamento do mastro. Uma fonte que mantém o modem ligado não comprova que o banco recupera carga diariamente.

A distribuição na margem foi retirada. A energia do NOC continua escopo próprio. Em cada barco, simular retorno da alimentação e registrar sequência de boot, registro 4G, WAN, VPN e retomada da coleta.

## Montagem

- Conferir materiais, fixação e proteção de cabos adequados a maresia, UV, vibração e abrasão.
- Usar prensa-cabos apropriados, alívio de tração, identificação nas duas pontas e percurso com laço de gotejamento.
- Respeitar instruções de montagem do fabricante; evitar enclausuramento que aqueça ou bloqueie a antena.
- Projetar proteção contra surtos e aterramento/equipotencialização conforme o ambiente; não improvisar ligação a massas/terra da embarcação.
- A classificação IP declarada descreve proteção do invólucro e não comprova resistência prolongada à corrosão salina.

## Ensaio ENE-01

Medir tensão na bateria e na entrada de cada carga, corrente em repouso, gravação noturna, transmissão e disparo de sirenes/luz. Registrar pico e duração; testar autonomia acordada sem ultrapassar limite de descarga. Aprovar somente se não houver resets, aquecimento anormal, queda abaixo da faixa de operação ou comprometimento dos circuitos do barco.

## Manutenção proposta

Inspeção após 30 dias do piloto e, provisoriamente, a cada seis meses; encurtar conforme corrosão/umidade observada. Registrar contatos, vedação, fixação, cabos, fusíveis, baterias, microSD, sensores, sirenes e teste de autonomia. Periodicidade final e custo ficam no contrato após o piloto.

## Kit IoT — dimensionamento pendente

Usuário informou em 29/09/2026: geralmente 12 V, baterias veiculares comuns/estacionárias e bombas de potência variável. [Pesquisa de consumo e dispositivos](IOT_MONITORING_RESEARCH.md). Levantar tensão máxima durante carga/transientes, capacidade/estado do banco, corrente de partida e cargas que atravessarão o shunt; 300/500 A não representa capacidade da bateria em Ah.

Incluir gateway, interfaces, conversor, detector e sensor de corrente no ensaio ENE-01/IOT-05. Consumo em deep sleep não é consumo de telemetria continuamente disponível. Circuito de monitoramento deve ter proteção e acesso de manutenção sem interromper bomba/automático. Projeto de comando remoto é adicional, dimensionado por barco; nenhuma ligação foi executada nesta pesquisa.

## Conversor disponível para bancada

Usuário dispõe de LM2596 ajustável com display; corrente contínua, proteção e estabilidade da placa não verificadas. Avaliar conforme o [protótipo](IOT_LOW_COST_PROTOTYPE.md), mantendo referência de fonte própria do Pi 4B e tensões separadas para eventual SIM800L. ENE-01/IOT-05 devem incluir ajuste conferido por multímetro, partida, ripple, carga, temperatura, cabos e consumo do display; não inferir capacidade da placa pela especificação do CI.
