# Laudo VIA — 7ep

**Modelo:** Claude  
**Configuracao:** C3  
**Rodada:** 1  
**Execucao:** `20260919_002149_858658`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 78 |
| Servicos | 7 |
| Arestas | 10 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1661 | calculado |
| endpoints_por_responsabilidade | 0.1628 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 1.0000 | calculado |
| taxa_defeitos_por_servico | 1.1429 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D03-001 | D03 | baixa | Demo Utility Service | grau de entrada 0 e grau de saida 0 |
| D11-001 | D11 | media | Audit Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-002 | D11 | media | Authentication Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-003 | D11 | media | Book Catalog Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-004 | D11 | media | Demo Utility Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-005 | D11 | media | Environment Management Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-006 | D11 | media | Loan Management Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-007 | D11 | media | Reader Management Service | 1 endpoint(s) para 7 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
