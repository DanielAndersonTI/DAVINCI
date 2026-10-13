# Depósito Zenodo — DA VINCI
## Árvore real do conteúdo a enviar + texto de assimilação

**Título do depósito:** *DA VINCI — Service Boundaries and Interaction Recovery in Agentic Microservice Design: A Configuration Study*
**Raiz local (pasta a zipar):** `Zenodo-DAVINCI-Service-Boundaries-and-Interaction-Recovery-in-Agentic-Microservice-Design-A- Configuration-Study\`
**Verificação:** enumeração recursiva + MD5 das duplicatas em 28/09/2026.
**Total:** **5.472 arquivos · 249.820.953 bytes (238,2 MiB) · 4 pastas de 1º nível + 2 arquivos soltos.**

> Este documento descreve o depósito **por conteúdo**, não por nome de arquivo. Muitos itens
> pedidos em checklists existem com outro nome ou em outro lugar; outros nunca existiram e a
> razão está declarada. Nenhuma linha foi inventada: tudo foi lido da árvore real.

---

## 1. Árvore

```
Zenodo-DAVINCI-...-Study/                   5.472 arq · 238,2 MiB
│
├── README.md                                            21,0 KB  ✔ documentação do artefato
├── LICENSE- Deed - Attribution 4.0 International ...pdf 125.681 B ✔ CC BY 4.0
│
├── Report-and-Dates/                       247 arq · 111,6 MiB  ✔ NÚCLEO (resultados do artigo)
│   ├── DAVINCI-Consolidated-Report.md      254,3 KB · 3.152 linhas  ✔ §1–§7 + Apêndices A–B
│   ├── Requirements/                        26 arq · 449,0 KB      ✔ (S1)
│   │   ├── Development-of-requirements.txt              (5,7 KB)   ← como os requisitos foram construídos
│   │   ├── Original-Requirements_PT.xlsx                (399,6 KB) ← proveniência (originais em PT)
│   │   └── Requirements-used-as-input/<sistema>/{requirements,reference_services,reference_interactions}.txt
│   │       8 sistemas: 7ep · acmeair · cargo-tracker · daytrader7 · jokul · jpetstore · pet-clinic · TNTConcept
│   ├── Prompts-used-in-the-agents/            6 arq · 125,4 KB     ✔ (S2) — os prompts exatos
│   │   Agent-1 (11,0) · Agent-2 (72,9) · Agent-2_1 (13,2) · Agent-3 (11,3) · Agent-4 (9,6) · Agent-5 (7,5)
│   ├── Qualitative-Analysis/                  2 arq · 25,2 KB     ✔ (S5) — DADOS HUMANOS
│   │   ├── Qualitative-Evaluation-Protocol.txt          (12.197 B) ← metodologia (critérios, escala 1–5)
│   │   └── Answer-sheet(Answers).xlsx                   (13.563 B) ← 12 respondentes anônimos
│   │         48 colunas = 4 (perfil) + 3 sistemas × 14 (A1: 5 critérios + comentário; A2: idem;
│   │         preferência; justificativa) + 2 (pergunta global / comentário adicional)
│   │         Sem nome, sem e-mail (anonimato preservado)
│   ├── Quantitative-Analysis/                11 arq · 1.399,4 KB   ✔ (S6) pipeline CONGELADO (C0–C3, 5 sistemas)
│   │   data.csv (9,7 KB) · descriptive.csv · wilcoxon.csv · spearman.csv
│   │   report.md (23,0 KB) · report.html (810,4 KB — preview regenerável)
│   │   figures/{boxplot_interactions, boxplot_services, scatter_tokens_vs_f1,
│   │            violin_interactions, violin_services}.png
│   └── Quantitative-Analysis-Updated/        38 arq · 4.395,6 KB   ✔ (S3 + S6) pipeline ESTENDIDO (corpus completo)
│       ├── data.csv                    50,2 KB · 361 linhas (cabeçalho + 360 observações)
│       │      ← TABELA CANÔNICA DE EXECUÇÕES = o "run table" pedido
│       │         (execution_id, tokens, duration_ms, total_calls, prompt/completion tokens,
│       │          f1_serv, f1_inter, yaml_valid, modelo, configuração, rodada, sistema)
│       ├── source_all_data.csv         46,7 KB · 361 linhas ← extração bruta dos artefatos
│       ├── cost.csv · descriptive.csv · wilcoxon.csv · spearman.csv · per_system.csv
│       ├── precision_recall.csv · yaml.csv · ranking.csv · proposals_c4.csv · results.json (58,4 KB)
│       ├── report.md (77,9 KB) · report.html (2.358,1 KB — preview regenerável)
│       ├── scripts: generate_report.py (123,7) · cost_report.py (29,3) · plots.py (19,3) ·
│       │            paired_tests.py · descriptive_stats.py · correlation.py · prepare_data.py ·
│       │            render_report_html.py · verify_report.py (checagem de integridade) ·
│       │            run_all.py · _paths.py · _source_scan.py
│       ├── README.md (3,6 KB) ← ordem de execução, seed fixo, bootstrap, o que cada arquivo é
│       └── figures/  (11 PNG, 300 dpi)
│   ├── Claude/                               54 arq · 35,5 MiB     ✔ corpus de saída (C0–C4 × 3 rodadas)
│   │   C0..C4/  Cx-Claude-Synthesize-two-three-tests.txt + Synthesize-two-three-tests.txt (cópia idêntica)
│   │   C0..C4/Test-{1,2,3}/
│   │        FS-Complete-Claude-<n>-Metrics.pdf  (~1,21 MiB) ← MÉTRICAS + YAML validado (artifact of record)
│   │        FS-Complete-Claude-<n>-YALM.pdf     (~1,17 MiB) ← diagrama da arquitetura proposta
│   │        execuion-metadados-<Cx>-Claude-FS<n>.json        ← custo/tokens/tempo (grafia mantida de propósito)
│   ├── Gemini/                               55 arq · 36,2 MiB     ✔ (C2/Test-1 tem 3 PDF: um YALM duplicado)
│   └── DeepSeek/                             54 arq · 33,3 MiB     ✔ (C3/Test-1 tem TXT em vez de PDF, 39,8 KB)
│
└── Multi-agent-Experiments/                  912 arq · 116,3 MiB   ✔ pipeline + entradas + evidência estática
    ├── main_fewshot.py                                 60,3 KB     ← entry point do experimento
    ├── execution_tracker.py                             9,2 KB     ← importado por main_fewshot.py (mantido)
    ├── requirements.txt                                 0,3 KB     ← ambiente fixado
    ├── agentes/                              17 arq · 183,2 KB     ✔
    │   agent1_architect_a_fs.py · agent2_architect_b_fs.py · agent2_1architect_b_fs.py (C4) ·
    │   agent3_validator_fs.py · agent4_refiner_fs.py · agent5_architectural_spec_fs.py · __init__.py
    │   zero-shot-agents/ (3) ~  ·  __pycache__/ (7) ~
    ├── quantitative_analysis/                15 arq · 102,3 KB     ✔ scripts do pipeline congelado
    │   run_all.py · inspect_sources.py · cache_texts.py · extract_data.py · descriptive_stats.py
    │   paired_tests.py · correlation.py · plots.py · generate_report.py · render_report_html.py
    │   _paths.py · _source_scan.py (13,7 KB) · README.md (3,6 KB) · .gitignore · __pycache__/ ~
    ├── .txt/                                 14 arq · 117,9 KB     ✔ notas de método (PT/EN)
    │   Static_Analysis_Methodology.txt (30,7) ← citado como autoritativo pelo Dates/README.md
    │   Levantamento-de-Requisitos.txt (7,5) · Protocolo.txt (8,3) · Qualitative-Analysis.txt (3,7)
    │   SYSTEM_OPERATION.md.txt (2,9) · Tokens-price.txt (0,1)
    │   8× Synthesize-two-three-tests-C{0..3}-{Gemini,Deepseek}.txt
    ├── .md/                       VAZIA (notas internas removidas) ✖
    ├── Dots/                      VAZIA (diagramas .dot removidos) ✖
    └── Dates/                               862 arq · 115,7 MiB
        ├── README.md                                   21,9 KB     ✔ inventário do corpus + Known Inconsistencies
        ├── davinci_inputs/                  33 arq                 ✔ entrada canônica dos agentes
        │   <sistema>/{requirements.txt, reference_services.txt, reference_interactions.txt,
        │              name_normalization_map.txt} + README.md      (8 sistemas × 4 + README)
        ├── ground true/                      8 arq                ✔ ground truth por sistema
        │   <sistema>/reference_microservices_architecture_<sistema>.csv
        ├── static-analysis-systems/         51 arq · 672,2 KB      ✔ evidência estática (entrada dos prompts)
        │   <sistema>/{classes, entrypoints, modules, package_dependencies, package_metrics}.csv
        │   + summary.json  ·  index.json (59,9 KB) · manifest.json · project_summaries.csv
        ├── static analysis/                 97 arq · ~8,3 MiB      ~/✖
        │   analyze_systems.py (30,9 KB) · README.md (2,0 KB, PT-BR, obsoleto)
        │   SootUp/ (95 arq — clone vendorizado, não invocado)
        └── systems/                        672 arq · 106,7 MiB     ✖ código-fonte de terceiros (1 licença por projeto)

    (Fora de `Multi-agent-Experiments`, mas na mesma raiz:)
    ├── Interface/                       52 arq · 1,27 MiB          ✖ app web da ferramenta (server.py, static/,
    │                                                               utils/, tests/ 9, tasks/ 10, spec/ 2,
    │                                                               .specify/ 20, img/ 1)
    └── result/                        4.259 arq · 8,91 MiB         ✖ saídas locais de execução
        7ed · 7ep · acmeair · bookstore · cargo tracker · cargo-tracker · daytrader7 · ed · jokul ·
        jpetstore · pet-clinic · petclinic  +  80 pastas results-tracer-*/ (tracing da Interface)

Legenda: ✔ = contém informação citada pelo artigo   ~ = redundante/regenerável (pode ficar)
        ✖ = fora do escopo científico (candidato a exclusão antes do zip; nada do artigo depende disso)
```

---

## 2. Texto de assimilação (leia antes de pedir qualquer arquivo)

**O que é este depósito.** O material de um experimento controlado de geração de arquiteturas
de microsserviços por pipelines multiagentes: **3 modelos × 5 configurações (C0–C4) × 3 rodadas =
45 execuções**, cada execução cobrindo os **8 sistemas de referência** (45 × 8 = **360
observações**). Cada execução deixou três artefatos: o PDF de métricas (que contém também o YAML
validado), o PDF do diagrama da arquitetura e o JSON de metadados (tokens, tempo, chamadas). Junto
com as saídas estão as
**entradas** (requisitos, serviços/interações de referência, evidência estática e ground truth),
o **processo** (prompts e código dos agentes), as **análises** (dois pipelines estatísticos que
leem os artefatos e produzem as tabelas e figuras), a **consolidação** (o relatório que reúne
tudo) e a **avaliação humana** (12 respondentes).

**O depósito não é organizado em “S1…S7”.** Essa é a estrutura proposta pelo checklist de revisão,
não a estrutura física do material. A organização real é por **papel**:

| Papel | Onde está |
|---|---|
| Entradas (S1) | `Report-and-Dates/Requirements/`, `Multi-agent-Experiments/Dates/{davinci_inputs, static-analysis-systems, ground true}/` |
| Processo (S2) | `Report-and-Dates/Prompts-used-in-the-agents/`, `Multi-agent-Experiments/{main_fewshot.py, agentes/}`, `README.md` |
| Saídas (S3) | `Report-and-Dates/{Claude, Gemini, DeepSeek}/<C0..C4>/Test-{1,2,3}/` |
| Análise (S6) | `Report-and-Dates/Quantitative-Analysis/` (congelado) e `Quantitative-Analysis-Updated/` (estendido) |
| Consolidação (S7) | `Report-and-Dates/DAVINCI-Consolidated-Report.md` (§1–§7 + Apêndices A–B) |
| Avaliação humana (S5) | `Report-and-Dates/Qualitative-Analysis/` |

**Regra de leitura obrigatória:** a informação existe **por conteúdo**, não por nome de arquivo.
Vários itens que o checklist pede por um nome específico existem com outro nome (a tabela da
seção 3 dá o mapa) e outros nunca existiram — e a razão está declarada (seções 4, 5 e 7).

## 3. Mapa “item pedido → onde está de fato”

| Item pedido pelo checklist | Onde está de fato | Situação |
|---|---|---|
| S1 · tabela dos sistemas (subjects) | não há um CSV único; os dados estão em `Requirements/Requirements-used-as-input/` (8×3), `Dates/davinci_inputs/` (8×4) e `Dates/ground true/` (8 CSV) | **presente**, fragmentado |
| S1 · requisitos que entraram nos prompts | `Requirements/Requirements-used-as-input/<sistema>/requirements.txt` (8 arquivos, EN) | **presente** |
| S1 · serviços e interações de referência | `.../reference_services.txt` + `.../reference_interactions.txt` (8+8) e `ground true/<sys>/reference_microservices_architecture_<sys>.csv` | **presente** |
| S1 · evidência estática | `Dates/static-analysis-systems/<sys>/` (5 CSV + `summary.json`), `index.json` (59,9 KB), `manifest.json`, `project_summaries.csv` | **presente** |
| S1 · como os requisitos foram derivados | `Requirements/Development-of-requirements.txt`, `Original-Requirements_PT.xlsx`, `.txt/Levantamento-de-Requisitos.txt` | **presente** |
| S1 · método da análise estática | `.txt/Static_Analysis_Methodology.txt` (30,7 KB) + `Dates/static analysis/analyze_systems.py` | **presente** |
| S2 · o que cada configuração (C0–C4) muda | `README.md` (seção de configurações) + `DAVINCI-Consolidated-Report.md` §2 + código `agentes/agent*_fs.py` | **presente** |
| S2 · configuração de execução (modelos, rodadas, temperatura) | `README.md` + §2–§3 do consolidado + `execuion-metadados-*.json` (modelo, tokens, tempo por execução) | **presente** |
| S2 · prompts exatos | `Prompts-used-in-the-agents/` → `Agent-1`, `Agent-2`, `Agent-2_1`, `Agent-3`, `Agent-4`, `Agent-5` | **presente** |
| S3 · tabela canônica de execuções (“run table”) | **`Quantitative-Analysis-Updated/data.csv`** — 361 linhas (cabeçalho + 360), chave `execution_id`, uma linha por (modelo, configuração, rodada, sistema) | **presente** (outro nome) |
| S3 · tabela bruta extraída dos artefatos | `source_all_data.csv` (361 linhas) + `proposals_c4.csv` + `yaml.csv` | **presente** |
| S3 · contagens e denominadores | `cost.csv` (`n_executions`, `n_budget`, `n_zero`), `per_system.csv`, `descriptive.csv` | **presente** |
| S3 · falhas e exclusões | §6 do consolidado (4 observações sem F1 em Claude/C4 rodada 3; 7 `execution_id` repetidos; 18 divergências PDF×TXT) + `C4-Claude-Synthesize-two-three-tests.txt` | **presente** (no relatório, não em arquivo próprio) |
| S4 · 5 análises de robustez | **não existem**; há apenas “sensitivity of the election” (§4.4 do `report.md` estendido) e as limitações (§6) | **ausente** (gap real — §7) |
| S5 · questionário aplicado | o instrumento são as **48 colunas** de `Answer-sheet(Answers).xlsx`; a metodologia é `Qualitative-Evaluation-Protocol.txt` | **presente** |
| S5 · respostas dos avaliadores | `Answer-sheet(Answers).xlsx`: 12 respondentes × 3 sistemas × 2 arquiteturas × 5 critérios + preferência + justificativa + 2 perguntas globais | **presente** |
| S5 · estímulos mostrados | não existem arquivos anonimizados; o protocolo declara (linhas 63–67) as 6 arquiteturas — Jokul = C0/C1, AcmeAir = C1/C2, TNTConcept = C1/C3 — e os arquivos correspondentes estão no corpus | **ausente** (gap real — §7) |
| S5 · manifest respondente→sistema→configuração | não existe; a planilha não tem coluna de sistema nem de avaliador (só *timestamp*) | **ausente** (gap real — §7) |
| S5 · consentimento / anonimato | não há declaração; a planilha não contém nome nem e-mail | **ausente** (gap real — §7) |
| S6 · scripts que geraram tabelas e figuras | `Multi-agent-Experiments/quantitative_analysis/` (13 `.py`, pipeline **congelado**) e `Quantitative-Analysis-Updated/` (11 `.py`, pipeline **estendido**) | **presente** (dois pipelines, ambos declarados) |
| S6 · ambiente e reprodutibilidade | `requirements.txt`, `README.md` dos dois pipelines (ordem de execução, cache, seed fixo, bootstrap), `verify_report.py` | **presente** |
| S7 · mapa artigo→artefato | §7 *Artifact index* do consolidado (45 blocos: modelo × configuração × rodada e arquivo por métrica/YAML/metadados) + §4.1 | **presente** |
| S7 · exclusões e questões conhecidas | §6 do consolidado + `README.md` §*Notes and Known Inconsistencies* + `Dates/README.md` §*Known Inconsistencies* + `Quantitative-Analysis-Updated/README.md` | **presente** |
| S7 · checksums | **não existem** (SHA-256 nunca foi gerado); a integridade é verificável por `verify_report.py` e pela contagem de linhas das tabelas | **ausente** |
| — · README do depósito no formato S1–S7 | não existe nesse formato; existem o `README.md` do artefato e **este documento** | **ausente** (substituído por este mapa) |
| — · `scan_all.py`, `build_md.py`, `verify_txt.py`, `verification.md`, `bundles.json`, `all_data.csv` | **não existem no depósito**: eram ferramentas de trabalho (*scratch*), nunca versionadas. O log escrito por `verify_txt.py` está **reproduzido** no §4.3 do consolidado e a ausência está **declarada** no §6 | **ausente por desenho** |

## 4. Por que as ausências não impedem a reprodutibilidade

A cadeia de rastreio de **todo número do artigo** está completa dentro do depósito:

```
Requirements-used-as-input/<sys>/{requirements, reference_services, reference_interactions}.txt   (S1)
        + Dates/static-analysis-systems/<sys>/*.csv                                              (S1)
        + Dates/davinci_inputs/<sys>/*                                                           (S1)
              ↓  Prompts-used-in-the-agents/Agent-1..5 — + main_fewshot.py + agentes/            (S2)
        Report-and-Dates/<Modelo>/<Cx>/Test-<n>/ {Metrics.pdf, YALM.pdf, execuion-metadados-*.json}  (S3)
              ↓  leitura por pdfplumber em _source_scan.py / extract_data.py / prepare_data.py
        Quantitative-Analysis-Updated/data.csv  (360 observações, seed fixo)                     (S3)
              ↓  descriptive_stats.py · paired_tests.py · correlation.py · cost_report.py · plots.py
        *.csv + results.json + figures/*.png + report.md  (2 pipelines)                          (S6)
              ↓  generate_report.py → render_report_html.py (preview, regenerável)
        DAVINCI-Consolidated-Report.md  (§3 estatística, §4 sínteses, §6 limitações, §7 índice)   (S7)
              ↓
        Qualitative-Analysis/{Qualitative-Evaluation-Protocol.txt, Answer-sheet(Answers).xlsx}   (S5)
```

O que está ausente é **conveniência de leitura** — um CSV único de sistemas, um *manifest* da
avaliação humana, um arquivo de *checksums* — e **não evidência**. Todos os artefatos primários
existem: as 45 execuções (15 por modelo), os 45 metadados de custo, as 15 sínteses de texto, as
360 observações tabuladas, os dois pipelines com *seed* fixo, os dois relatórios e as 12 respostas
humanas. As ferramentas de trabalho (`scan_all.py`, `build_md.py`, `verify_txt.py`)
eram intermediárias de autoria: os **produtos** delas são justamente o `data.csv` e o próprio
relatório consolidado, ambos presentes, e o log de conferência que geravam está reproduzido no
§4.3 do consolidado.

## 5. Exclusões deliberadas (não são lacunas)

**Removidos do depósito nesta etapa** (bytes idênticos preservados na versão de trabalho do autor):
notas internas de desenvolvimento (`pipeline-history.md`, `INPUT_DATA_GUIDE.md`,
`consolidated-report-c0-c3-ablation-experiments.md`, `Alteracoes-Conclusoes-*.txt`,
`Aprendizados-Hipoteses-*.txt`, `Inputs-for-PetClinic-and-Bookstore.txt`), 8 diagramas de trabalho
(`Dots/*.dot`), `requirements-fixed.txt` (lista relaxada declarada obsoleta pelo próprio README) e
`experimento_completo.py` (iteração anterior do pipeline). Permanecem as pastas `.md/` e `Dots/`,
hoje vazias.

**Recomendados para exclusão antes do *upload*** (nada do artigo depende deles):
`result/` (4.259 arquivos de saída local de execução, inclusive `results-tracer-*`),
`Dates/systems/` (672 arquivos / 106,7 MiB de código de terceiros, com uma licença por projeto),
`Dates/static analysis/SootUp/` (clone vendorizado, não invocado pelo método),
`Interface/` (aplicação web da ferramenta) e os `__pycache__/`.

**Mantidos de propósito, embora pareçam redundantes:** os pares de sínteses em TXT
(`Cx-<Modelo>-Synthesize-two-three-tests.txt` e a cópia de nome genérico). As sínteses são citadas
no §4.2 do consolidado; a segunda cópia é redundância documental herdada, não um erro — e o §4.3
registra as 18 divergências entre síntese e PDF.

## 6. Fatos que a revisão deve aceitar como estão

1. **Grafia `execuion-metadados-*.json`** (sem o “t” de *execution*): presente nos 45 arquivos e
   lida pelos scripts. Renomear quebra `_source_scan.py`, `extract_data.py` e `prepare_data.py`.
2. **`FS-Complete-<Modelo>-<n>-*` usa o número da rodada (1–3), não a configuração**; a
   configuração vem da pasta `Cx`. A configuração C4 tem duas propostas (A1/A2).
3. **`DeepSeek/C3/Test-1`** guarda TEXTOS em vez de PDFs (`FS-Complete-DeepSeek--YALM.txt`, 39,8 KB
   + `FS-Complete-DeepSeek-1-Metrics.txt`, 1,0 KB): a execução existe; o artefato foi gravado em texto.
4. **`Gemini/C2/Test-1`** tem **três** PDFs (um YALM repetido no mesmo *run*) e o metadado é
   `execuion-metadados-C2-Gemini-FS2.json`.
5. **`Claude/C4/Test-3`** ocorreu, mas **não gerou F1** (4 observações sem métrica); o custo está no
   metadado e o fato está no §6 do consolidado.
6. **7 `execution_id` repetidos** (Claude/C2, rodadas 2 e 3): 360 linhas, 353 identificadores
   distintos — registrado no §6.
7. **`Original-Requirements_PT.xlsx`** é a proveniência (enunciados originais, em PT); os TXT em
   `Requirements-used-as-input/` são a versão normalizada em EN que entrou nos prompts.
8. **`Answer-sheet(Answers).xlsx`**: cabeçalho do Google Forms em PT-BR com critérios em EN; não há
   coluna de sistema nem de avaliador (apenas *timestamp*) — o vínculo coluna↔sistema é o da ordem
   do formulário; já o protocolo (linhas 59–61 e 234) declara ordem de apresentação **sorteada por
   avaliador** — inconsistência documental registrada, não corrigível *a posteriori*.

## 7. Pendências reais — as únicas existentes

| Pendência | Natureza |
|---|---|
| S4 — 5 análises de robustez (variabilidade por célula, contrastes focais, rodada comum, penalidade de falha, leave-one-system-out) | a **produzir**; os dados estão em `data.csv`; “rodada comum” exige balanceamento, impedido pelas 4 observações sem F1 (Claude/C4, rodada 3) |
| S5 — estímulos anonimizados (“Architecture 1/2”), manifest respondente→sistema→configuração→rodada e nota de consentimento/anonimato | a **produzir/decidir** (nenhum arquivo do depósito informa qual rodada foi exibida) |
| S7 — `CHECKSUMS.sha256` | a **gerar** (hoje a verificação é `verify_report.py` + contagem de linhas) |
| README do depósito no formato S1–S7 | **não existe**; este documento cumpre o papel de mapa |
| Postura de licença | o `README.md` declara uso restrito/não comercial enquanto o PDF anexado é CC BY 4.0 — **decidir antes do upload** |
| Exclusão de `result/`, `Dates/systems/`, `SootUp/`, `Interface/` | **decidir** antes de zipar (recomendado excluir: −≈125 MiB) |

> Enquanto essas seis linhas não forem resolvidas ou aceitas como limitações declaradas, qualquer
> pedido adicional deve ser respondido com: *“o depósito é o corpus completo + os dois pipelines de
> análise + a avaliação humana; o que não existe está listado como pendência declarada na seção 7
> do `ZENODO-DEPOSIT-TREE.md`”*.

---

### Nota de uso deste documento

* Ele **não está dentro** da pasta do depósito: foi gravado em `DAVINCI\ZENODO-DEPOSIT-TREE.md`,
  ao lado de `Zenodo-DAVINCI-...-Study\`, para não alterar os bytes do que será zipado. Se você
  quiser que ele viaje **dentro** do `.zip` (recomendável como porta de entrada do depósito),
  mova-o para a raiz da pasta do depósito antes de gerar o pacote.
* Ele é o artefato de referência para a discussão com o orientador e para o LLM revisor: contém a
  árvore verificada, o mapa “item pedido → arquivo real” e as **seis** pendências reais.
* Números de controle para conferência independente: **5.472 arquivos · 249.820.953 B** ·
  45 execuções (15 por modelo) · 45 metadados JSON · 163 arquivos no corpus de saída
  (54 Claude + 55 Gemini + 54 DeepSeek) · `data.csv` com **361 linhas** · consolidado com
  **3.152 linhas** · 26 arquivos em `Requirements/` · 6 prompts · 2 arquivos de avaliação humana.




