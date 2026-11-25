# VIA — Verificador de Integridade Arquitetural

Verificador determinístico de decomposições monolito → microserviços. Lê o YAML final produzido pelo DAVINCI, constrói o grafo de serviços e aplica regras automáticas. Nenhuma chamada de LLM participa das regras.

Versão: 1.0.0. Corpus: 356 artefatos, 8 sistemas, 3 modelos, 5 configurações. Testes: 41.

## Estrutura

```text
VIA/
├── via/                    código do verificador
│   ├── io/loader.py        leitura canônica dos dois esquemas YAML
│   ├── io/manifest.py      manifesto, reparos de id e trava do corpus
│   ├── graph.py            grafo dirigido, graus, SCC, pares mútuos
│   ├── rules/automatic.py  D03 a D07, D11 e D12
│   ├── metrics.py          Gini, Jaccard, Spearman, bootstrap
│   ├── report.py           laudo JSON e Markdown
│   ├── analysis.py         tabelas, correlações e contrastes
│   ├── figures.py          quatro figuras PNG
│   └── cli.py              linha de comando
├── tests/                  41 testes
├── data/                   manifesto, reparos e trava do corpus
├── reports/                verificação, laudos e saídas da análise
└── scripts/                make_slides.py, d11_profile.py, build_requirements.py
```

## Comandos

Executar a partir de `VIA/`.

### 1. Manifesto e trava do corpus

```powershell
python -m via manifest `
  --data ..\Report-and-Dates\Quantitative-Analysis-Updated\data.csv `
  --result ..\result `
  --manifest data\manifest.csv `
  --mapping data\mapping_fixes.csv `
  --lock data\corpus_v1.json
```

### 2. Laudos

```powershell
python -m via quick-check `
  --manifest data\manifest.csv `
  --inputs ..\Experimento_Multiagente\Dates\davinci_inputs `
  --out reports\quick-check-v1\verdicts `
  --resumo reports\quick-check-v1\summary.csv `
  --d07-mode not_applicable `
  --generated-at 2026-11-24T00:00:00+00:00
```

### 3. Tabelas e figuras

```powershell
python -m via report `
  --resumo reports\quick-check-v1\summary.csv `
  --data ..\Report-and-Dates\Quantitative-Analysis-Updated\data.csv `
  --out reports\quick-check-v1 `
  --n-boot 5000
```

### 4. Slides

```powershell
python scripts\make_slides.py
```

### 5. Testes

```powershell
python -m pytest -q
```

## Saídas principais

| Caminho | Conteúdo |
|---|---|
| `reports/quick-check-v1/verification.md` | comandos, hashes, versões e limites |
| `reports/quick-check-v1/summary.csv` | uma linha por artefato |
| `reports/quick-check-v1/prevalence.csv` | prevalência por código |
| `reports/quick-check-v1/verdicts/` | 356 laudos JSON e 356 Markdown |
| `reports/quick-check-v1/figures/` | quatro figuras a 200 dpi |

A nota técnica, os slides e os documentos de trabalho são mantidos fora deste repositório, conforme o `.gitignore`.

## Regras

| Código | O que detecta | Status |
|---|---|---|
| D03 | serviço isolado | automática |
| D04 | componente fortemente conexa | automática |
| D05 | referência que não resolve | automática |
| D06 | auto-dependência | automática |
| D07 | divergência entre dependências e interações | não aplicável no corpus |
| D10 | granularidade | descritiva |
| D11 | interface subespecificada: menos de 0,5 endpoint por responsabilidade | automática |
| D12 | ausência lexical de termo de autenticação | automática, heurística |

## Limites

As regras são proxies de integridade. D11 mede densidade de endpoints por responsabilidade, não endpoint errado. D12 é higiene lexical, não segurança. A validação humana e o alpha entre anotadores ainda não foram feitos. O corpus tem oito sistemas e não sustenta generalização.

## Segurança

Nenhuma chave de API é lida, gravada ou incluída em laudos, tabelas, figuras ou relatórios. A análise usa apenas o corpus e o `data.csv`.
