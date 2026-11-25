# Laudo VIA — JPetStore

**Modelo:** Gemini  
**Configuracao:** C3  
**Rodada:** 2  
**Execucao:** `20260908_095804_871969`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 77 |
| Servicos | 6 |
| Arestas | 6 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1667 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1667 | calculado |
| endpoints_por_responsabilidade | 0.3333 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.3636 | calculado |
| taxa_defeitos_por_servico | 1.5000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D03-001 | D03 | baixa | Authentication Service | grau de entrada 0 e grau de saida 0 |
| D04-001 | D04 | alta | Catalog Service, Inventory Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Catalog Service, Inventory Service | Catalog Service -> Inventory Service; Inventory Service -> Catalog Service |
| D05-001 | D05 | alta | Customer Account Service, contact | nome nao resolvido: contact |
| D05-002 | D05 | alta | Order Service, delivery addresses | nome nao resolvido: delivery addresses |
| D11-001 | D11 | media | Authentication Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-002 | D11 | media | Catalog Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-003 | D11 | media | Inventory Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-004 | D11 | media | Order Service | 1 endpoint(s) para 3 responsabilidade(s) |
| D11-005 | D11 | media | Shopping Cart Service | 1 endpoint(s) para 4 responsabilidade(s) |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
