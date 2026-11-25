# Laudo VIA — TNTConcept

**Modelo:** Claude  
**Configuracao:** C2  
**Rodada:** 3  
**Execucao:** `20260917_002445_864904`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 45 |
| Servicos | 12 |
| Arestas | 49 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0833 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2383 | calculado |
| endpoints_por_responsabilidade | 0.1690 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.9900 | calculado |
| taxa_defeitos_por_servico | 1.0000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Administration Service, Billing Service, CRM Service, Commissioning Service, Content Management Service, File Storage Service, Financial Service, Identity Service, Notification Service, Project Tracking Service, Workforce Service | componente fortemente conexa com 11 servicos |
| D04-002 | D04 | alta | Administration Service, Billing Service | Administration Service -> Billing Service; Billing Service -> Administration Service |
| D04-003 | D04 | alta | Administration Service, CRM Service | Administration Service -> CRM Service; CRM Service -> Administration Service |
| D04-004 | D04 | alta | Administration Service, File Storage Service | Administration Service -> File Storage Service; File Storage Service -> Administration Service |
| D04-005 | D04 | alta | Administration Service, Identity Service | Administration Service -> Identity Service; Identity Service -> Administration Service |
| D04-006 | D04 | alta | Administration Service, Notification Service | Administration Service -> Notification Service; Notification Service -> Administration Service |
| D04-007 | D04 | alta | Administration Service, Workforce Service | Administration Service -> Workforce Service; Workforce Service -> Administration Service |
| D04-008 | D04 | alta | Billing Service, CRM Service | Billing Service -> CRM Service; CRM Service -> Billing Service |
| D04-009 | D04 | alta | Billing Service, File Storage Service | Billing Service -> File Storage Service; File Storage Service -> Billing Service |
| D04-010 | D04 | alta | Billing Service, Financial Service | Billing Service -> Financial Service; Financial Service -> Billing Service |
| D04-011 | D04 | alta | CRM Service, Project Tracking Service | CRM Service -> Project Tracking Service; Project Tracking Service -> CRM Service |
| D04-012 | D04 | alta | Commissioning Service, File Storage Service | Commissioning Service -> File Storage Service; File Storage Service -> Commissioning Service |
| D04-013 | D04 | alta | Commissioning Service, Notification Service | Commissioning Service -> Notification Service; Notification Service -> Commissioning Service |
| D04-014 | D04 | alta | Content Management Service, File Storage Service | Content Management Service -> File Storage Service; File Storage Service -> Content Management Service |
| D04-015 | D04 | alta | Content Management Service, Identity Service | Content Management Service -> Identity Service; Identity Service -> Content Management Service |
| D04-016 | D04 | alta | File Storage Service, Project Tracking Service | File Storage Service -> Project Tracking Service; Project Tracking Service -> File Storage Service |
| D04-017 | D04 | alta | Financial Service, Project Tracking Service | Financial Service -> Project Tracking Service; Project Tracking Service -> Financial Service |
| D04-018 | D04 | alta | Identity Service, Project Tracking Service | Identity Service -> Project Tracking Service; Project Tracking Service -> Identity Service |
| D04-019 | D04 | alta | Identity Service, Workforce Service | Identity Service -> Workforce Service; Workforce Service -> Identity Service |
| D04-020 | D04 | alta | Notification Service, Workforce Service | Notification Service -> Workforce Service; Workforce Service -> Notification Service |
| D11-001 | D11 | media | Administration Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-002 | D11 | media | Billing Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-003 | D11 | media | CRM Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-004 | D11 | media | Commissioning Service | 1 endpoint(s) para 6 responsabilidade(s) |
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
