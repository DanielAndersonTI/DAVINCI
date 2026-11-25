# Laudo VIA — TNTConcept

**Modelo:** Gemini  
**Configuracao:** C0  
**Rodada:** 1  
**Execucao:** `20260903_205150_127417`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 45 |
| Servicos | 12 |
| Arestas | 27 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2188 | calculado |
| endpoints_por_responsabilidade | 0.7500 | calculado |
| estabilidade_jaccard_servicos | 0.7802 | calculado |
| estabilidade_jaccard_arestas | 0.4161 | calculado |
| taxa_defeitos_por_servico | 0.5833 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D05-001 | D05 | alta | Administration Service, contract types | nome nao resolvido: contract types |
| D05-002 | D05 | alta | Billing Service, taxes | nome nao resolvido: taxes |
| D05-003 | D05 | alta | CRM and Proposals Service, contacts | nome nao resolvido: contacts |
| D05-004 | D05 | alta | Financial Management Service, entries | nome nao resolvido: entries |
| D05-005 | D05 | alta | Identity and Access Service, contractual | nome nao resolvido: contractual |
| D11-001 | D11 | media | Project and Work Tracking Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Avisos

- 12 non-bullet lines ignored in requirements

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
