# Laudo VIA — Cargo-Tracker

**Modelo:** Gemini  
**Configuracao:** C0  
**Rodada:** 1  
**Execucao:** `20260903_205027_893437`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 71 |
| Servicos | 5 |
| Arestas | 5 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1333 | calculado |
| endpoints_por_responsabilidade | 0.8333 | calculado |
| estabilidade_jaccard_servicos | 0.8333 | calculado |
| estabilidade_jaccard_arestas | 0.1250 | calculado |
| taxa_defeitos_por_servico | 1.2000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D05-001 | D05 | alta | Cargo Management Service, destination | nome nao resolvido: destination |
| D05-002 | D05 | alta | Cargo Tracking Service, last known location | nome nao resolvido: last known location |
| D05-003 | D05 | alta | Integration Service, integration service | nome nao resolvido: integration service |
| D05-004 | D05 | alta | Logistics Event Service, load | nome nao resolvido: load |
| D05-005 | D05 | alta | Route Planning Service, destination | nome nao resolvido: destination |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
