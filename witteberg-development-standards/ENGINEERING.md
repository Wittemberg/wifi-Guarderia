# Engenharia, persistência e segurança

Síntese adaptada de `engineering/*`, `patterns/LOCAL-AGENTS.md` e `patterns/ERROR-HANDLING.md` do snapshot de referência indicado no [README](README.md).

## Persistência

Configurações, identidades, chaves, políticas e estados relevantes precisam sobreviver a reboot/redeploy. Cache e memória de processo não são fonte única. Volumes e backup devem ser testados com restauração. Um agente/coletor permanente não deve depender de navegador, terminal aberto ou login diário.

Falhas transitórias de rede devem gerar reconexão com backoff limitado e jitter, não perda de identidade. Falha de configuração/credencial deve aparecer distintamente, evitando retry agressivo que cause bloqueio ou carga.

## Segurança

Sem segredo em código, log, URL ou cliente web. Separar administração, leitura e automação. Autorização por identidade e recurso é aplicada no serviço, não somente na UI. TLS precisa validar o destino. Banco e gerência não ficam públicos por conveniência.

## Não regressão

Antes de alterar componente compartilhado, localizar consumidores e testar os caminhos afetados. Configuração de rede já homologada é baseline: mudança exige motivo, comparação e possibilidade de retorno. Não modernizar stack ou refazer tela incidentalmente.

## Evidência

Teste automatizado não substitui campo quando há rádio, energia ou hardware. Divergência entre ensaio de bancada e ambiente real precisa de investigação. Relatório deve separar componente alterado, efeito, teste e restrição.

## Erros

Não falhar silenciosamente. Diferenciar erro da aplicação, coletor, rede, credencial, equipamento e configuração. Mensagem explica fato observado e próximo responsável, sem stacktrace/segredo exposto. Dado não disponível é um estado controlado.
