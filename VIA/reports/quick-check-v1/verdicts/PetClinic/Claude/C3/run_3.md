# Laudo VIA — PetClinic

**Modelo:** Claude  
**Configuracao:** C3  
**Rodada:** 3  
**Execucao:** `20260919_003550_005918`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 52 |
| Servicos | 5 |
| Arestas | 8 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2000 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.0941 | calculado |
| endpoints_por_responsabilidade | 0.1471 | calculado |
| estabilidade_jaccard_servicos | 0.9000 | calculado |
| estabilidade_jaccard_arestas | 0.6944 | calculado |
| taxa_defeitos_por_servico | 1.4000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Veterinarian Service, Visit Service | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Veterinarian Service, Visit Service | Veterinarian Service -> Visit Service; Visit Service -> Veterinarian Service |
| D11-001 | D11 | media | Animal Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-002 | D11 | media | Owner Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | UI Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-004 | D11 | media | Veterinarian Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-005 | D11 | media | Visit Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
