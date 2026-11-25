# Laudo VIA — DayTrader7

**Modelo:** DeepSeek  
**Configuracao:** C0  
**Rodada:** 1  
**Execucao:** `20260909_000040_069614`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 76 |
| Servicos | 4 |
| Arestas | 11 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2500 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1897 | calculado |
| endpoints_por_responsabilidade | 0.0862 | calculado |
| estabilidade_jaccard_servicos | 0.5714 | calculado |
| estabilidade_jaccard_arestas | 0.4393 | calculado |
| taxa_defeitos_por_servico | 2.5000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, Investor Service, Market Data Service, Trading Service | componente fortemente conexa com 4 servicos |
| D04-002 | D04 | alta | Authentication Service, Investor Service | Authentication Service -> Investor Service; Investor Service -> Authentication Service |
| D04-003 | D04 | alta | Authentication Service, Trading Service | Authentication Service -> Trading Service; Trading Service -> Authentication Service |
| D04-004 | D04 | alta | Market Data Service, Trading Service | Market Data Service -> Trading Service; Trading Service -> Market Data Service |
| D05-001 | D05 | alta | Authentication Service, Portfolio Service | nome nao resolvido: Portfolio Service |
| D05-002 | D05 | alta | Trading Service, Order History Service | nome nao resolvido: Order History Service |
| D05-003 | D05 | alta | Trading Service, Portfolio Service | nome nao resolvido: Portfolio Service |
| D05-004 | D05 | alta | Trading Service, Simulation Administration Service | nome nao resolvido: Simulation Administration Service |
| D06-001 | D06 | media | Authentication Service | Authentication Service -> Authentication Service |
| D11-001 | D11 | media | Authentication Service | 2 endpoint(s) para 14 responsabilidade(s) |
| D11-002 | D11 | media | Investor Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-003 | D11 | media | Market Data Service | 1 endpoint(s) para 16 responsabilidade(s) |
| D11-004 | D11 | media | Trading Service | 1 endpoint(s) para 21 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
