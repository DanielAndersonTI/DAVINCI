# Regra de etiquetagem das fronteiras

Escrita em 26 de novembro de 2026, antes de qualquer marcação. Vale para os 52
serviços da referência. Não é alterada durante a marcação; dúvida vai para a
coluna `duvida` e é resolvida depois.

## O que a etiqueta é

Um atributo do gabarito, serviço por serviço. Diz se a fronteira daquele serviço
na arquitetura de referência é reconhecível a partir do texto dos requisitos ou
se ela exigiu uma decisão de projeto.

Não é etiqueta de aresta. Não é nota do modelo. Não vai para a entrada do
experimento.

## Onde está o material

| Arquivo | Para que serve |
|---|---|
| `corpus/requirements-v2/<sistema>.en.txt` | o texto que o modelo vê, congelado |
| `labels/labels.csv` | a planilha, 52 linhas, uma por serviço |
| `corpus/reference/*.csv` | a referência. **Fechada na rodada 1** |
| `OneDrive\Auditorias-DAVINCI\corpus-publico\static-analysis` | módulos e pacotes de cada sistema, fora do repositório, para a rodada 2 |

Use o texto congelado. Não use `Requirements-used-as-input`, que é a entrada
antiga com pistas.

## Rodada 1, pelo texto

Você vê apenas duas coisas: o arquivo `<sistema>.en.txt` e o nome do serviço na
planilha. Não abra a descrição da referência nesta rodada.

Para cada linha da planilha, preencha:

1. **linhas**: os identificadores do requisito que compõem aquele serviço,
   separados por espaço. Exemplo: `RF-01 RF-02 RNF-45`.
2. **etiqueta**: `agrupamento` ou `decisao`, pela regra abaixo.
3. **duvida**: vazio, ou a razão em uma linha, se ficou em dúvida. Mesmo em
   dúvida, a etiqueta é preenchida.
4. **rodada1_data**: a data, no formato 2026-11-27.

### A regra

> **Agrupamento** quando o conjunto de linhas daquele serviço se reconhece
> apenas pelo vocabulário e pela coesão do texto.
>
> **Decisão** quando o conjunto só se separa porque uma restrição de tamanho,
> volume, armazenamento, disponibilidade, carga, segurança ou propriedade impõe
> o corte, e o texto não marca o corte.

Perguntas de apoio, na ordem:

- As linhas deste serviço falam de um assunto só, com as mesmas palavras?
- Alguma linha declara uma restrição de operação que não é de negócio?
- Se eu juntasse este serviço com o vizinho mais próximo, algum requisito seria
  violado?

Exemplo já resolvido, para calibrar: no Jokul, o Authentication Service reúne
RF-01 a RF-07 e RF-34, todos sobre cadastro, login, perfil e sessão. O assunto é
um só e o vocabulário é o mesmo. Etiqueta: `agrupamento`.

## Rodada 2, pelo motivo

Só nas linhas marcadas como `decisao`. Agora abra a descrição daquele serviço em
`corpus/reference/` e, se precisar, a análise estática.

1. **motivo**: uma linha, dizendo qual restrição sustenta o corte. Exemplo de
   forma: "arquivos de até 2 GB e área de entrega própria separam o vídeo do
   catálogo".
2. Se não houver motivo no texto nem na estrutura do código, troque a etiqueta
   para `sem_motivo` e escreva a razão em `duvida`.
3. **rodada2_data**: a data.

Não reescreva a etiqueta por causa do motivo. Se o motivo contradiz a rodada 1,
registre em `duvida` e mantenha a etiqueta.

## Depois

1. Congelar: `sha256sum labels/labels.csv > labels/MANIFEST.sha256`.
2. Lista de conflito: todas as linhas com `duvida` preenchido.
3. Conferência do orientador, quinze minutos, sobre a lista de conflito.
4. `labels/relatorio.md` com as contagens: quantos agrupamentos, quantas
   decisões, quantos sem motivo, e o que o orientador mudou.

## O que não fazer

- Não editar `labels.csv` depois do hash sem emenda datada em `EMENDAS.md`.
- Não abrir a descrição da referência na rodada 1.
- Não olhar saída de modelo nenhuma. Não existe nenhuma até aqui, e continua
  assim até o congelamento.
- Não salvar o CSV pelo Excel. O Excel grava em cp1252 e quebra os acentos.
  Edite no VS Code, ou no LibreOffice escolhendo UTF-8 ao salvar.

## Tempo

Rodada 1, cerca de quarenta minutos. Rodada 2, cerca de quarenta, só nas
decisões. Conferência do orientador, quinze.
