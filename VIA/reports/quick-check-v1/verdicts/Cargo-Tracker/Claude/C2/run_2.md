# Laudo VIA — Cargo-Tracker

**Modelo:** Claude  
**Configuracao:** C2  
**Rodada:** 2  
**Execucao:** `20260917_000558_646198`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 71 |
| Servicos | 6 |
| Arestas | 17 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1667 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1173 | calculado |
| endpoints_por_responsabilidade | 0.1296 | calculado |
| estabilidade_jaccard_servicos | 0.5000 | calculado |
| estabilidade_jaccard_arestas | 0.4722 | calculado |
| taxa_defeitos_por_servico | 1.3333 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Cargo Management Service, Cargo Tracking Service, Event Processing Service, Integration Service, Logistics Network Service, Route Planning Service | componente fortemente conexa com 6 servicos |
| D04-002 | D04 | alta | Cargo Management Service, Logistics Network Service | Cargo Management Service -> Logistics Network Service; Logistics Network Service -> Cargo Management Service |
| D04-003 | D04 | alta | Cargo Management Service, Route Planning Service | Cargo Management Service -> Route Planning Service; Route Planning Service -> Cargo Management Service |
| D04-004 | D04 | alta | Cargo Tracking Service, Event Processing Service | Cargo Tracking Service -> Event Processing Service; Event Processing Service -> Cargo Tracking Service |
| D04-005 | D04 | alta | Cargo Tracking Service, Integration Service | Cargo Tracking Service -> Integration Service; Integration Service -> Cargo Tracking Service |
| D04-006 | D04 | alta | Cargo Tracking Service, Route Planning Service | Cargo Tracking Service -> Route Planning Service; Route Planning Service -> Cargo Tracking Service |
| D04-007 | D04 | alta | Event Processing Service, Logistics Network Service | Event Processing Service -> Logistics Network Service; Logistics Network Service -> Event Processing Service |
| D04-008 | D04 | alta | Logistics Network Service, Route Planning Service | Logistics Network Service -> Route Planning Service; Route Planning Service -> Logistics Network Service |
| D11-001 | D11 | media | Cargo Management Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-002 | D11 | media | Cargo Tracking Service | 1 endpoint(s) para 11 responsabilidade(s) |
| D11-003 | D11 | media | Event Processing Service | 1 endpoint(s) para 11 responsabilidade(s) |
| D11-004 | D11 | media | Integration Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-005 | D11 | media | Logistics Network Service | 2 endpoint(s) para 6 responsabilidade(s) |
| D11-006 | D11 | media | Route Planning Service | 1 endpoint(s) para 10 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
