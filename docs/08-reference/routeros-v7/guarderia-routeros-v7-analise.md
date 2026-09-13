# Análise do script e proposta RouterOS v7

## arquitetura

- WAN1 primária, WAN2 backup.
- Duas sondas públicas independentes por WAN.
- Rotas /32 prendem cada sonda ao gateway correto.
- Rotas default recursivas têm `check-gateway=ping`.
- Nenhum script coloca a default como `disabled=yes`.
- Se os dois links caírem, as defaults ficam *inactive*, não *disabled*.
- As rotas de sonda permanecem configuradas.
- Quando um link volta, o RouterOS detecta e reativa a default automaticamente.
- WireGuard passa a ser o túnel de gerenciamento com a VPS pública; o MikroTik inicia a sessão, portanto CGNAT no local não impede o túnel.
- alertas devem ser centralizados na VPS.

## Observação importante

O template entregue assume WANs com IP e gateway estáticos no lado privado dos modems/roteadores.
Se a WAN receber endereço por DHCP diretamente, a camada de failover precisa de uma variante própria
para atualizar os next-hops de sonda conforme o lease. Não convém misturar os dois modelos.

## Testes obrigatórios

1. Com WAN1 e WAN2 ativos, confirmar default ativa pela WAN1.
2. Desconectar fisicamente WAN1; confirmar mudança para WAN2.
3. Reconectar WAN1; confirmar retorno automático à WAN1.
4. Desconectar WAN1 e WAN2; confirmar que as defaults ficam inactive e não disabled.
5. Reconectar somente WAN2; confirmar recuperação automática sem intervenção.
6. Repetir reconectando somente WAN1.
7. Com WireGuard ativo, repetir failover e observar novo handshake via link remanescente.
