# Laudo VIA — DayTrader7

**Modelo:** DeepSeek  
**Configuracao:** C4  
**Rodada:** 2  
**Execucao:** `20260923_212515_725336`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 76 |
| Servicos | 6 |
| Arestas | 16 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1667 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1795 | calculado |
| endpoints_por_responsabilidade | 0.1346 | calculado |
| estabilidade_jaccard_servicos | 0.6250 | calculado |
| estabilidade_jaccard_arestas | 0.4492 | calculado |
| taxa_defeitos_por_servico | 1.3333 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, Market Data Service, Order History Service, Portfolio Service, Simulation Administration Service, Trading Service | componente fortemente conexa com 6 servicos |
| D04-002 | D04 | alta | Authentication Service, Portfolio Service | Authentication Service -> Portfolio Service; Portfolio Service -> Authentication Service |
| D04-003 | D04 | alta | Authentication Service, Trading Service | Authentication Service -> Trading Service; Trading Service -> Authentication Service |
| D04-004 | D04 | alta | Market Data Service, Trading Service | Market Data Service -> Trading Service; Trading Service -> Market Data Service |
| D04-005 | D04 | alta | Order History Service, Trading Service | Order History Service -> Trading Service; Trading Service -> Order History Service |
| D04-006 | D04 | alta | Portfolio Service, Trading Service | Portfolio Service -> Trading Service; Trading Service -> Portfolio Service |
| D04-007 | D04 | alta | Simulation Administration Service, Trading Service | Simulation Administration Service -> Trading Service; Trading Service -> Simulation Administration Service |
| D06-001 | D06 | media | Authentication Service | Authentication Service -> Authentication Service |
| D11-001 | D11 | media | Authentication Service | 2 endpoint(s) para 12 responsabilidade(s) |
| D11-002 | D11 | media | Market Data Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | Order History Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-004 | D11 | media | Portfolio Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-005 | D11 | media | Simulation Administration Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-006 | D11 | media | Trading Service | 1 endpoint(s) para 12 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
