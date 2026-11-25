# Laudo VIA — AcmeAir

**Modelo:** DeepSeek  
**Configuracao:** C0  
**Rodada:** 1  
**Execucao:** `20260909_000024_135959`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 61 |
| Servicos | 6 |
| Arestas | 12 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1667 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.3533 | calculado |
| endpoints_por_responsabilidade | 0.2400 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.4393 | calculado |
| taxa_defeitos_por_servico | 1.3333 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Authentication Service, Booking Service, Loyalty Service | componente fortemente conexa com 3 servicos |
| D04-002 | D04 | alta | Authentication Service, Booking Service | Authentication Service -> Booking Service; Booking Service -> Authentication Service |
| D04-003 | D04 | alta | Authentication Service, Loyalty Service | Authentication Service -> Loyalty Service; Loyalty Service -> Authentication Service |
| D05-001 | D05 | alta | Customer Profile Service, phone type | nome nao resolvido: phone type |
| D05-002 | D05 | alta | Environment Administration Service, customers | nome nao resolvido: customers |
| D05-003 | D05 | alta | Flight Search Service, destination airport | nome nao resolvido: destination airport |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-002 | D11 | media | Booking Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-003 | D11 | media | Environment Administration Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-004 | D11 | media | Loyalty Service | 1 endpoint(s) para 4 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
