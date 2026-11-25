# Laudo VIA — Jokul

**Modelo:** Claude  
**Configuracao:** C4  
**Rodada:** 2  
**Execucao:** `20260923_203416_082971`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 66 |
| Servicos | 3 |
| Arestas | 4 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.3333 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.0580 | calculado |
| endpoints_por_responsabilidade | 0.1304 | calculado |
| estabilidade_jaccard_servicos | 0.7500 | calculado |
| estabilidade_jaccard_arestas | 0.5000 | calculado |
| taxa_defeitos_por_servico | 1.3333 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Media Service, Movie Catalog Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Media Service, Movie Catalog Service | Media Service -> Movie Catalog Service; Movie Catalog Service -> Media Service |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-002 | D11 | media | Media Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-003 | D11 | media | Movie Catalog Service | 1 endpoint(s) para 9 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
