# Laudo VIA — JPetStore

**Modelo:** Claude  
**Configuracao:** C3  
**Rodada:** 1  
**Execucao:** `20260919_002344_285942`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 77 |
| Servicos | 6 |
| Arestas | 7 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2652 | calculado |
| endpoints_por_responsabilidade | 0.1364 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.8500 | calculado |
| taxa_defeitos_por_servico | 1.0000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-002 | D11 | media | Catalog Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-003 | D11 | media | Customer Account Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-004 | D11 | media | Inventory Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-005 | D11 | media | Order Service | 1 endpoint(s) para 15 responsabilidade(s) |
| D11-006 | D11 | media | Shopping Cart Service | 1 endpoint(s) para 8 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
