# Laudo VIA — Jokul

**Modelo:** DeepSeek  
**Configuracao:** C0  
**Rodada:** 3  
**Execucao:** `20260909_001722_534070`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 66 |
| Servicos | 3 |
| Arestas | 6 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.3333 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.0741 | calculado |
| endpoints_por_responsabilidade | 0.1667 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.7857 | calculado |
| taxa_defeitos_por_servico | 1.3333 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, Media Service, Movie Catalog Service | componente fortemente conexa com 3 servicos |
| D04-002 | D04 | alta | Authentication Service, Media Service | Authentication Service -> Media Service; Media Service -> Authentication Service |
| D04-003 | D04 | alta | Authentication Service, Movie Catalog Service | Authentication Service -> Movie Catalog Service; Movie Catalog Service -> Authentication Service |
| D04-004 | D04 | alta | Media Service, Movie Catalog Service | Media Service -> Movie Catalog Service; Movie Catalog Service -> Media Service |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-002 | D11 | media | Media Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | Movie Catalog Service | 1 endpoint(s) para 7 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
