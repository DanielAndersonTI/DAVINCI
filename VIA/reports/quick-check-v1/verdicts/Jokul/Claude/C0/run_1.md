# Laudo VIA — Jokul

**Modelo:** Claude  
**Configuracao:** C0  
**Rodada:** 1  
**Execucao:** `20260916_223723_901253`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 66 |
| Servicos | 4 |
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
| gini_granularidade | 0.0700 | calculado |
| endpoints_por_responsabilidade | 0.1600 | calculado |
| estabilidade_jaccard_servicos | 0.8750 | calculado |
| estabilidade_jaccard_arestas | 0.7500 | calculado |
| taxa_defeitos_por_servico | 1.0000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-002 | D11 | media | Media Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | Movie Catalog Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-004 | D11 | media | Movie Management Service | 1 endpoint(s) para 6 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
