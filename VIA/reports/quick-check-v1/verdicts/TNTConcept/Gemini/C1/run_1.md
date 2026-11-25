# Laudo VIA — TNTConcept

**Modelo:** Gemini  
**Configuracao:** C1  
**Rodada:** 1  
**Execucao:** `20260902_235207_721636`

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
| gini_granularidade | 0.1843 | calculado |
| endpoints_por_responsabilidade | 0.3636 | calculado |
| estabilidade_jaccard_servicos | 0.0000 | calculado |
| estabilidade_jaccard_arestas | 0.0000 | calculado |
| taxa_defeitos_por_servico | 0.6667 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Billing, Financial Management | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Billing, Financial Management | Billing -> Financial Management; Financial Management -> Billing |
| D11-001 | D11 | media | Administration and Configuration | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-002 | D11 | media | Billing | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-003 | D11 | media | CRM and Proposals | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-004 | D11 | media | Financial Management | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-005 | D11 | media | Identity and Access | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-006 | D11 | media | Project and Work Tracking | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-007 | D11 | media | Workforce Management | 1 endpoint(s) para 3 responsabilidade(s) |

## Avisos

- 12 non-bullet lines ignored in requirements

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
