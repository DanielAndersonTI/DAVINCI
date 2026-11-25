# Laudo VIA — Jokul

**Modelo:** DeepSeek  
**Configuracao:** C3  
**Rodada:** 1  
**Execucao:** `20260908_151820_469565`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 66 |
| Servicos | 3 |
| Arestas | 5 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.3333 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2083 | calculado |
| endpoints_por_responsabilidade | 0.1875 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.5714 | calculado |
| taxa_defeitos_por_servico | 1.3333 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, Media Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Authentication Service, Media Service | Authentication Service -> Media Service; Media Service -> Authentication Service |
| D05-001 | D05 | alta | Movie Catalog Service, rating | nome nao resolvido: rating |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-002 | D11 | media | Media Service | 1 endpoint(s) para 7 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
