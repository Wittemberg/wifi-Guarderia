# Revisão da baseline documental

Os levantamentos e revisões abaixo preservam datas e resultados históricos. Para o estado vigente de implementação e pendências reais, consultar o [resumo consolidado](../00-project/IMPLEMENTATION_STATUS.md).

Data: 12/09/2026. Escopo: arquivos Markdown e configuração Git desta primeira entrega. Esta revisão não executa testes de equipamentos, VPS ou serviços.

## Verificações executadas na baseline 0.1.0

| Verificação | Estado |
|---|---|
| Links relativos e arquivos referenciados | 100 links locais resolvidos; nenhuma referência ausente |
| Títulos, UTF-8 e blocos de código | 45 arquivos Markdown verificados; nenhum erro detectado |
| Coerência dos 20 trânsitos /30, VLANs e LANs | 20 linhas verificadas por cálculo de prefixo, gateway e VLAN |
| Requisitos referenciados na homologação | IDs de teste dos requisitos encontrados na matriz |
| Revisão de segredos e dados pessoais | Nenhum padrão de chave/token detectado; escopo sanitizado revisado |
| Whitespace Git | `git diff --cached --check` sem erros |
| Commit local e publicação remota | Verificáveis pelo histórico Git e relatório final de entrega |

Verificação estrutural realizada com Python local sobre os arquivos, incluindo decodificação UTF-8, pares de blocos de código, resolução de caminhos relativos e cálculo dos prefixos IPv4. O inventário de referência inclui 392 arquivos catalogados do snapshot; catalogação não equivale a teste ou leitura integral de cada componente.

O SHA do próprio commit não é embutido nos documentos para evitar autorreferência. A confirmação de publicação é feita comparando `git rev-parse HEAD` com `git ls-remote origin refs/heads/main`, após o push, e conferindo `git status --porcelain` vazio.

## Revisão técnica

Foram explicitados: rotas de retorno, SNAT restrito de coleta, política IPv6, segregação L2/L3, credenciais por estação, limites de campo RF, diferenças de alimentação PoE, lacunas de coleta, semântica history/trends, backup container/host, TLS e separação entre especificação e homologação.

## Limitações

Atualização documental posterior em 12/09/2026: inventário da RB951G recebido do usuário, atualização RouterOS/RouterBOOT 7.23.5 registrada e denominação central NOC aplicada. A coleta foi realizada pelo usuário; não é homologação remota executada pelo agente. Os totais da tabela acima descrevem a baseline original.

Na baseline de 12/09, versões exatas, domínio, inspeção local, aquisição e resultados de campo dependiam da próxima fase; inventário/implantação e DNS foram atualizados nos registros de 15–16/09. Critérios numéricos de PoC são propostas de aceite. Nenhum script executável de implantação foi gerado sem esses parâmetros. A afirmação de ausência de execução se refere à baseline de 12/09; consultas na VPS e implantação posteriores têm evidências próprias.

## Incorporação RouterOS v7 — baseline 0.1.2

Leitura dos dois anexos e revisão estática concluídas. A conferência da versão final detectou API TCP 58728 habilitada no arquivo de Downloads; a revisão e o arquivo arquivado refletem essa versão. Os dois arquivos arquivados foram comparados byte a byte com os recebidos, e seus hashes SHA-256 foram conferidos.

Verificados 50 arquivos Markdown, 147 links locais, UTF-8, títulos e fechamento de blocos de código, sem erros. Requisitos REQ-23/24 associados a DOC-03, ROS-01 e WAN-01 a WAN-07 na homologação. O IPAM existente foi preservado e as diferenças do template foram explicitadas. A exceção de versionamento aplica-se apenas ao template recebido; exports reais permanecem excluídos.

Nenhum import/dry-run RouterOS ou teste de failover foi executado. O template exige adaptação antes da validação em laboratório.

## Atualização documental — 16/09/2026

Revisados estado atual, roadmap, inventário, DNS, stack, monitoramento, segurança, operação, requisitos, decisões, memória e homologação para concluir a etapa VPS/stack e coleta interna. Ver [registro de conclusão](VPS_PHASE_COMPLETION.md). Links locais e `git diff --check` verificados antes do commit. Resultados de runtime têm escopo próprio no registro; a revisão documental não aprova VPN, restauração ou campo.

## Consolidação documental — hub e notebook, 16/09/2026

Revisados os documentos Markdown do projeto, índices, memória e padrões locais para reconciliar o estado da implantação. Corrigidos registros superados de ausência de peers, SSH pendente, dependência de instalação da VPS e restrição pública presumida. Histórico inicial da VPS e preparação do hub preservados como histórico. Referências RouterOS originais preservadas sem alteração.

Criado o [registro de validação do notebook](NOTEBOOK_VPN_VALIDATION.md), distinguindo observação no servidor, confirmação do usuário e testes não executados. VPN-01/02 parciais; VPN-03, segurança, reboot/restauração e campo continuam pendentes. Acesso à RB951G indisponível, reafirmado pelo usuário. Revisão documental não executa mudanças operacionais.

Antes da publicação: conferir UTF-8, títulos, blocos de código, links locais, IPAM, rastreabilidade dos testes, ausência de segredos no diff e whitespace. Resultado quantitativo da verificação registrado após execução abaixo. Publicação confirmada por comparação de SHA local/remoto no relatório de entrega, sem embutir SHA autorreferente neste arquivo.

Resultado da verificação local desta consolidação: 55 arquivos Markdown em UTF-8, títulos e fechamento de blocos conferidos; 219 links locais resolvidos; 20 linhas de trânsito /30/VLAN/LAN verificadas por cálculo; 30 IDs de testes referenciados pelos requisitos encontrados na matriz. Nenhum erro estrutural ou de whitespace; busca por padrões de chaves privadas, PSKs, tokens GitHub e chaves WireGuard nas adições sem ocorrências. Links externos não foram revalidados nesta revisão de estado.


## Revisão minuciosa após retenção S3 — 16/09/2026

Revisados README, contexto, memória, roadmap, riscos, requisitos, decisões, inventário, especificação da stack, bootstrap, retenção de métricas, operação/backup, runbooks, segurança e homologação. Resumos atuais foram atualizados sem apagar os resultados históricos da instalação e auditoria inicial.

Separados três níveis de evidência: usuário informou configuração de expiração da versão atual em sete dias; HeadObject mostrou expiração no backup e recibo; exclusão efetiva e configuração completa do lifecycle não foram verificadas. GetBucketLifecycleConfiguration foi negado e nenhuma permissão ou política foi alterada nesta revisão. Evidência privada retention-audit.json; [registro canônico](BACKUP_AUTOMATION.md).

Retenção local 7/4/3 e S3 de sete dias estão documentadas como janelas diferentes; histórico/trends de métricas não foram alterados. Cópia externa da chave é confirmação do usuário; não equivale a teste dessa cópia. Recuperação integral, RPO/RTO e segurança não foram marcados como homologados.

Preparado o [plano de acesso da VPS](../04-security/VPS_ACCESS_PLAN.md), com inventário somente leitura, testes de painéis pela VPN, matriz de acesso, retorno e critérios SEC-03/04. Não houve implantação desse plano. Referências técnicas consultadas: documentação oficial AWS S3, Docker e Traefik.

Verificação desta revisão: UTF-8, fechamento de blocos, títulos, caminhos/âncoras locais, referências de requisitos/testes e diff Git. Resultados quantitativos ficam no registro privado da revisão. Arquivos operacionais, credenciais e cópias criptografadas permanecem fora do repositório; commit/publicação novos não são presumidos.


## Consolidação do estado de implementações — 17/09/2026

A revisão encontrou resultados corretos nos registros de execução, mas resumos contraditórios ainda tratavam reboot, restrições e alertas como pendentes. Foram corrigidos memória, roadmap, requisitos, riscos, homologação, segurança, DNS, WireGuard, inventário e procedimentos; removida a acumulação de atualizações intermediárias dos resumos atuais. Registros de instalação/auditoria iniciais ficaram explicitamente históricos.

Criado o [estado consolidado](../00-project/IMPLEMENTATION_STATUS.md), com cada entrega ligada à evidência, limites e próximo passo. Reboot, nove portas TCP IPv4, sete domínios, logins VPN, backup S3 e alertas SES/Telegram estão concluídos no escopo registrado. Recuperação integral, chave externa, UDP/IPv6 externo e equipamentos de campo permanecem pendentes. Esta revisão não executou novos testes operacionais. A publicação do conjunto foi autorizada posteriormente pelo usuário e é rastreada no histórico Git.

Validação final desta consolidação: 63 documentos Markdown, 309 links locais, uma âncora local e 30 identificadores de testes rastreados, sem erros; git diff --check aprovado. Registro privado documentation-implementation-review.json. Os totais de revisões anteriores permanecem históricos.

## Inventário atual da central NOC — 21/09/2026

Treze anexos lidos integralmente; síntese sanitizada de hardware, configuração e testes. Identificação RB750r2 r3, recursos, interfaces e serviços conferidos entre as saídas e o export. Documentação ativa apresenta o equipamento atual; anexos literais e registros de releases permanecem fontes históricas, não inventário.

Após integrar os registros remotos de VPS/operação, verificados 63 arquivos Markdown e 319 links locais, UTF-8 e blocos de código. Nenhum serial, software-id ou MAC da coleta nos documentos. Rede administrativa futura separada da LAN em uso; testes ICMP recebidos e validação DNS pendente distinguidos. Sem alterações no gateway; sem import, testes adicionais de rede ou publicação de export real.

## Mudança para 4G individual — 29/09/2026

Revisão solicitada pelo usuário: retirada da distribuição de Internet pela costa e adoção de modem/SIM próprios por barco. Atualizados contexto, requisitos, ADR-022/023, arquitetura, IPAM, hardware/energia, VPN, provisionamento, telemetria, segurança, backup, operação, modelo comercial, PoC, homologação, índices e memória. Criado procedimento de conectividade celular e gestão de linhas. Mantidos os registros históricos e resultados operacionais no escopo original.

Verificação local executada: 66 arquivos Markdown decodificados em UTF-8, títulos e fechamento de blocos conferidos; 341 links locais e uma âncora resolvidos; 20 pares de peer/LAN verificados por fórmula, gateway e ausência de sobreposição; 30 requisitos únicos e 39 IDs de testes referenciados encontrados na matriz. RF-01 a RF-05 conferidos como substituídos/não executados; CEL-01 a CEL-07, SIM-01 e DATA-01 permanecem não executados. `git diff --check` sem erros. Busca de padrões de chaves privadas, tokens GitHub e chaves AWS nas adições sem ocorrências; isso não substitui revisão humana de conteúdo.

Consulta externa limitada aos manuais oficiais de WireGuard e LTE/RouterOS para fundamentar a proposta; nenhuma cotação, plano, cobertura ou capacidade de gestão da Vivo foi validada. Sem testes operacionais, alteração de infraestrutura, contratação ou envio de notificações. Commit/push não executados nesta revisão; publicação não presumida.

## Pesquisa IoT e comando de bomba — 29/09/2026

Pesquisa externa em fabricantes e anúncios de preço para bateria, fumaça, corrente/nível da bomba e gateways. Documentados preços e condições de consulta, interfaces, consumo e precisão declarados, limites ambientais e integração proposta com o NOC. Incorporadas as confirmações do usuário: geralmente 12 V, bateria veicular/estacionária, bombas variadas e desejo de acionamento remoto quando possível. Atualizados requisitos, ADR-024, arquitetura, painéis, segurança, procedimentos, custos, PoC, riscos, memória e changelog.

Verificação executada: 67 documentos Markdown em UTF-8, títulos e blocos conferidos, 360 links locais e uma âncora resolvidos; 20 mapeamentos peer/LAN consistentes; 34 requisitos únicos e 44 IDs de testes referenciados encontrados na homologação. IOT-01 a IOT-05 conferidos como não executados. `git diff --check` sem erros. Busca por padrões de chaves privadas, tokens GitHub/AWS e chaves atribuídas nas adições e nos dois novos documentos sem ocorrências. Não equivale a ensaio de hardware, certificação marítima, implantação, compra ou publicação Git.

## Protótipo econômico — 29/09/2026

Registrado inventário confirmado: UNO, MEGA e Raspberry Pi 4B, sem sensores. Proposta MEGA/Pi 4B e comparação INA226/INA228 com SmartShunt documentadas, incluindo energia, referência de preço, calibração e sequência de aquisição/bancada. Atualizados ADR-025, requisitos, homologação, procedimento, custos, riscos, estado, índices e memória.

Validação local: 68 Markdown em UTF-8, 371 links locais e uma âncora resolvidos, 20 mapeamentos peer/LAN, 34 requisitos únicos e 44 IDs de testes rastreados; títulos e fechamento de blocos sem erros. `git diff --check` aprovado. Nenhum firmware compilado/carregado, teste de placa/campo, compra ou implantação efetuado.

## Inventário LM2596 e GSM — 29/09/2026

Incluídos conversor ajustável com display e módulo GSM/GPRS possivelmente SIM800L. Fontes TI, Raspberry Pi e manual SIMCom consultadas; capacidade real da placa e identidade do modem seguem pendentes. Revisados protótipo, energia, ADR-025, requisitos, procedimento, homologação, estado, memória e changelog. Verificação: 68 Markdown, 372 links locais, uma âncora, 20 mapeamentos peer/LAN, 34 requisitos e 44 IDs de testes, sem erros; `git diff --check` aprovado. Sem ensaio elétrico, envio de mensagem ou alteração de infraestrutura.
