# Laudo VIA — DayTrader7

**Modelo:** DeepSeek  
**Configuracao:** C1  
**Rodada:** 3  
**Execucao:** `20260909_110219_868035`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 76 |
| Servicos | 5 |
| Arestas | 7 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2857 | calculado |
| endpoints_por_responsabilidade | 0.2143 | calculado |
| estabilidade_jaccard_servicos | 0.7143 | calculado |
| estabilidade_jaccard_arestas | 0.1861 | calculado |
| taxa_defeitos_por_servico | 1.8000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, Investor Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Authentication Service, Investor Service | Authentication Service -> Investor Service; Investor Service -> Authentication Service |
| D05-001 | D05 | alta | Market Data Service, traded volume | nome nao resolvido: traded volume |
| D05-002 | D05 | alta | Portfolio Service, purchase date | nome nao resolvido: purchase date |
| D05-003 | D05 | alta | Trading Service, type | nome nao resolvido: type |
| D11-001 | D11 | media | Authentication Service | 2 endpoint(s) para 12 responsabilidade(s) |
| D11-002 | D11 | media | Investor Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | Market Data Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-004 | D11 | media | Portfolio Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-005 | D11 | media | Trading Service | 1 endpoint(s) para 3 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
