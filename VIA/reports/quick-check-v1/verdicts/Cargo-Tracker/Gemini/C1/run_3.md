# Laudo VIA — Cargo-Tracker

**Modelo:** Gemini  
**Configuracao:** C1  
**Rodada:** 3  
**Execucao:** `20260903_171811_012917`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 71 |
| Servicos | 8 |
| Arestas | 12 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.1250 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.2446 | calculado |
| endpoints_por_responsabilidade | 0.3478 | calculado |
| estabilidade_jaccard_servicos | 0.5347 | calculado |
| estabilidade_jaccard_arestas | 0.5066 | calculado |
| taxa_defeitos_por_servico | 1.2500 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Cargo Management Service, Route Planning Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Cargo Management Service, Route Planning Service | Cargo Management Service -> Route Planning Service; Route Planning Service -> Cargo Management Service |
| D05-001 | D05 | alta | Architecture A and Architecture B have identical Service metrics (Precision=1.0000, F1=0.9091). | nome nao resolvido: F1=0.9091). |
| D05-002 | D05 | alta | Architecture B has significantly higher Interaction metrics (Precision=1.0000, F1=0.8421) compared to Architecture A (Precision=0.3333 | nome nao resolvido: F1=0.8421) compared to Architecture A (Precision=0.3333 |
| D05-003 | D05 | alta | Output must be raw CSV with no markdown or extra text.Microservice, Communicates With | nome nao resolvido: Communicates With |
| D11-001 | D11 | media | Cargo Management Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-002 | D11 | media | Cargo Tracking Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-003 | D11 | media | Integration Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-004 | D11 | media | Logistics Event Registration Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D11-005 | D11 | media | Route Planning Service | 1 endpoint(s) para 4 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
