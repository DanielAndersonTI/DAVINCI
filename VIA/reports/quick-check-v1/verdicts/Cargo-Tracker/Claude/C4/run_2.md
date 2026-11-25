# Laudo VIA — Cargo-Tracker

**Modelo:** Claude  
**Configuracao:** C4  
**Rodada:** 2  
**Execucao:** `20260923_203205_073469`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 71 |
| Servicos | 7 |
| Arestas | 10 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1429 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2198 | calculado |
| endpoints_por_responsabilidade | 0.1346 | calculado |
| estabilidade_jaccard_servicos | 0.4444 | calculado |
| estabilidade_jaccard_arestas | 0.1208 | calculado |
| taxa_defeitos_por_servico | 1.2857 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Cargo Tracking Service, Logistics Event Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Cargo Tracking Service, Logistics Event Service | Cargo Tracking Service -> Logistics Event Service; Logistics Event Service -> Cargo Tracking Service |
| D11-001 | D11 | media | Cargo Management Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-002 | D11 | media | Cargo Tracking Service | 1 endpoint(s) para 10 responsabilidade(s) |
| D11-003 | D11 | media | Integration Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-004 | D11 | media | Location Registry Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-005 | D11 | media | Logistics Event Service | 1 endpoint(s) para 11 responsabilidade(s) |
| D11-006 | D11 | media | Route Planning Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-007 | D11 | media | Voyage Registry Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
