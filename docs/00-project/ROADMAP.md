# Plano de execução

Revisão de 29/09/2026: acesso 4G próprio por barco, sem distribuição na costa. Não há prazo, compra ou implantação celular autorizados por esta revisão documental.

| Fase | Entrega | Dependência e saída | Estado |
|---|---|---|---|
| F0 | Especificação revisada e rastreabilidade | DOC-01/02, ADR-022/023 e revisão de links/IPAM | Revisão documental; publicação não presumida |
| F1 | Inventário do kit e levantamento celular/comercial | HW-01; modem/APN/SIM, cobertura preliminar, recuperação e orçamento de dados | NOC/VPS inventariados; kit/linha pendentes |
| F2 | Hub e stack NOC | VPN-01/02 no escopo administrativo, STACK-01 e recuperação integral | Implantação existente preservada; homologação integral parcial |
| F3 | Templates e consumo em bancada | MON-01/02/03, DATA-01 inicial e alertas de equipamentos | Pendente; alertas de backup existentes não substituem esta fase |
| F4 | Kit 4G, VPN e isolamento em bancada | CEL-01/06, LAN-01, VPN-01/02/03, SEC-01/02/03/04; segundo peer de teste | Pendente |
| F5 | Campo nos locais reais | F3/F4 e alimentação aprovada; CEL-02/03/04/07, ENE-01 | Pendente |
| F6 | Piloto prolongado e segurança | CEL-05, SECUR-01, VIDEO-01, OPS-02 e ciclo DATA-01 | Pendente |
| F7 | Gestão de linhas e viabilidade | SIM-01, DATA-01, CAP-01 e COM-01; proposta/contrato formalizado | Vivo provável; operadora/plano/custos pendentes |
| F8 | Lotes até 20 barcos | Aceite por barco e repetição de capacidade, isolamento e consumo | Pendente |

## Próximas ações

Preparar comparação do kit 4G e levantamento no fundeio, obter proposta de operadora com gestão individual e definir critérios do piloto. Após autorização operacional própria, usar um kit e SIM de teste; um segundo kit/linha ou bancada equivalente atende isolamento e gestão individual, mas somente dois kits reais permitem ensaio celular simultâneo CEL-07.

Na VPS, prosseguir com plano de recuperação integral em ambiente separado e chave externa. Reboot, restrições TCP IPv4 e alertas já validados não precisam de repetição sem nova causa. Preservar o gateway NOC em uso; nenhuma etapa depende de instalar core ou base na costa. [Estado](IMPLEMENTATION_STATUS.md).

## Expansão

Cada novo barco exige modem/SIM, IPAM, peer exclusivo, ACL, medição de energia/cobertura, monitoramento, política de dados e aceite. Comparar concorrência da rede celular e custos em lotes; o resultado de uma linha não garante vinte. Contrato em pool precisa de política individual e avaliação do impacto de franquia compartilhada.

Separar especificado, implantado, medido e aceite humano. Toda mudança operacional requer escopo, backup, acesso de recuperação e pós-teste. [PoC](../06-validation/POC_PLAN.md) e [riscos](RISKS_AND_OPEN_ITEMS.md).

## Ampliação IoT confirmada

Incluir inventário elétrico/sensores em F1; gateway/broker, qualidade e latência em F3; IOT-01 a IOT-04 em bancada F4; energia/latência/cobertura em F5; IOT-05 e estabilidade em F6; custo instalado/calibração em F7. A pesquisa não aprova compra nem atuação em bombas em uso. [Candidatos e critérios](../01-architecture/IOT_MONITORING_RESEARCH.md).
