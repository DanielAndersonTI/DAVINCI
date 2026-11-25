# Laudo VIA — DayTrader7

**Modelo:** DeepSeek  
**Configuracao:** C4  
**Rodada:** 3  
**Execucao:** `20260923_213801_898837`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 76 |
| Servicos | 7 |
| Arestas | 20 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1429 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1905 | calculado |
| endpoints_por_responsabilidade | 0.1373 | calculado |
| estabilidade_jaccard_servicos | 0.8125 | calculado |
| estabilidade_jaccard_arestas | 0.6486 | calculado |
| taxa_defeitos_por_servico | 1.1429 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Auth Service, Investor Account Service, Market Data Service, Order History Service, Portfolio Service, Simulation Administration Service, Trading Service | componente fortemente conexa com 7 servicos |
| D04-002 | D04 | alta | Auth Service, Investor Account Service | Auth Service -> Investor Account Service; Investor Account Service -> Auth Service |
| D04-003 | D04 | alta | Investor Account Service, Portfolio Service | Investor Account Service -> Portfolio Service; Portfolio Service -> Investor Account Service |
| D04-004 | D04 | alta | Investor Account Service, Trading Service | Investor Account Service -> Trading Service; Trading Service -> Investor Account Service |
| D04-005 | D04 | alta | Market Data Service, Trading Service | Market Data Service -> Trading Service; Trading Service -> Market Data Service |
| D04-006 | D04 | alta | Order History Service, Simulation Administration Service | Order History Service -> Simulation Administration Service; Simulation Administration Service -> Order History Service |
| D04-007 | D04 | alta | Order History Service, Trading Service | Order History Service -> Trading Service; Trading Service -> Order History Service |
| D04-008 | D04 | alta | Portfolio Service, Trading Service | Portfolio Service -> Trading Service; Trading Service -> Portfolio Service |
| D04-009 | D04 | alta | Simulation Administration Service, Trading Service | Simulation Administration Service -> Trading Service; Trading Service -> Simulation Administration Service |
| D11-001 | D11 | media | Auth Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-002 | D11 | media | Investor Account Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-003 | D11 | media | Market Data Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-004 | D11 | media | Order History Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-005 | D11 | media | Portfolio Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-006 | D11 | media | Simulation Administration Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-007 | D11 | media | Trading Service | 1 endpoint(s) para 12 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
