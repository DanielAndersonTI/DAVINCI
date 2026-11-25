# Laudo VIA — AcmeAir

**Modelo:** DeepSeek  
**Configuracao:** C4  
**Rodada:** 2  
**Execucao:** `20260923_212438_528904`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 61 |
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
| gini_granularidade | 0.1263 | calculado |
| endpoints_por_responsabilidade | 0.1818 | calculado |
| estabilidade_jaccard_servicos | 0.8571 | calculado |
| estabilidade_jaccard_arestas | 0.7375 | calculado |
| taxa_defeitos_por_servico | 1.1667 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, Booking Service, Customer Profile Service, Environment Administration Service, Flight Search Service, Loyalty Service | componente fortemente conexa com 6 servicos |
| D04-002 | D04 | alta | Authentication Service, Booking Service | Authentication Service -> Booking Service; Booking Service -> Authentication Service |
| D04-003 | D04 | alta | Authentication Service, Customer Profile Service | Authentication Service -> Customer Profile Service; Customer Profile Service -> Authentication Service |
| D04-004 | D04 | alta | Authentication Service, Environment Administration Service | Authentication Service -> Environment Administration Service; Environment Administration Service -> Authentication Service |
| D04-005 | D04 | alta | Authentication Service, Loyalty Service | Authentication Service -> Loyalty Service; Loyalty Service -> Authentication Service |
| D04-006 | D04 | alta | Booking Service, Environment Administration Service | Booking Service -> Environment Administration Service; Environment Administration Service -> Booking Service |
| D04-007 | D04 | alta | Booking Service, Flight Search Service | Booking Service -> Flight Search Service; Flight Search Service -> Booking Service |
| D04-008 | D04 | alta | Customer Profile Service, Environment Administration Service | Customer Profile Service -> Environment Administration Service; Environment Administration Service -> Customer Profile Service |
| D04-009 | D04 | alta | Environment Administration Service, Flight Search Service | Environment Administration Service -> Flight Search Service; Flight Search Service -> Environment Administration Service |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-002 | D11 | media | Booking Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-003 | D11 | media | Customer Profile Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-004 | D11 | media | Environment Administration Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-005 | D11 | media | Flight Search Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-006 | D11 | media | Loyalty Service | 1 endpoint(s) para 4 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
