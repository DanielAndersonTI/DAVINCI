# Laudo VIA — PetClinic

**Modelo:** DeepSeek  
**Configuracao:** C0  
**Rodada:** 3  
**Execucao:** `20260909_001737_139594`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 52 |
| Servicos | 4 |
| Arestas | 8 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2500 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.0682 | calculado |
| endpoints_por_responsabilidade | 0.1818 | calculado |
| estabilidade_jaccard_servicos | 1.0000 | calculado |
| estabilidade_jaccard_arestas | 1.0000 | calculado |
| taxa_defeitos_por_servico | 1.5000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Animal Management Service, Owner Management Service, Veterinarian Management Service, Visit Management Service | componente fortemente conexa com 4 servicos |
| D04-002 | D04 | alta | Animal Management Service, Owner Management Service | Animal Management Service -> Owner Management Service; Owner Management Service -> Animal Management Service |
| D04-003 | D04 | alta | Animal Management Service, Visit Management Service | Animal Management Service -> Visit Management Service; Visit Management Service -> Animal Management Service |
| D04-004 | D04 | alta | Owner Management Service, Visit Management Service | Owner Management Service -> Visit Management Service; Visit Management Service -> Owner Management Service |
| D04-005 | D04 | alta | Veterinarian Management Service, Visit Management Service | Veterinarian Management Service -> Visit Management Service; Visit Management Service -> Veterinarian Management Service |
| D11-001 | D11 | media | Animal Management Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-002 | D11 | media | Owner Management Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D11-003 | D11 | media | Veterinarian Management Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-004 | D11 | media | Visit Management Service | 1 endpoint(s) para 5 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
