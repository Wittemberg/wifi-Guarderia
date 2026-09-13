# Revisão do template RouterOS v7 recebido

Data: 12/09/2026. Estado: leitura integral dos dois anexos e análise estática concluídas; nenhum import, reset, alteração de equipamento ou teste RouterOS executado. Fontes originais e hashes: [anexos](../08-reference/routeros-v7/README.md).

## Conclusão

O desenho de WAN primária/backup com sondas recursivas é referência útil para a **RB951G da central NOC**, atualizada para 7.23.5. O arquivo recebido **não está pronto para importação** no projeto. A atualização de firmware já concluída não valida o template.

A incorporação adiciona uma proposta de redundância da central NOC, sem presumir contratação/disponibilidade de dois links. Não substitui o core RB750Gr3 nem altera o IPAM adotado. A segunda WAN da guarderia permanece uma evolução distinta.

## Arquitetura recebida

Ether1 é WAN1, ether2 é WAN2 e ether3–5 compõem uma LAN sem VLAN. O rádio legado é desabilitado. O template configura endereços estáticos nos segmentos privados dos modems, DHCP/DNS na LAN, quatro rotas de sondas /32, quatro defaults recursivas, NAT de saída, WireGuard para VPS, firewall IPv4, WinBox TCP 58292 e API TCP 58728 sem TLS, descoberta/MAC e NTP. SNMP é somente exemplo comentado.

As instruções do anexo de análise — inclusive os sete testes — foram convertidas em requisitos de validação futura; não foram executadas.

## Achados e tratamento

| ID | Prioridade | Evidência no `.rsc` original | Consequência e tratamento |
|---|---|---|---|
| REV-01 | P0 | Linhas 19–41: variáveis `CFG_*` sem aspas | Nomes com `_` exigem tratamento conforme sintaxe RouterOS; corrigir declaração e referências antes de validar import |
| REV-02 | P0 | Bloco de variáveis encerra antes dos usos externos | Globais declaradas dentro de escopo precisam ser declaradas no escopo consumidor; preferir um bloco único com variáveis locais alfanuméricas |
| REV-03 | P0 | Linha 13: comentário de reset com `skip-backup=yes` | Não é comando ativo no arquivo, mas é uma orientação inadequada para adoção automática; exigir backup, recuperação e mudança separada se reset for necessário |
| REV-04 | P0 | Placeholders de endpoint e chave no bloco inicial | Sem validação anterior às mutações, import pode parar após mudanças parciais; validar parâmetros e plano antes de alterar interfaces |
| REV-05 | P0 | IPs LAN/WG e identidade divergem da baseline | Adaptar conforme tabela abaixo; não substituir o IPAM pelo anexo |
| REV-06 | P0 | Linha 157: peer aceita somente IP de túnel da VPS | Não contempla redes remotas/identidades do projeto nem cria suas rotas; completar AllowedIPs e rotas de ida/retorno |
| REV-07 | P0 | Linha 171: input aceita tudo de MGMT; bridge LAN pertence a MGMT | Qualquer host dessa LAN recebe alcance aos serviços ativos do roteador; restringir origem e serviço, além da interface |
| REV-08 | P0 | Somente firewall IPv4; sem política IPv6, usuários ou privilégios | Não atende toda a matriz de segurança; definir política equivalente ou bloqueio de IPv6 e credenciais nominais |
| REV-09 | P1 | Linha 179: FastTrack genérico em forward | Pode contornar filas e parte da inspeção; excluir gerência/VPN/fluxos de ensaio ou desabilitar durante homologação |
| REV-10 | P0 | Linha 196: API habilitada em TCP 58728, API-SSL desligada; SNMP comentado | API sem TLS alcançável por toda MGMT no firewall recebido. Desabilitar se dispensável ou restringir a coletor autorizado via VPN, com conta de leitura e transporte protegido conforme política; porta alternativa não protege credenciais |
| REV-11 | P1 | WinBox 58292; MAC WinBox na LAN; descoberta em MGMT | Porta alternativa não autentica nem isola usuários; revisar fontes, MAC e descoberta conforme acesso físico |
| REV-12 | P1 | Linha 214: DDNS cloud habilitado | Não é requisito do WireGuard iniciado até VPS pública; manter desabilitado na adaptação salvo necessidade documentada |
| REV-13 | P1 | Repetidos `add`, sem detecção de estado anterior | Reimportação pode duplicar objetos ou falhar. Definir pré-condição de bancada limpa e estratégia de repetição/rollback |
| REV-14 | P1 | Log final informa baseline aplicada | Mensagem não valida rotas, VPN, isolamento ou recuperação; somente pós-testes e evidências liberam aceite |

### Sintaxe e importação

O manual exige aspas quando o nome da variável contém caracteres além de letras/dígitos e descreve a visibilidade de globais entre escopos. A leitura estática identifica esses problemas no template; não substitui o parser da RB951G. A adaptação proposta deve usar nomes como `cfgIdentity` em escopo único. Referência: [Scripting](https://help.mikrotik.com/docs/spaces/ROS/pages/47579229/Scripting).

Depois das correções, validar em laboratório com o modo verbose/dry-run suportado pela versão alvo. Esse teste pode encontrar erros de importação sem aplicar a configuração, mas não comprova funcionamento de failover ou VPN. Referência: [Configuration Management](https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management).

## Reconciliação com o projeto

| Item | Anexo original | Baseline a preservar/adaptar |
|---|---|---|
| Alvo | GUARDERIA-POC-RB951 | RB951G da central NOC; identidade proposta `GV-NOC-01` |
| LAN administrativa | 192.168.50.0/24 | 10.21.0.0/24; gateway .1 e PC administrativo .10 |
| Pool DHCP | 192.168.50.50–220 | A definir na LAN NOC; não incluir reservas administrativas |
| Túnel local | 10.200.0.2/24 | 10.250.0.2/24 |
| Túnel VPS | 10.200.0.1/32 | 10.250.0.1/32 |
| WAN1 | 192.168.15.253/24, gateway .1 | Exemplo não confirmado; inventariar modem/provedor |
| WAN2 | 192.168.68.253/24, gateway .1 | Exemplo não confirmado; inventariar modem/provedor |
| Porta VPS | UDP 51820 | Mantida na proposta |
| Porta local WireGuard | UDP 51821 | Candidata para RB951G; não muda o endpoint 51820 da VPS |
| Gerência WinBox | TCP 58292 | Candidata local, restrita às fontes autorizadas; não regra global de todos os equipamentos |
| Segunda porta Ethernet | WAN2 | Somente na RB951G; ether2 do core continua trunk |

As diferenças exigem alterar também ACLs, DHCP, rotas, AllowedIPs e documentação de portas. Trocar somente os endereços no bloco inicial não resolve todo o escopo.

## Interpretação do failover

As duas defaults de cada WAN têm distância igual e podem participar de ECMP. Como os dois alvos se resolvem pelo mesmo gateway físico, isso não é balanceamento WAN1/WAN2. Uma WAN continua elegível enquanto pelo menos uma de suas sondas responde; somente a perda de ambas remove todos os candidatos daquela WAN. A prioridade entre WANs é distance 1 versus 2. Esse padrão corresponde ao exemplo oficial de [failover recursivo](https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup).

Na falha total, as rotas permanecem configuradas; sua elegibilidade depende de next-hop e checagem, não de um script que aplique `disabled=yes`. Ausência de dois alvos ICMP não prova falha de todos os serviços, e resposta ICMP não prova DNS/HTTPS/VPS saudáveis. Targets de provedores diferentes reduzem dependência de um alvo, mas não tornam os enlaces fisicamente independentes.

## Conexões e WireGuard

Trocar a rota preferida não garante preservar conexões TCP/UDP já estabelecidas. NAT, conntrack e mudança de caminho precisam de ensaio, inclusive com Ethernet ativa e perda de upstream. Não definir limpeza global de conntrack como reação automática. Referências: [NAT](https://help.mikrotik.com/docs/spaces/ROS/pages/3211299/NAT) e [connection tracking/FastTrack](https://help.mikrotik.com/docs/spaces/ROS/pages/130220087/Connection+tracking).

O peer limitado a um /32 da VPS não permite por si só a administração direta de outras redes. AllowedIPs e rotas são partes distintas da configuração. Testar origem preservada da central NOC até o core e o retorno. Referência: [WireGuard](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard).

## Estado da incorporação

Originais arquivados, achados registrados e testes adicionados. A [especificação dual-WAN](NOC_DUAL_WAN.md) orienta uma futura versão adaptada. Nenhuma correção silenciosa foi feita ao `.rsc` original, e nenhuma cópia executável é anunciada como pronta para produção.

## Conferência da versão recebida

Durante a revisão, o arquivo de Downloads foi atualizado: `api disabled=yes` passou a `api disabled=no port=58728`. A cópia arquivada e seu hash correspondem à versão final relida. A mudança foi incorporada ao REV-10; não é evidência de configuração no equipamento.
