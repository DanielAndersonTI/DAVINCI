# Laudo VIA — DayTrader7

**Modelo:** Gemini  
**Configuracao:** C1  
**Rodada:** 3  
**Execucao:** `20260903_171921_736232`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 76 |
| Servicos | 6 |
| Arestas | 10 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1667 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2204 | calculado |
| endpoints_por_responsabilidade | 0.1935 | calculado |
| estabilidade_jaccard_servicos | 0.9167 | calculado |
| estabilidade_jaccard_arestas | 0.3207 | calculado |
| taxa_defeitos_por_servico | 1.3333 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Portfolio Service, Trading Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Portfolio Service, Trading Service | Portfolio Service -> Trading Service; Trading Service -> Portfolio Service |
| D05-001 | D05 | alta | Investor Account Service, total logins | nome nao resolvido: total logins |
| D05-002 | D05 | alta | Simulation Administration Service, simulation limits | nome nao resolvido: simulation limits |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-002 | D11 | media | Investor Account Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | Market Data Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-004 | D11 | media | Portfolio Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-005 | D11 | media | Trading Service | 1 endpoint(s) para 9 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
