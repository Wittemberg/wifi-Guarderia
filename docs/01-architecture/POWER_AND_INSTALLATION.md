# Alimentação, instalação e ambiente marítimo

Estado: requisitos de projeto e ensaio. Sem inspeção da embarcação não há capacidade de bateria, bitola ou fusível final aprovado.

## Compatibilidade elétrica dos rádios

| Modelo | Entrada DC | PoE | Consumo máximo declarado |
|---|---|---|---|
| mANTBox ax 15s | 12–28 V | Passivo, 18–28 V | 11 W sem acessórios; 21 W total |
| wAP ax | 12–57 V | 802.3af/at, faixa declarada 18–57 V | 9 W |

Fontes: [mANTBox](https://mikrotik.com/product/mantbox_ax_15s) e [wAP ax](https://mikrotik.com/product/wap_ax). Usar injector/entrada compatível com a revisão recebida. Um switch PoE de 48 V não deve ser conectado diretamente à entrada passiva de 18–28 V da mANTBox. A RB750Gr3 não é tratada como fonte PoE para os rádios.

## Diagrama funcional

```text
Banco DC da embarcação
  → proteção próxima à origem
  → seccionamento e proteção contra descarga conforme projeto
  → conversão DC/DC estabilizada adequada à carga
      → rádio (entrada compatível)
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

**Exemplo exclusivamente matemático:** rádio de 9 W contínuos e conversão de 90% exige 240 Wh/dia na bateria; a 12 V equivale a 20 Ah/dia antes da limitação de descarga e demais cargas. Isso não dimensiona alarme/câmeras nem constitui medição do wAP em uso.

## Solar e backup

Painel solar é opção, não requisito confirmado. Dimensionar pela energia diária total, insolação efetiva, perdas do controlador e dias de autonomia, incluindo sombreamento do mastro. Uma fonte que mantém o rádio ligado não comprova que o banco recupera carga diariamente.

Na margem, somar core, ONT/roteador do provedor, switch, rádios e perdas. Ensaiar nobreak sob carga real e simular retorno de energia. Registrar sequência de boot e recuperação da WAN/VPN.

## Montagem

- Conferir materiais, fixação e proteção de cabos adequados a maresia, UV, vibração e abrasão.
- Usar prensa-cabos apropriados, alívio de tração, identificação nas duas pontas e percurso com laço de gotejamento.
- Respeitar instruções de montagem do fabricante; evitar enclausuramento que aqueça ou bloqueie a antena.
- Projetar proteção contra surtos e aterramento/equipotencialização conforme o ambiente; não improvisar ligação a massas/terra da embarcação.
- IP54/IP55 descreve proteção do invólucro e não comprova resistência prolongada à corrosão salina.

## Ensaio ENE-01

Medir tensão na bateria e na entrada de cada carga, corrente em repouso, gravação noturna, transmissão e disparo de sirenes/luz. Registrar pico e duração; testar autonomia acordada sem ultrapassar limite de descarga. Aprovar somente se não houver resets, aquecimento anormal, queda abaixo da faixa de operação ou comprometimento dos circuitos do barco.

## Manutenção proposta

Inspeção após 30 dias do piloto e, provisoriamente, a cada seis meses; encurtar conforme corrosão/umidade observada. Registrar contatos, vedação, fixação, cabos, fusíveis, baterias, microSD, sensores, sirenes e teste de autonomia. Periodicidade final e custo ficam no contrato após o piloto.
