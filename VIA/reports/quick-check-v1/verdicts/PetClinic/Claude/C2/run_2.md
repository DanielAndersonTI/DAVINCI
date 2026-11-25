# Laudo VIA — PetClinic

**Modelo:** Claude  
**Configuracao:** C2  
**Rodada:** 2  
**Execucao:** `20260917_000952_753255`

## Entrada

| Item | Valor |
|---|---:|
| Requisitos | 52 |
| Servicos | 4 |
| Arestas | 7 |
| Schema | en |

## Metricas

| Metrica | Valor | Status |
|---|---:|---|
| cobertura_requisitos | n/d | semiautomatico_nao_executado |
| precisao_servicos | n/d | semiautomatico_nao_executado |
| densidade_ciclos | 0.2500 | calculado |
| consistencia_interna | n/d | d07_nao_aplicavel |
| conflitos_de_posse | n/d | semiautomatico_nao_executado |
| gini_granularidade | 0.0536 | calculado |
| endpoints_por_responsabilidade | 0.1429 | calculado |
| estabilidade_jaccard_servicos | 0.0000 | calculado |
| estabilidade_jaccard_arestas | 0.0000 | calculado |
| taxa_defeitos_por_servico | 1.5000 | calculado |

## Achados

| ID | Codigo | Severidade | Elementos | Evidencia |
|---|---|---|---|---|
| D04-001 | D04 | alta | Animal Service, Owner Service, Veterinarian Service, Visit Service | componente fortemente conexa com 4 servicos |
| D04-002 | D04 | alta | Animal Service, Owner Service | Animal Service -> Owner Service; Owner Service -> Animal Service |
| D04-003 | D04 | alta | Animal Service, Visit Service | Animal Service -> Visit Service; Visit Service -> Animal Service |
| D04-004 | D04 | alta | Veterinarian Service, Visit Service | Veterinarian Service -> Visit Service; Visit Service -> Veterinarian Service |
| D11-001 | D11 | media | Animal Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D11-002 | D11 | media | Owner Service | 1 endpoint(s) para 6 responsabilidade(s) |
| D11-003 | D11 | media | Veterinarian Service | 1 endpoint(s) para 8 responsabilidade(s) |
| D11-004 | D11 | media | Visit Service | 1 endpoint(s) para 7 responsabilidade(s) |
| D12-001 | D12 | baixa | artefato inteiro | nenhuma mencao a autenticacao ou autorizacao no artefato |

## Notas

- D07: not_applicable.
- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.
- O VIA mede integridade interna, nao qualidade global da arquitetura.
