# Laudo VIA — 7ep

**Modelo:** DeepSeek  
**Configuracao:** C1  
**Rodada:** 1  
**Execucao:** `20260909_103416_609424`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 78 |
| Servicos | 7 |
| Arestas | 18 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1429 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1357 | calculado |
| endpoints_por_responsabilidade | 0.1750 | calculado |
| estabilidade_jaccard_servicos | 0.9375 | calculado |
| estabilidade_jaccard_arestas | 0.7341 | calculado |
| taxa_defeitos_por_servico | 1.1429 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Audit Service, Authentication Service, Book Catalog Service, Loan Management Service, Reader Management Service | componente fortemente conexa com 5 servicos |
| D04-002 | D04 | alta | Audit Service, Authentication Service | Audit Service -> Authentication Service; Authentication Service -> Audit Service |
| D04-003 | D04 | alta | Audit Service, Book Catalog Service | Audit Service -> Book Catalog Service; Book Catalog Service -> Audit Service |
| D04-004 | D04 | alta | Audit Service, Loan Management Service | Audit Service -> Loan Management Service; Loan Management Service -> Audit Service |
| D04-005 | D04 | alta | Audit Service, Reader Management Service | Audit Service -> Reader Management Service; Reader Management Service -> Audit Service |
| D04-006 | D04 | alta | Book Catalog Service, Loan Management Service | Book Catalog Service -> Loan Management Service; Loan Management Service -> Book Catalog Service |
| D04-007 | D04 | alta | Loan Management Service, Reader Management Service | Loan Management Service -> Reader Management Service; Reader Management Service -> Loan Management Service |
| D11-001 | D11 | media | Audit Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-002 | D11 | media | Authentication Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-003 | D11 | media | Book Catalog Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-004 | D11 | media | Demo Utility Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-005 | D11 | media | Environment Management Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-006 | D11 | media | Loan Management Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-007 | D11 | media | Reader Management Service | 1 endpoint(s) para 6 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
