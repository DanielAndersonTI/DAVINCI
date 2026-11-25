# Laudo VIA — PetClinic

**Modelo:** Claude  
**Configuracao:** C2  
**Rodada:** 1  
**Execucao:** `20260916_235707_633926`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 52 |
| Servicos | 4 |
| Arestas | 4 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2500 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.1071 | calculado |
| endpoints_por_responsabilidade | 0.1429 | calculado |
| estabilidade_jaccard_servicos | 0.5000 | calculado |
| estabilidade_jaccard_arestas | 0.5000 | calculado |
| taxa_defeitos_por_servico | 1.5000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Veterinarian Management, Visit Management | componente fortemente conexa com 2 servicos |
| D04-002 | D04 | alta | Veterinarian Management, Visit Management | Veterinarian Management -> Visit Management; Visit Management -> Veterinarian Management |
| D11-001 | D11 | media | Owner Management | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-002 | D11 | media | Pet Management | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-003 | D11 | media | Veterinarian Management | 1 endpoint(s) para 9 responsabilidade(s) |
| D11-004 | D11 | media | Visit Management | 1 endpoint(s) para 7 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
