# Laudo VIA — AcmeAir

**Modelo:** Gemini  
**Configuracao:** C3  
**Rodada:** 1  
**Execucao:** `20260908_092510_221371`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 61 |
| Servicos | 6 |
| Arestas | 6 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.0000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2368 | calculado |
| endpoints_por_responsabilidade | 0.3158 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.4000 | calculado |
| taxa_defeitos_por_servico | 1.0000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D05-001 | D05 | alta | Environment Administration Service, customers | nome nao resolvido: customers |
| D05-002 | D05 | alta | Flight Search Service, destination | nome nao resolvido: destination |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-002 | D11 | media | Booking Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-003 | D11 | media | Customer Profile Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-004 | D11 | media | Loyalty Service | 1 endpoint(s) para 3 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
