# Laudo VIA — Cargo-Tracker

**Modelo:** Gemini  
**Configuracao:** C4  
**Rodada:** 2  
**Execucao:** `20260924_002115_352545`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 71 |
| Servicos | 5 |
| Arestas | 12 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.0333 | calculado |
| endpoints_por_responsabilidade | 0.2083 | calculado |
| estabilidade_jaccard_servicos | 0.8333 | calculado |
| estabilidade_jaccard_arestas | 0.1471 | calculado |
| taxa_defeitos_por_servico | 1.4000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Cargo Management Service, Cargo Tracking Service, Logistics Event Registration Service, Route Planning Service | componente fortemente conexa com 4 servicos |
| D04-002 | D04 | alta | Cargo Management Service, Cargo Tracking Service | Cargo Management Service -> Cargo Tracking Service; Cargo Tracking Service -> Cargo Management Service |
| D04-003 | D04 | alta | Cargo Management Service, Route Planning Service | Cargo Management Service -> Route Planning Service; Route Planning Service -> Cargo Management Service |
| D04-004 | D04 | alta | Cargo Tracking Service, Logistics Event Registration Service | Cargo Tracking Service -> Logistics Event Registration Service; Logistics Event Registration Service -> Cargo Tracking Service |
| D04-005 | D04 | alta | Cargo Tracking Service, Route Planning Service | Cargo Tracking Service -> Route Planning Service; Route Planning Service -> Cargo Tracking Service |
| D11-001 | D11 | media | Cargo Management Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-002 | D11 | media | Cargo Tracking Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | Integration Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-004 | D11 | media | Logistics Event Registration Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-005 | D11 | media | Route Planning Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
