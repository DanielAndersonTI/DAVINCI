# Laudo VIA — TNTConcept

**Modelo:** Gemini  
**Configuracao:** C3  
**Rodada:** 3  
**Execucao:** `20260908_100952_521021`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 45 |
| Servicos | 12 |
| Arestas | 40 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0833 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2633 | calculado |
| endpoints_por_responsabilidade | 0.4800 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.5492 | calculado |
| taxa_defeitos_por_servico | 0.7500 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Commissioning Service, Content and Document Management Service, File Storage Service, Financial Management Service, Notification Service, Project and Work Tracking Service, Workforce Management Service | componente fortemente conexa com 7 servicos |
| D04-002 | D04 | alta | Commissioning Service, File Storage Service | Commissioning Service -> File Storage Service; File Storage Service -> Commissioning Service |
| D04-003 | D04 | alta | Commissioning Service, Notification Service | Commissioning Service -> Notification Service; Notification Service -> Commissioning Service |
| D04-004 | D04 | alta | Commissioning Service, Project and Work Tracking Service | Commissioning Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Commissioning Service |
| D04-005 | D04 | alta | Commissioning Service, Workforce Management Service | Commissioning Service -> Workforce Management Service; Workforce Management Service -> Commissioning Service |
| D04-006 | D04 | alta | Content and Document Management Service, File Storage Service | Content and Document Management Service -> File Storage Service; File Storage Service -> Content and Document Management Service |
| D04-007 | D04 | alta | File Storage Service, Project and Work Tracking Service | File Storage Service -> Project and Work Tracking Service; Project and Work Tracking Service -> File Storage Service |
| D04-008 | D04 | alta | Financial Management Service, Project and Work Tracking Service | Financial Management Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Financial Management Service |
| D04-009 | D04 | alta | Notification Service, Project and Work Tracking Service | Notification Service -> Project and Work Tracking Service; Project and Work Tracking Service -> Notification Service |
| D04-010 | D04 | alta | Notification Service, Workforce Management Service | Notification Service -> Workforce Management Service; Workforce Management Service -> Notification Service |
| D04-011 | D04 | alta | Project and Work Tracking Service, Workforce Management Service | Project and Work Tracking Service -> Workforce Management Service; Workforce Management Service -> Project and Work Tracking Service |
| D05-001 | D05 | alta | Administration and Configuration Service, contract types | nome nao resolvido: contract types |
| D05-002 | D05 | alta | Billing Service, taxes | nome nao resolvido: taxes |
| D05-003 | D05 | alta | CRM and Proposals Service, contacts | nome nao resolvido: contacts |
| D05-004 | D05 | alta | Identity and Access Service, contractual | nome nao resolvido: contractual |
| D11-001 | D11 | media | Financial Management Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-002 | D11 | media | Project and Work Tracking Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-003 | D11 | media | Workforce Management Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Avisos

- 12 non-bullet lines ignored in requirements

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
