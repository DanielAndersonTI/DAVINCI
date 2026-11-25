# Laudo VIA — DayTrader7

**Modelo:** Gemini  
**Configuracao:** C2  
**Rodada:** 3  
**Execucao:** `20260907_231926_924901`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 76 |
| Servicos | 7 |
| Arestas | 17 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2857 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1933 | calculado |
| endpoints_por_responsabilidade | 0.2059 | calculado |
| estabilidade_jaccard_servicos | 0.7143 | calculado |
| estabilidade_jaccard_arestas | 0.4832 | calculado |
| taxa_defeitos_por_servico | 1.2857 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, Investor Account Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Market Data Service, Portfolio Service, Simulation Administration Service, Trading Service | componente fortemente conexa com 4 servicos |
| D04-003 | D04 | alta | Authentication Service, Investor Account Service | Authentication Service -> Investor Account Service; Investor Account Service -> Authentication Service |
| D04-004 | D04 | alta | Market Data Service, Simulation Administration Service | Market Data Service -> Simulation Administration Service; Simulation Administration Service -> Market Data Service |
| D04-005 | D04 | alta | Portfolio Service, Trading Service | Portfolio Service -> Trading Service; Trading Service -> Portfolio Service |
| D04-006 | D04 | alta | Simulation Administration Service, Trading Service | Simulation Administration Service -> Trading Service; Trading Service -> Simulation Administration Service |
| D05-001 | D05 | alta | Output must be pure CSV without markdown code blocks, or comments.Microservice | nome nao resolvido: or comments.Microservice |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-002 | D11 | media | Investor Account Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-003 | D11 | media | Market Data Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-004 | D11 | media | Portfolio Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-005 | D11 | media | Simulation Administration Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-006 | D11 | media | Trading Service | 1 endpoint(s) para 6 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
