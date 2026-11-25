# Laudo VIA — TNTConcept

**Modelo:** Gemini  
**Configuracao:** C4  
**Rodada:** 3  
**Execucao:** `20260924_004820_759079`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 45 |
| Servicos | 12 |
| Arestas | 42 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0833 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1389 | calculado |
| endpoints_por_responsabilidade | 0.3636 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.6336 | calculado |
| taxa_defeitos_por_servico | 0.6667 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Administration and Configuration Service, Billing Service, CRM and Proposals Service, Content and Document Management Service, File Storage Service, Financial Management Service, Identity and Access Service, Notification Service, Project and Work Tracking Service, Workforce Management Service | componente fortemente conexa com 10 servicos |
| D04-002 | D04 | alta | Administration and Configuration Service, Billing Service | Administration and Configuration Service -> Billing Service; Billing Service -> Administration and Configuration Service |
| D04-003 | D04 | alta | Administration and Configuration Service, CRM and Proposals Service | Administration and Configuration Service -> CRM and Proposals Service; CRM and Proposals Service -> Administration and Configuration Service |
| D04-004 | D04 | alta | Administration and Configuration Service, Identity and Access Service | Administration and Configuration Service -> Identity and Access Service; Identity and Access Service -> Administration and Configuration Service |
| D04-005 | D04 | alta | Administration and Configuration Service, Notification Service | Administration and Configuration Service -> Notification Service; Notification Service -> Administration and Configuration Service |
| D04-006 | D04 | alta | Administration and Configuration Service, Workforce Management Service | Administration and Configuration Service -> Workforce Management Service; Workforce Management Service -> Administration and Configuration Service |
| D04-007 | D04 | alta | Billing Service, Financial Management Service | Billing Service -> Financial Management Service; Financial Management Service -> Billing Service |
| D04-008 | D04 | alta | Content and Document Management Service, Identity and Access Service | Content and Document Management Service -> Identity and Access Service; Identity and Access Service -> Content and Document Management Service |
| D04-009 | D04 | alta | Identity and Access Service, Project and Work Tracking Service | Identity and Access Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Identity and Access Service |
| D04-010 | D04 | alta | Identity and Access Service, Workforce Management Service | Identity and Access Service -> Workforce Management Service; Workforce Management Service -> Identity and Access Service |
| D11-001 | D11 | media | Administration and Configuration Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-002 | D11 | media | Billing Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-003 | D11 | media | CRM and Proposals Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-004 | D11 | media | Financial Management Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-005 | D11 | media | Identity and Access Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-006 | D11 | media | Project and Work Tracking Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-007 | D11 | media | Workforce Management Service | 1 endpoint(s) para 3 responsabilidade(s) |

## Avisos

- 12 non-bullet lines ignored in requirements

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
