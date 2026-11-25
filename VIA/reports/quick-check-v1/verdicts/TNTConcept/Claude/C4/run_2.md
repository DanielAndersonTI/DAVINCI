# Laudo VIA — TNTConcept

**Modelo:** Claude  
**Configuracao:** C4  
**Rodada:** 2  
**Execucao:** `20260923_203646_754009`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 45 |
| Servicos | 12 |
| Arestas | 30 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0833 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2405 | calculado |
| endpoints_por_responsabilidade | 0.1714 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.5918 | calculado |
| taxa_defeitos_por_servico | 1.0000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Billing Service, Financial Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Billing Service, Financial Service | Billing Service -> Financial Service; Financial Service -> Billing Service |
| D11-001 | D11 | media | Administration Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-002 | D11 | media | Billing Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-003 | D11 | media | CRM Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-004 | D11 | media | Commissioning Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-005 | D11 | media | Content Management Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-006 | D11 | media | File Storage Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-007 | D11 | media | Financial Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-008 | D11 | media | Identity Service | 1 endpoint(s) para 11 responsabilidade(s) |
| D11-009 | D11 | media | Notification Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-010 | D11 | media | Project Tracking Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-011 | D11 | media | Workforce Service | 1 endpoint(s) para 5 responsabilidade(s) |

## Avisos

- 12 non-bullet lines ignored in requirements

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
