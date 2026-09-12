# Modelos de evidência

Os campos abaixo são formulários vazios para uso futuro, não dados de demonstração. Copiar a seção necessária para registro privado e publicar somente a síntese sanitizada.

## Sessão técnica

| Campo | Preencher com |
|---|---|
| ID sessão | Identificador único |
| Testes/requisitos | IDs da matriz |
| Início/fim | ISO-8601 UTC e referência de timezone local |
| Responsável | Identidade autorizada no registro privado |
| Equipamentos | IDs, modelos e versões reais |
| Configuração | Commit do template e hash da configuração protegida |
| Ambiente | Local, distância, altura, orientação, condições e carga |
| Instrumentos | Origem, versão e precisão/resolução |
| Esperado | Critério documentado antes de medir |
| Observado | Dados reais, lacunas e erros |
| Resultado | Aprovado/reprovado/não executado |
| Artefatos | Identificador privado, tamanho, SHA-256 |
| Aceite | Autor/data ou pendente |

## Registro RF por intervalo

Campos: session_id, timestamp_utc, boat_id, distance_m, orientation_deg, collector_id, metric_source, rssi_dbm, tx_phy_rate, rx_phy_rate, ping_sent, ping_received, rtt_p95_ms, useful_throughput_bps, reconnect_count, voltage_v, sample_state, note.

Campo ausente fica vazio com `sample_state` e motivo. Manter amostras brutas e agregação identificadas separadamente. Não publicar localização/MAC ou descrição de proprietário no arquivo público.

## Registro de mudança

Campos: change_id, motivo, escopo autorizado, alvo, antes, plano, backup_ref, recovery_path, início, alteração aplicada, pós-testes, resultado, rollback_executado, estado_final, responsável, evidence_ref.

## Relatório de PoC

1. Objetivo e configuração exata.
2. Condições e limitações da sessão.
3. Resultado por teste, distância e orientação.
4. Pior caso e média, com cobertura da medição.
5. Perda, latência, vazão e eventos correlacionados.
6. Consumo/autonomia medidos e condições de carga.
7. Falhas, causa comprovada ou hipóteses ainda abertas.
8. Decisão e próximos ajustes com teste de repetição.
9. Referências privadas e hash dos dados brutos.

## Checklist de revisão documental

- [ ] Cada documento tem finalidade e estado.
- [ ] Fatos do usuário e propostas estão distintos.
- [ ] Links relativos resolvem.
- [ ] IPs, VLANs e rotas são consistentes.
- [ ] Fonte e data dos dados de fabricante estão registradas.
- [ ] Nenhum segredo ou dado pessoal desnecessário foi incluído.
- [ ] Nenhum teste de campo está marcado sem execução.
- [ ] Commit e publicação foram verificados pelo Git.
