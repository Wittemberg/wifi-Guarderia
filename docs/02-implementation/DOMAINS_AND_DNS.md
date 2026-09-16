# Domínios e DNS

Registro: 15/09/2026. Domínio principal `awecloudsolution.com` e uso de CNAME informados pelo usuário. Publicação confirmada pelo usuário e resolução conferida diretamente na VPS com `dig`: o A e os cinco CNAMEs abaixo responderam conforme a tabela, com TTL observado de 300 s. Este é o registro inicial de DNS; resultados posteriores de HTTPS e instalação constam na atualização de 16/09 ao final deste documento. Acesso pela VPN ainda não validado.

## Registros publicados e resolução observada

Os nomes da coluna Nome são relativos à zona `awecloudsolution.com`.

| Tipo | Nome | Destino | Finalidade |
|---|---|---|---|
| A | `vps-guarderia` | `204.157.108.99` | Destino central dos aliases |
| CNAME | `zabbix-guarderia` | `vps-guarderia.awecloudsolution.com` | Console Zabbix |
| CNAME | `grafana-guarderia` | `vps-guarderia.awecloudsolution.com` | Dashboards |
| CNAME | `status-guarderia` | `vps-guarderia.awecloudsolution.com` | Uptime Kuma |
| CNAME | `portainer-guarderia` | `vps-guarderia.awecloudsolution.com` | Administração de containers |
| CNAME | `vpn-guarderia` | `vps-guarderia.awecloudsolution.com` | Endpoint WireGuard |

`guarderia.awecloudsolution.com` fica reservado como ideia para página futura, sem serviço ou registro exigido nesta fase. Não criar registro público para PostgreSQL. Provedor DNS não registrado; TTL observado nas respostas: 300 s.

## Acesso e implantação

- Endpoint proposto: `vpn-guarderia.awecloudsolution.com:51820`, UDP. A resolução deve funcionar antes do túnel; o caminho DNS deve permitir alcançar diretamente o endpoint UDP.
- Interfaces web usam HTTPS e encaminhamento por hostname no proxy TLS; CNAME não contém porta, protocolo ou caminho.
- Zabbix, Grafana e Portainer permanecem restritos à administração pela VPN. DNS público não substitui firewall nem autoriza exposição pública.
- Uptime Kuma começa com acesso administrativo restrito. Publicação de página de status exige definição de conteúdo e acesso; não implica publicar sua administração.
- Todos os aliases propostos resolvem para o IP público. A implementação deve validar acesso dos administradores pela VPN a esse destino ou adotar resolução interna para o proxy privado e documentar a alteração.
- Certificados precisam cobrir cada hostname web. Método de emissão/renovação pendente; não abrir administração apenas para emitir certificados.

## Validação futura

1. Conferir no provedor o registro A e cada CNAME, sem conflitos no mesmo nome.
2. Consultar a resolução externa e pela VPN; comparar o destino com o inventário privado.
3. Testar WireGuard, rotas e coleta conforme VPN-01/02/03.
4. Validar hostname, cadeia e renovação dos certificados, login e encaminhamento de cada serviço.
5. Comprovar acesso administrativo autorizado e bloqueio externo, incluindo após reinício do Docker (SEC-03/04 e OPS-01).

A resolução pelo resolvedor da VPS foi conferida com `dig +noall +answer <hostname> A` para os seis nomes da tabela. Todas as respostas apresentaram o IP esperado e os cinco aliases apresentaram CNAME para vps-guarderia. Isso não comprova propagação em todos os resolvedores, acesso pela VPN, TLS ou funcionamento dos serviços; essas verificações permanecem pendentes. Referências: [stack](STACK_SPEC.md), [VPS](../01-architecture/VPS_INVENTORY.md) e [segurança](../04-security/SECURITY.md).

## Novos nomes após instalação Orion — 16/09/2026

| Nome completo | Serviço |
|---|---|
| `node-guarderia.awecloudsolution.com` | Node Exporter |
| `cadvisor-guarderia.awecloudsolution.com` | cAdvisor |
| `prometheus-guarderia.awecloudsolution.com` | Prometheus |

Usuário informou acesso pelo navegador. Consultas na VPS apresentaram DNS/TLS inconsistentes durante a propagação; conclusão uniforme pelos resolvedores da VPS ainda pendente. HTTPS de Zabbix, Grafana, Kuma e Portainer foi validado nesta sessão. A coleta dos três novos serviços foi concluída via DNS interno tasks.monitor_*; não depende dos domínios públicos. Ver [fechamento](../06-validation/VPS_PHASE_COMPLETION.md).
