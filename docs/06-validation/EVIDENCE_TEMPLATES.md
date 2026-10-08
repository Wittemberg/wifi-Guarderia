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

## Registro celular por intervalo — revisão de 29/09/2026

Campos: session_id, timestamp_utc, boat_id, asset_id, line_id_logico, plan_ref, position_ref_privada, orientation_deg, collector_id, metric_source, radio_technology, registration_state, data_session_state, rsrp_dbm, rsrq_db, sinr_db, wan_rx_bytes, wan_tx_bytes, counter_reset, probe_path, ping_sent, ping_received, rtt_p95_ms, useful_upload_bps, useful_download_bps, reconnect_count, vpn_handshake_age_s, voltage_v, sample_state, note.

Campo ausente fica vazio com estado/motivo. Não publicar ICCID/IMSI/IMEI, célula/localização, número de linha ou titular. RSRP/RSRQ/SINR apenas quando suportados e conferidos. Separar sondas LAN, Internet 4G e VPN; manter amostras brutas e agregações identificadas.

## Registro de consumo e gestão individual

Campos: boat_id, line_id_logico, contract_ref_privada, source, observed_at, source_updated_at, cycle_start, cycle_end, unit, used_data, quota, pool_ref_se_aplicavel, local_counter_baseline, reset_events, discrepancy, estimated_monthly_data, estimation_method, alert_threshold, action_authorization_ref, action_scope, requested_at, effective_at, effect_on_other_line, result, evidence_ref.

Franquia/velocidade desconhecidas ficam pendentes; ausência de API não impede registro manual com fonte/data. Ação sobre linha de teste exige autorização e recuperação local. Extrapolação mensal é hipótese, não fatura medida.

## Registro de mudança

Campos: change_id, motivo, escopo autorizado, alvo, antes, plano, backup_ref, recovery_path, início, alteração aplicada, pós-testes, resultado, rollback_executado, estado_final, responsável, evidence_ref.

## Relatório de PoC

1. Objetivo e configuração exata.
2. Condições e limitações da sessão.
3. Resultado por teste, posição real, horário, orientação e plano/operadora.
4. Pior caso e média, com cobertura da medição.
5. Perda, latência, vazão e eventos correlacionados.
6. Consumo de dados por linha/ciclo, energia/autonomia e condições de carga.
7. Falhas, causa comprovada ou hipóteses ainda abertas.
8. Decisão e próximos ajustes com teste de repetição.
9. Referências privadas e hash dos dados brutos.

## Checklist de revisão documental

- [ ] Cada documento tem finalidade e estado.
- [ ] Fatos do usuário e propostas estão distintos.
- [ ] Links relativos resolvem.
- [ ] IPs, peers, LANs e rotas são consistentes.
- [ ] Fonte e data dos dados de fabricante estão registradas.
- [ ] Nenhum segredo ou dado pessoal desnecessário foi incluído.
- [ ] Nenhum teste de campo está marcado sem execução.
- [ ] Commit e publicação foram verificados pelo Git.
