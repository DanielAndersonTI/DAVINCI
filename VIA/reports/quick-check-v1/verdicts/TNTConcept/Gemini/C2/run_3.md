# Laudo VIA — TNTConcept

**Modelo:** Gemini  
**Configuracao:** C2  
**Rodada:** 3  
**Execucao:** `20260907_232226_089142`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 45 |
| Servicos | 12 |
| Arestas | 33 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0833 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1688 | calculado |
| endpoints_por_responsabilidade | 0.3077 | calculado |
| estabilidade_jaccard_servicos | 0.5000 | calculado |
| estabilidade_jaccard_arestas | 0.2719 | calculado |
| taxa_defeitos_por_servico | 0.7500 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Billing Service, Financial Management Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Billing Service, Financial Management Service | Billing Service -> Financial Management Service; Financial Management Service -> Billing Service |
| D11-001 | D11 | media | Administration and Configuration Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-002 | D11 | media | Billing Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | CRM and Proposals Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-004 | D11 | media | Content and Document Management Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-005 | D11 | media | Financial Management Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-006 | D11 | media | Identity and Access Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-007 | D11 | media | Project and Work Tracking Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-008 | D11 | media | Workforce Management Service | 1 endpoint(s) para 4 responsabilidade(s) |

## Avisos

- 12 non-bullet lines ignored in requirements

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
