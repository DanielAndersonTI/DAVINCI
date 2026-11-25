# Verificação do quick-check VIA v1

Data: 24/11/2026. Versão do VIA: 1.0.0.
Escopo: 356 artefatos do corpus DAVINCI, sem novas chamadas de LLM.

## 1. Comandos executados

Todos os comandos partem de `VIA/`.

```powershell
python -m via manifest --data ..\Report-and-Dates\Quantitative-Analysis-Updated\data.csv --result ..\result --manifest data\manifest.csv --mapping data\mapping_fixes.csv --lock data\corpus_v1.json

python -m via quick-check --manifest data\manifest.csv --inputs ..\Experimento_Multiagente\Dates\davinci_inputs --out reports\quick-check-v1\verdicts --resumo reports\quick-check-v1\summary.csv --d07-mode not_applicable --generated-at 2026-11-24T00:00:00+00:00

python -m via report --resumo reports\quick-check-v1\summary.csv --data ..\Report-and-Dates\Quantitative-Analysis-Updated\data.csv --out reports\quick-check-v1 --n-boot 5000

python scripts\d11_profile.py
```

O carimbo fixo em `--generated-at` elimina a única fonte de variação entre duas execuções do quick-check. A data não entra em nenhuma métrica.

## 2. Corpus

| Item | Valor |
|---|---|
| Linhas em `data.csv` | 360 |
| Artefatos com laudo | 356 |
| Excluídos | 4 |
| Sistemas | 8 |
| Modelos | 3 |
| Configurações | 5 |
| Células sistema × modelo × configuração | 120 |
| Execuções por célula | 3, salvo Claude/C4 com 2 em quatro sistemas |

Hash do `data.csv`:

```text
c3252deae86c79fa6476e93bf5aed4f66b2db768b70a3361b117090c2faae90c
```

Hash do manifesto:

```text
a07dad2492d8889eb3b56fa93f5c51ab7ce3ca3dce948ccd7205fd61ba8c107a
```

Composição por modelo: Claude 116, DeepSeek 120, Gemini 120.
Composição por configuração: C0 72, C1 72, C2 72, C3 72, C4 68.

## 3. Exclusões

Nenhum arquivo foi apagado, movido ou reescrito. A exclusão é uma linha com `status=excluded` no manifesto. Os quatro artefatos têm `services:` vazio.

| Sistema | Modelo | Config | Execução | Motivo | SHA-256 do YAML |
|---|---|---|---|---|---|
| Jokul | Claude | C4 | 3 | lista de serviços vazia | `bb524dc30fe15dd85bafed3e18c3b96fe7ea113a67dd5986e704ad4517dd9efe` |
| JPetStore | Claude | C4 | 3 | lista de serviços vazia | `0b2b1c16770c7d4e3e73e6ae1f4845395327218fc0ae6c2a8cad0e7819abbbd0` |
| PetClinic | Claude | C4 | 3 | lista de serviços vazia | `2fba0215962bf5c734275d06d68179e4561e8cbabccf985c9a7cfa12d3f44e2f` |
| TNTConcept | Claude | C4 | 3 | lista de serviços vazia | `543340b9a4d4045fd5e8bb7028e47041cd9c3838a3e8587e86702540844342fe` |

## 4. Reparos de mapeamento

O `data.csv` traz ids de execução duplicados em Claude/C2 e deslocados em Claude/C4. Os três diretórios de cada célula existem em `result/` e foram ordenados pelo carimbo temporal do nome do diretório. O F1 do `sumario.json` foi usado como conferência.

| Método | Linhas | O que faz |
|---|---|---|
| `original_id` | 309 | id do CSV resolve direto no diretório |
| `claude_c2_chronological` | 24 | ordena os três diretórios de Claude/C2 por timestamp |
| `claude_c4_chronological` | 24 | ordena os três diretórios de Claude/C4 por timestamp |
| `global_id_fallback` | 3 | id único encontrado em `result/7ed`, erro de nome de pasta do experimento anterior |

O arquivo `data/mapping_fixes.csv` registra cada reparo, o id original, o id resolvido e o F1 dos dois lados.

## 5. Status das regras

| Código | Regra | Status nesta rodada |
|---|---|---|
| D03 | serviço isolado | automática |
| D04 | componente fortemente conexa | automática; subtipo `ciclo2` registrado à parte |
| D05 | endpoint ou dependência não resolvida | automática |
| D06 | auto-dependência | automática |
| D07 | divergência entre dependências e interações | `not_applicable`: a serialização do corpus grava as duas listas iguais |
| D10 | granularidade | descritiva, não é achado |
| D11 | interface subespecificada: menos de 0,5 endpoint por responsabilidade | automática |
| D12 | ausência lexical de termo de autenticação | automática, heurística |

D07 não entra no cálculo de taxa de defeitos nesta rodada. O `laudo` registra `d07_status=not_applicable` e omite a métrica de consistência interna.

## 6. Testes

```text
python -m pytest -q
41 passed, 1 warning
```

O aviso vem do plugin `anyio` do pytest, não do VIA.

Cobertura atual:

- carregamento dos esquemas em inglês e português;
- descarte de dependências vazias;
- normalização de nomes e fusão de duplicatas;
- requisitos apenas em linhas com marcador;
- D03, D04 com subtipo, D05, D06, D07, D11 e D12;
- fronteiras de D11: razão exatamente 0,5 não aciona, razão abaixo de 0,5 aciona, serviço sem endpoint aciona;
- métricas, Gini, Jaccard, Spearman e bootstrap;
- manifesto com ids duplicados e YAML vazio;
- determinismo do laudo, com `gerado_em` como único campo variável.

## 7. Ambiente

| Componente | Versão |
|---|---|
| Python | 3.12.0 |
| PyYAML | 6.0.3 |
| NetworkX | 3.6.1 |
| NumPy | 2.4.4 |
| SciPy | 1.17.1 |
| Matplotlib | 3.10.9 |
| pytest | 9.2.0 |

## 8. Saídas

| Caminho | Conteúdo |
|---|---|
| `reports/quick-check-v1/verdicts/` | 356 laudos JSON e 356 Markdown |
| `reports/quick-check-v1/summary.csv` | uma linha por artefato |
| `reports/quick-check-v1/d11_profile.csv` | pares endpoint × responsabilidade dos 1.977 achados D11 |
| `reports/quick-check-v1/prevalence.csv` | prevalência por código |
| `reports/quick-check-v1/by_model.csv` | médias por modelo |
| `reports/quick-check-v1/by_config.csv` | médias por configuração |
| `reports/quick-check-v1/by_system.csv` | médias por sistema |
| `reports/quick-check-v1/by_cell.csv` | médias por sistema × modelo × configuração |
| `reports/quick-check-v1/correlations.csv` | Spearman por sistema e por métrica |
| `reports/quick-check-v1/pooled_correlations.csv` | bootstrap agrupado por sistema |
| `reports/quick-check-v1/contrasts.csv` | H1, H2 e H3 com Holm |
| `reports/quick-check-v1/exploratory_contrasts.csv` | E1 a E8, p bruto |
| `reports/quick-check-v1/figures/` | quatro figuras PNG a 200 dpi |
| `reports/quick-check-v1/tables.md` | tabelas em Markdown |
| `reports/quick-check-v1/overview.json` | composição do corpus analisado |
| `data/requirements/` | um JSONL por sistema e `_summary.csv` com contagem e hash |

## 9. Limites declarados

1. As regras automáticas são proxies. A validade de constructo ainda não foi medida contra adjudicação humana.
2. D11 é quase saturada: 353 de 356 artefatos têm ao menos um serviço com interface subespecificada. Em 1.947 dos 1.977 achados o serviço declara um único endpoint para várias responsabilidades; nenhum achado tem serviço sem endpoint. A taxa de defeitos completa é dominada por D11; por isso a análise estrutural usa D03 a D06 por serviço.
3. D12 é higiene lexical, não segurança. A presença de um termo de autenticação não prova que o mecanismo exista.
4. O corpus tem oito sistemas e 120 células. O bootstrap por sistema é descritivo, não inferência sobre uma população de sistemas.
5. Os contrastes E1 a E8 foram calculados depois da inspeção dos resultados. Não são pré-registrados e não sustentam confirmação confirmatória.
6. Não houve nova execução de LLM. O estudo reanalisa artefatos já produzidos.

## 10. Segurança

Nenhuma chave de API foi lida, gravada, impressa ou incluída nos laudos, tabelas, figuras ou neste documento. A análise usa apenas arquivos do corpus e o `data.csv`.
