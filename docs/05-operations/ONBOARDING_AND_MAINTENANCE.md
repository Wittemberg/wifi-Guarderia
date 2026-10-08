# Entrada em operação e manutenção

## Onboarding por embarcação

1. Cadastrar ID lógico, responsável privado, termo de acesso e plano contratado. Associar modem e SIM próprios; registrar se fornecido pela operação ou pelo titular, permissões de gestão, APN e limites de consumo em inventário protegido.
2. Levantar casco, pontos de instalação, alimentação, cobertura e autonomia necessária.
3. Reservar LAN e peer WireGuard exclusivo no [IPAM](../01-architecture/NETWORK_PLAN.md); registrar origem manual e validação do inventário.
4. Montar kit em bancada com credenciais exclusivas; testar alarme e câmeras com/sem WAN.
5. Registrar firmware e configuração, medir consumo e produzir backup protegido.
6. Instalar, etiquetar e fotografar somente os detalhes técnicos necessários.
7. Executar testes de cobertura 4G, dados/franquia, VPN, isolamento, alimentação, aplicativo e retorno de energia.
8. Cadastrar monitoramento, alertas e contatos autorizados; testar notificação acordada.
9. Orientar proprietário sobre uso, falhas, alimentação e acionamento de suporte.
10. Registrar aceite e pendências. Qualquer item P0 reprovado impede liberação do serviço afetado.

## Inventário canônico mínimo

ID do ativo, site, barco, função, modelo, versão, MAC/serial privados, porta física, LAN/peer, linha lógica, operadora/plano/ciclo, titularidade, estado, data de instalação, garantia, referência de segredo, última verificação e responsável. Dados descobertos não sobrescrevem dados verificados silenciosamente. Mudança de IP não cria automaticamente novo equipamento.

## Rotina operacional

| Cadência | Verificação |
|---|---|
| Diária | Falhas ativas, idade de dados, backup, disco e notificações |
| Semanal | Flapping, sinal celular suportado, consumo por linha/ciclo, tendência de energia e pressão de capacidade |
| Mensal | Incidentes recorrentes, acessos, credenciais revogadas e custos e conciliação da fatura de cada linha |
| Após 30 dias piloto | Inspeção física e confronto de energia com autonomia prevista |
| Semestral proposta | Vedação, corrosão, terminais, bateria, sensores, sirenes, câmeras e fixação |
| Trimestral proposta | Restauração do NOC e acesso de recuperação |

Os intervalos são política inicial a ajustar pelas condições reais. Visita extraordinária deve registrar deslocamento, mão de obra, peças, falha identificada e vínculo com garantia/contrato.

## Relatório ao cliente

Informar período, disponibilidade observada com lacunas explícitas, incidentes, ações realizadas e pendências que exigem intervenção. “Sem dados” não conta automaticamente como disponibilidade nem como falha do equipamento; relatar cobertura da medição separadamente. Distinguir suporte técnico da vigilância patrimonial.

## Gestão de linhas e encerramento — revisão de 29/09/2026

Antes do aceite: validar banda/franquia/velocidade contratadas, alertas de consumo, controle individual disponível, contatos de suporte, prazo de reposição e recuperação local. Medir bytes do monitoramento/VPN e incluir no orçamento da linha. Telemetria de rede e portal da operadora têm fontes e atrasos distintos.

Na retirada, seguir RB-08/RB-15: revogar VPN e credenciais de aplicação, remover rotas/ACLs daquele barco, cancelar/devolver linha segundo titularidade e autorização, conferir fim da cobrança e proteger dados do kit. Cancelar linha não revoga automaticamente VPN ou contas de vídeo. Registrar baixa antes de reutilizar endereço/equipamento; nova instalação recebe credenciais próprias.
