# Validação da VPN de borda e alcance reverso da LAN NOC

Data: 22/09/2026  
Escopo: VPS WireGuard `10.250.0.1`, RB750r2 `10.250.0.2`, LAN NOC `192.168.15.0/24` e NVR `192.168.15.110`.

## Objetivo

Validar os dois sentidos relevantes da VPN de borda:

1. cliente da LAN NOC → serviços da VPS;
2. VPS → equipamento da LAN NOC.

O primeiro sentido já havia sido aprovado com ping, SSH e acesso ao Portainer. O segundo foi testado posteriormente usando o NVR `192.168.15.110`, previamente confirmado como acessível dentro da LAN.

## Falha observada

O primeiro teste da VPS para `192.168.15.110` apresentou 100% de perda. A consulta de rota mostrou que o destino estava sendo encaminhado pelo gateway público da interface `eth0`, e não por `wg0`:

```text
192.168.15.110 via <gateway-publico> dev eth0 src <ip-publico>
```

O peer WireGuard do MikroTik já continha:

```ini
AllowedIPs = 10.250.0.2/32, 192.168.15.0/24
```

Porém, essa alteração havia sido aplicada ao peer em execução com `wg set`. Esse comando atualiza a seleção criptográfica de peer, mas não instala automaticamente a rota Linux correspondente. A rota só é criada automaticamente quando `wg-quick` processa o arquivo de configuração, ou deve ser adicionada separadamente durante uma alteração em execução.

## Correção e persistência

A rota foi adicionada inicialmente em tempo de execução para validar a hipótese:

```bash
ip route add 192.168.15.0/24 dev wg0
```

Depois da confirmação, a persistência ficou baseada no comportamento nativo do `wg-quick`: o prefixo `192.168.15.0/24` permanece em `AllowedIPs` no arquivo `/etc/wireguard/wg0.conf`, e o serviço `wg-quick@wg0` está habilitado. Não há `PostUp`/`PreDown` redundante para essa rota.

Estado final observado após recuperação e reinicialização:

```text
wg-quick@wg0: enabled e active
192.168.15.0/24 dev wg0 scope link
192.168.15.110 dev wg0 src 10.250.0.1
```

## Resultado medido

Teste executado na VPS:

```bash
ping -c 3 192.168.15.110
```

Resultado:

```text
3 packets transmitted, 3 received, 0% packet loss
rtt min/avg/max/mdev = 23.804/25.262/26.162/1.040 ms
```

O resultado comprova alcance ICMP da VPS ao NVR pelo túnel e pela RB750r2. Não comprova, isoladamente, disponibilidade das portas ou autenticação do NVR.

## Intercorrência de recuperação

Durante a tentativa inicial de tornar a rota persistente, a interface `wg0` foi derrubada para reinício enquanto a sessão administrativa usava o próprio túnel. A sessão SSH foi perdida, e novas conexões pelo IP público permaneceram bloqueadas conforme a política de segurança. O acesso foi recuperado pelo console do provedor e a VPN voltou após correção/subida do serviço.

Essa ocorrência não justifica liberar SSH público permanentemente. O console do provedor permanece o caminho de recuperação fora de banda.

## Procedimento seguro para mudanças futuras

Antes de reiniciar `wg0`:

1. confirmar acesso ao console do provedor;
2. manter uma sessão de console disponível durante a mudança;
3. salvar backup protegido de `/etc/wireguard/wg0.conf`;
4. validar a configuração sem publicar chaves privadas;
5. lembrar que `wg set` não gerencia rotas Linux;
6. evitar rotas `PostUp` que dupliquem prefixos já instalados pelo `wg-quick` a partir de `AllowedIPs`;
7. após a mudança, conferir serviço, handshake, rota e aplicação.

Verificações sanitizadas:

```bash
systemctl is-enabled wg-quick@wg0
systemctl is-active wg-quick@wg0
wg show wg0
ip route show dev wg0
ip route get 192.168.15.110
ping -c 3 192.168.15.110
```

Nunca copiar a linha `PrivateKey` para evidências, tickets ou repositório.

## Estado de aceite

| Critério | Resultado |
|---|---|
| RB750r2 ↔ VPS com handshake recente | Aprovado |
| LAN NOC → VPS por ping/SSH | Aprovado |
| LAN NOC → Portainer via Traefik | Aprovado pelo usuário |
| VPS → NVR `192.168.15.110` por ICMP | Aprovado, 3/3 respostas |
| Rota para `192.168.15.0/24` após reinicialização | Aprovado |
| Recuperação sem acesso público | Aprovada via console do provedor |
| SSH público TCP 5822 | Permanece bloqueado |

A validação é parcial para a LAN: somente o NVR citado foi testado no sentido VPS → LAN. Outros equipamentos, protocolos e regras de acesso exigem testes próprios.
