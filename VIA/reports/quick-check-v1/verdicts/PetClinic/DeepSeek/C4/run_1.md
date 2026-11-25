# Laudo VIA — PetClinic

**Modelo:** DeepSeek  
**Configuracao:** C4  
**Rodada:** 1  
**Execucao:** `20260923_212143_382200`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 52 |
| Servicos | 5 |
| Arestas | 9 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.4000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.0780 | calculado |
| endpoints_por_responsabilidade | 0.1220 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 0.8889 | calculado |
| taxa_defeitos_por_servico | 1.6000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Animal Service, Owner Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Veterinarian Service, Visit Service | componente fortemente conexa com 2 servicos |
| D04-003 | D04 | alta | Animal Service, Owner Service | Animal Service -> Owner Service; Owner Service -> Animal Service |
| D04-004 | D04 | alta | Veterinarian Service, Visit Service | Veterinarian Service -> Visit Service; Visit Service -> Veterinarian Service |
| D11-001 | D11 | media | Animal Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-002 | D11 | media | Interface Service | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-003 | D11 | media | Owner Service | 1 endpoint(s) para 10 responsabilidade(s) |
| D11-004 | D11 | media | Veterinarian Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-005 | D11 | media | Visit Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
