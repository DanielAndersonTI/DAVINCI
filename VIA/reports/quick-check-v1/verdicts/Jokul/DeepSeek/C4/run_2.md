# Laudo VIA — Jokul

**Modelo:** DeepSeek  
**Configuracao:** C4  
**Rodada:** 2  
**Execucao:** `20260923_212538_104523`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 66 |
| Servicos | 4 |
| Arestas | 6 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.5000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2744 | calculado |
| endpoints_por_responsabilidade | 0.0976 | calculado |
| estabilidade_jaccard_servicos | 0.5750 | calculado |
| estabilidade_jaccard_arestas | 0.3500 | calculado |
| taxa_defeitos_por_servico | 1.5000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, User Management Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Media Service, Movie Catalog Service | componente fortemente conexa com 2 servicos |
| D04-003 | D04 | alta | Authentication Service, User Management Service | Authentication Service -> User Management Service; User Management Service -> Authentication Service |
| D04-004 | D04 | alta | Media Service, Movie Catalog Service | Media Service -> Movie Catalog Service; Movie Catalog Service -> Media Service |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-002 | D11 | media | Media Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-003 | D11 | media | Movie Catalog Service | 1 endpoint(s) para 19 responsabilidade(s) |
| D11-004 | D11 | media | User Management Service | 1 endpoint(s) para 4 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
