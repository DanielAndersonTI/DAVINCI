# Laudo VIA — Cargo-Tracker

**Modelo:** DeepSeek  
**Configuracao:** C4  
**Rodada:** 1  
**Execucao:** `20260923_212027_699234`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 71 |
| Servicos | 5 |
| Arestas | 12 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.0930 | calculado |
| endpoints_por_responsabilidade | 0.1163 | calculado |
| estabilidade_jaccard_servicos | 0.8333 | calculado |
| estabilidade_jaccard_arestas | 0.5899 | calculado |
| taxa_defeitos_por_servico | 1.4000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Cargo Management, Cargo Tracking, Logistics Event Registration, Route Planning | componente fortemente conexa com 4 servicos |
| D04-002 | D04 | alta | Cargo Management, Logistics Event Registration | Cargo Management -> Logistics Event Registration; Logistics Event Registration -> Cargo Management |
| D04-003 | D04 | alta | Cargo Management, Route Planning | Cargo Management -> Route Planning; Route Planning -> Cargo Management |
| D04-004 | D04 | alta | Cargo Tracking, Logistics Event Registration | Cargo Tracking -> Logistics Event Registration; Logistics Event Registration -> Cargo Tracking |
| D04-005 | D04 | alta | Logistics Event Registration, Route Planning | Logistics Event Registration -> Route Planning; Route Planning -> Logistics Event Registration |
| D11-001 | D11 | media | Cargo Management | 1 endpoint(s) para 10 responsabilidade(s) |
| D11-002 | D11 | media | Cargo Tracking | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-003 | D11 | media | Integration | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-004 | D11 | media | Logistics Event Registration | 1 endpoint(s) para 10 responsabilidade(s) |
| D11-005 | D11 | media | Route Planning | 1 endpoint(s) para 8 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
