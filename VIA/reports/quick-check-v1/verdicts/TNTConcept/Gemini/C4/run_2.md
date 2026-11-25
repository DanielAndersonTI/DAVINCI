# Laudo VIA — TNTConcept

**Modelo:** Gemini  
**Configuracao:** C4  
**Rodada:** 2  
**Execucao:** `20260924_003112_676069`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 45 |
| Servicos | 12 |
| Arestas | 66 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0833 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1520 | calculado |
| endpoints_por_responsabilidade | 0.3529 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.8030 | calculado |
| taxa_defeitos_por_servico | 0.6667 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Administration and Configuration Service, Billing Service, CRM and Proposals Service, Commissioning Service, Content and Document Management Service, File Storage Service, Financial Management Service, Identity and Access Service, Notification Service, Project and Work Tracking Service, Reporting Service, Workforce Management Service | componente fortemente conexa com 12 servicos |
| D04-002 | D04 | alta | Administration and Configuration Service, Billing Service | Administration and Configuration Service -> Billing Service; Billing Service -> Administration and Configuration Service |
| D04-003 | D04 | alta | Administration and Configuration Service, CRM and Proposals Service | Administration and Configuration Service -> CRM and Proposals Service; CRM and Proposals Service -> Administration and Configuration Service |
| D04-004 | D04 | alta | Administration and Configuration Service, File Storage Service | Administration and Configuration Service -> File Storage Service; File Storage Service -> Administration and Configuration Service |
| D04-005 | D04 | alta | Administration and Configuration Service, Identity and Access Service | Administration and Configuration Service -> Identity and Access Service; Identity and Access Service -> Administration and Configuration Service |
| D04-006 | D04 | alta | Administration and Configuration Service, Notification Service | Administration and Configuration Service -> Notification Service; Notification Service -> Administration and Configuration Service |
| D04-007 | D04 | alta | Administration and Configuration Service, Reporting Service | Administration and Configuration Service -> Reporting Service; Reporting Service -> Administration and Configuration Service |
| D04-008 | D04 | alta | Administration and Configuration Service, Workforce Management Service | Administration and Configuration Service -> Workforce Management Service; Workforce Management Service -> Administration and Configuration Service |
| D04-009 | D04 | alta | Billing Service, CRM and Proposals Service | Billing Service -> CRM and Proposals Service; CRM and Proposals Service -> Billing Service |
| D04-010 | D04 | alta | Billing Service, File Storage Service | Billing Service -> File Storage Service; File Storage Service -> Billing Service |
| D04-011 | D04 | alta | Billing Service, Financial Management Service | Billing Service -> Financial Management Service; Financial Management Service -> Billing Service |
| D04-012 | D04 | alta | Billing Service, Project and Work Tracking Service | Billing Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Billing Service |
| D04-013 | D04 | alta | Billing Service, Reporting Service | Billing Service -> Reporting Service; Reporting Service -> Billing Service |
| D04-014 | D04 | alta | CRM and Proposals Service, Project and Work Tracking Service | CRM and Proposals Service -> Project and Work Tracking Service; Project and Work Tracking Service -> CRM and Proposals Service |
| D04-015 | D04 | alta | CRM and Proposals Service, Reporting Service | CRM and Proposals Service -> Reporting Service; Reporting Service -> CRM and Proposals Service |
| D04-016 | D04 | alta | Commissioning Service, File Storage Service | Commissioning Service -> File Storage Service; File Storage Service -> Commissioning Service |
| D04-017 | D04 | alta | Commissioning Service, Notification Service | Commissioning Service -> Notification Service; Notification Service -> Commissioning Service |
| D04-018 | D04 | alta | Commissioning Service, Project and Work Tracking Service | Commissioning Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Commissioning Service |
| D04-019 | D04 | alta | Commissioning Service, Reporting Service | Commissioning Service -> Reporting Service; Reporting Service -> Commissioning Service |
| D04-020 | D04 | alta | Commissioning Service, Workforce Management Service | Commissioning Service -> Workforce Management Service; Workforce Management Service -> Commissioning Service |
| D04-021 | D04 | alta | Content and Document Management Service, File Storage Service | Content and Document Management Service -> File Storage Service; File Storage Service -> Content and Document Management Service |
| D04-022 | D04 | alta | Content and Document Management Service, Identity and Access Service | Content and Document Management Service -> Identity and Access Service; Identity and Access Service -> Content and Document Management Service |
| D04-023 | D04 | alta | Content and Document Management Service, Reporting Service | Content and Document Management Service -> Reporting Service; Reporting Service -> Content and Document Management Service |
| D04-024 | D04 | alta | File Storage Service, Project and Work Tracking Service | File Storage Service -> Project and Work Tracking Service; Project and Work Tracking Service -> File Storage Service |
| D04-025 | D04 | alta | Financial Management Service, Project and Work Tracking Service | Financial Management Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Financial Management Service |
| D04-026 | D04 | alta | Financial Management Service, Reporting Service | Financial Management Service -> Reporting Service; Reporting Service -> Financial Management Service |
| D04-027 | D04 | alta | Identity and Access Service, Project and Work Tracking Service | Identity and Access Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Identity and Access Service |
| D04-028 | D04 | alta | Identity and Access Service, Reporting Service | Identity and Access Service -> Reporting Service; Reporting Service -> Identity and Access Service |
| D04-029 | D04 | alta | Identity and Access Service, Workforce Management Service | Identity and Access Service -> Workforce Management Service; Workforce Management Service -> Identity and Access Service |
| D04-030 | D04 | alta | Notification Service, Project and Work Tracking Service | Notification Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Notification Service |
| D04-031 | D04 | alta | Notification Service, Workforce Management Service | Notification Service -> Workforce Management Service; Workforce Management Service -> Notification Service |
| D04-032 | D04 | alta | Project and Work Tracking Service, Reporting Service | Project and Work Tracking Service -> Reporting Service; Reporting Service -> Project and Work Tracking Service |
| D04-033 | D04 | alta | Project and Work Tracking Service, Workforce Management Service | Project and Work Tracking Service -> Workforce Management Service; Workforce Management Service -> Project and Work Tracking Service |
| D04-034 | D04 | alta | Reporting Service, Workforce Management Service | Reporting Service -> Workforce Management Service; Workforce Management Service -> Reporting Service |
| D11-001 | D11 | media | Administration and Configuration Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-002 | D11 | media | Billing Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-003 | D11 | media | CRM and Proposals Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-004 | D11 | media | Financial Management Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-005 | D11 | media | Identity and Access Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-006 | D11 | media | Project and Work Tracking Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-007 | D11 | media | Workforce Management Service | 1 endpoint(s) para 3 responsabilidade(s) |

## Avisos

- 12 non-bullet lines ignored in requirements

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
