# Segurança, acesso e proteção dos dados

Estado: requisitos para implementação e teste. A primeira entrega não altera firewall nem cria usuários em sistemas remotos.

## Princípios

Menor privilégio, autenticação individual, isolamento de barcos, segredos fora do Git, TLS validado e mudanças rastreáveis. WireGuard restringe transporte; não concede acesso irrestrito ao que está atrás do peer.

## Matriz de fluxos permitidos

| Origem | Destino | Serviço | Regra |
|---|---|---|---|
| Internet | VPS | UDP 51820 | VPN pública autenticada |
| Administração autorizada | VPS | SSH/HTTPS | Preferir VPN; bootstrap com restrição temporária documentada |
| Coletor autorizado | Equipamentos cadastrados | ICMP, UDP 161 SNMPv3, HTTPS/API TLS conforme necessidade | Somente pela VPN e alvos ativos |
| PC administrativo 10.21.0.10 / peer de recuperação | Gestão core/AP/wAP | SSH/WinBox/HTTPS estritamente necessários | Fonte, destino e serviço explícitos |
| Zabbix web/server | PostgreSQL | TCP 5432 | Rede interna de dados |
| Grafana | Zabbix API | HTTPS ou backend privado protegido | Token somente leitura |
| LAN barco N | Internet | Serviços contratados | NAT somente WAN core |
| LAN barco N | wAP N | DHCP/DNS/NTP se oferecidos | Serviços locais, sem administração |
| LAN barco N | LAN barco M/gestão/trânsitos/VPN | Qualquer | Negar |
| Trânsito barco N | Trânsito M | Qualquer | Negar |
| Internet | WinBox, SNMP, banco, Portainer, câmeras | Qualquer | Negar |

Responder a conexões estabelecidas/relacionadas conforme contexto; descartar inválidas. O recebimento de syslog e trap só será aberto se adotado e limitado à origem cadastrada. Não confundir TCP 8728 sem TLS com API-SSL 8729 ou REST HTTPS.

## Controle de origem

Rejeitar endereço de origem incompatível com VLAN de entrada no core. Não aceitar LAN de outro barco apresentada por uma estação. Rejeitar VLANs não cadastradas no trunk; verificar isolamento no rádio e ausência de forwarding direto entre estações. Rotas específicas não bastam para isso.

IPv6 precisa de decisão explícita: ou implementação com política equivalente e teste ou bloqueio de encaminhamento entre segmentos e ausência de anúncios acidentais. Considerar também gerência MAC, descoberta, bridge e interfaces não usadas.

## Credenciais e papéis

| Papel | Permissão |
|---|---|
| Administrador | Configuração, usuários, backups e mudanças autorizadas |
| Operador | Consulta, incidentes e manutenção de alertas dentro de escopo |
| Coletor | Leitura necessária à telemetria, sem alteração de configuração |
| Proprietário do barco | Somente serviço/dados do próprio barco, se habilitado |
| Integração NOC-Agent futura | Leitura limitada por identidade e escopo |

MFA onde suportado, revogação individual e conta de emergência protegida. Permissões por barco não podem depender apenas de filtros visuais de dashboard. Portal do cliente é evolução: não compartilhar painel administrativo como substituto de isolamento.

## Segredos e TLS

Chaves WireGuard permanecem na ponta e no backup cifrado restrito. Credenciais de banco/monitoramento em secrets ou arquivo protegido, com cópia de recuperação fora da VPS. Não registrar tokens em logs, URLs, query strings ou commits.

Certificados privados exigem CA confiável instalada no coletor; certificados públicos exigem hostname compatível. Não usar `rejectUnauthorized=false`, `verify=false` ou opções equivalentes como solução permanente. Tratar erro de autenticação/certificado como erro específico, nunca degradar para conexão insegura silenciosamente.

## Classificação e retenção

| Classe | Exemplos | Local |
|---|---|---|
| Pública/sanitizada | Especificação, template sem dados reais | Git |
| Operacional restrita | MAC, serial, IP real, croqui detalhado, fotos de instalação | Storage privado |
| Segredo | Senhas, chaves, tokens, dumps com credenciais | Cofre/backup cifrado |
| Dados de pessoas/imagens | Contatos, vídeo e identificação de proprietário | Sistema autorizado, acesso por finalidade |

Definir finalidade, responsáveis, acesso e retenção dos dados antes de produção. Não copiar filmagens para a VPS/Git para diagnóstico comum. Exigências contratuais, privacidade e enquadramento regulatório devem ser analisadas na etapa comercial; este documento não conclui conformidade jurídica.

## Ameaças e validação

| Ameaça | Controle | Teste |
|---|---|---|
| Cliente tenta acessar outro barco | VLAN, ACL e autenticação individual | SEC-01 |
| Spoof de origem/MAC | Vínculo identidade/VLAN e anti-spoof | SEC-02 |
| Gerência publicada pelo Docker | Redes privadas, bind/regras e verificação externa | SEC-03 |
| Roubo de credencial | Menor privilégio e revogação | SEC-04 |
| Falha TLS/servidor falso | Verificação de certificado | SEC-04 |
| NOC comprometido | Coletor leitura, separação de papéis | SEC-04 |
| Texto malicioso em log/hostname | Tratar como dado, não instrução | INT-01 futuro |
| Perda da configuração | Backup e restauração ensaiados | BAK-01 |

Hash de evidência permite detectar alteração quando comparado com referência confiável; não torna o arquivo imutável por si só.

## Revisão da coleta atual da central NOC — 21/09/2026

A configuração IPv4 recebida bloqueia novas conexões administrativas pela lista WAN, mas permite toda a LAN no input; serviços não restringem origem no campo address. HTTP 780 e API 58728 estão habilitados sem TLS, SSH 5822 e WinBox 58292 ativos. Não há drop final explícito nas cadeias input/forward nem política IPv6 demonstrada. Isso é análise estática, não teste externo de exposição. Antes da VPN, definir ACLs específicas e política para novas interfaces; revisar MAC/descoberta, contas e necessidade de cada serviço. Detalhes no [inventário](../01-architecture/NOC_ROUTER_INVENTORY.md).

A documentação pública mantém nomes lógicos, recursos e resultados agregados. Seriais, software-id, MACs, endereços operacionais privados e export completo permanecem fora do Git.
