# Kits de segurança e responsabilidades do serviço

Estado: requisitos e alternativas comerciais, sem seleção final de modelos. A escolha de Intelbras é compatível com a experiência do usuário, mas modelos anteriores citados na conversa não estão homologados para esta instalação.

## Escopo solicitado originalmente

| Alternativa | Composição solicitada | Estado |
|---|---|---|
| A — Alarme | Central, 3 contatos sem fio, 2 sirenes interna/externa e luz externa | Especificação de compatibilidade pendente |
| B — Alarme e vídeo | A + câmera interna e externa com aplicativo remoto | Modelos e gravação pendentes |
| C — Vigilância | B + empresa de monitoramento/vigilância | Prestador e contrato pendentes |

A sugestão antiga de kit reduzido com dois sensores não substitui o pedido original. Qualquer redução deve aparecer como alternativa com diferença de cobertura e preço. A conectividade de cada kit usa a mesma infraestrutura de rede, com capacidade a validar.

## Requisitos da central e sensores

Verificar alimentação DC e bateria própria, autonomia, supervisão de sensores, alcance interno, compatibilidade do receptor, saídas para sirenes e sinalizador, capacidade de corrente e necessidade de módulo/relé. Sensores proprietários podem usar protocolo não WiFi; não cadastrar cada sensor como host IP sem suporte.

Testar porta, compartimento e abertura de tampa nos locais reais; vibração e movimento normal não devem gerar eventos indevidos. Validar comunicação com aplicativo e eventual prestador, falha/restauração de WAN e falta de alimentação. A central deve cumprir alarme local sem conexão à VPS.

## Requisitos de vídeo

Câmera externa com proteção e montagem adequadas ao ambiente; câmera interna conforme condição da cabine. Conferir visão noturna, consumo noturno/pico, gravação local, qualidade necessária, acesso por usuário e comportamento sem Internet. RTSP/ONVIF ou aplicativo são opções dependentes do modelo, não capacidades presumidas.

Dimensionar armazenamento por bitrate medido: `GB/dia ≈ Mbps × 10,8` para stream contínuo, antes de variação de codec/eventos. Validar ciclo de gravação, integridade de cartão, desgaste e retenção efetiva. Aplicativo pode usar nuvem/relay; medir upload e tempo de abertura no celular usando rede externa. VPS não recebe gravação contínua.

## Separação de serviços

Monitoramento técnico identifica conectividade, falhas e energia quando observável. Vigilância patrimonial recebe eventos e executa procedimentos contratuais. Um dashboard verde não significa barco protegido contra qualquer incidente. Quem recebe alarme, quem liga ao proprietário e quem se desloca deve estar explícito.

## Testes de aceite

SECUR-01: disparar cada sensor; confirmar sirenes/luz, recebimento autorizado, bateria e funcionamento sem WAN. VIDEO-01: registrar e consultar imagem interna/externa, evento noturno, retenção e recuperação de energia. Não filmar ou publicar pessoas para compor evidência técnica desnecessária.

## Evoluções

Tensão de bateria, água no porão, fumaça e bomba são possíveis extensões; dependem de sensores, calibração, alimentação e política de resposta específicos. Não anunciar segurança de vida ou prevenção de naufrágio como capacidade validada do kit WiFi.
