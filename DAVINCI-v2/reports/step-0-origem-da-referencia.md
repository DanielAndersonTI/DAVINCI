# Passo 0, origem da referência

Data: 26 de novembro de 2026. Status: concluído com uma pendência de conferência.

## Pergunta

A referência de 52 serviços descreve a implementação ou os requisitos? A resposta
decide se D4, referência fixa, vale, e se as etiquetas de fronteira medem algo.

## Material usado

| Fonte | Volume |
|---|---|
| Referências de arquitetura | 8 arquivos, 52 serviços |
| Requisitos originais em português | 8 arquivos, 509 requisitos |
| Tradução publicada em inglês | 8 arquivos JSON, 509 entradas |
| Análise estática do código | 40 arquivos, módulos, pacotes, dependências, classes |

A tradução publicada é 1:1 com o original em todos os oito sistemas: 69, 62, 83,
52, 67, 70, 62 e 44 entradas. Nenhuma das oito contém linha que nomeie serviço ou
declare aresta. As linhas de pista usadas no experimento anterior foram
acrescentadas sobre a tradução, na entrada do experimento.

## Achados

**1. Os oito sistemas são monolitos.** A contagem de módulos de construção vai de
1 a 4, e a de pacotes, de 6 a 72.

| Sistema | Módulos | Pacotes | Serviços na referência |
|---|---|---|---|
| 7ep | 3 | 14 | 7 |
| Jokul | 1 | 12 | 3 |
| TNTConcept | 3 | 72 | 14 |
| acmeair | 1 | 10 | 6 |
| cargo-tracker | 1 | 28 | 6 |
| daytrader7 | 4 | 11 | 6 |
| jpetstore | 1 | 6 | 6 |
| pet-clinic | 2 | 7 | 4 |
| **Total** | **17** | **160** | **52** |

**2. A referência não é a estrutura de módulos.** São 52 serviços contra 17
módulos. A razão por sistema varia de 1,5 a quase 5.

**3. O alinhamento com os pacotes varia, e a variação é o achado.** Nos oito
sistemas, a decomposição corta em algum lugar diferente da estrutura física.

| Sistema | O que os pacotes mostram | Relação com a referência |
|---|---|---|
| Jokul | 12 pacotes em camadas (controller, domain, repositories, services) | a referência corta por domínio, não por camada |
| cargo-tracker | pacotes de modelo por conceito (cargo, handling, location, voyage) e de infraestrutura | a referência segue em boa parte os pacotes |
| jpetstore | domain, mapper, service, actions | corta por domínio, contra camadas |
| acmeair | camadas mais loader e mongo | corta por domínio, contra camadas |
| daytrader7 | beans, ejb3, entities, web, jsf | corta por domínio, contra camadas |
| 7ep | mistura de pacotes de demonstração (math, autoinsurance, library) | corta por capacidade, não por pacote |
| pet-clinic | owner, domain, ui, internal | a referência separa quatro domínios onde o código tem um |
| TNTConcept | 72 pacotes em 3 módulos | corta por área de negócio |

**4. No Jokul o corte da referência é visível e não está no código.** O sistema é
um único jar Maven. As classes de armazenamento existem, mas convivem com as
demais no mesmo artefato: `StorageService`, `FileSystemStorageService`,
`StorageProperties`, `MovieUploadController`. A referência separa Media do
Catalog. Essa separação é uma decisão, não uma leitura da estrutura.

**5. Os requisitos foram elicitados do código.** Duas linhas do original em
português descrevem o estado atual do sistema, e não o desejado: RNF-60, "essa
restrição não aparece validada no backend", e RNF-61, "o sistema atual está mais
orientado a um acervo local de filmes". Requisito que descreve o que o código faz
hoje só pode ter sido escrito olhando o código.

## Conclusão

A referência é uma decomposição humana de um monolito, fixa e publicada, e não a
extração de uma estrutura que já exista no código. D4 vale no sentido operativo:
a referência não muda com o texto dos requisitos e serve de gabarito para todas
as configurações. A formulação de 12.9, item 4, fica corrigida: a referência é
julgamento registrado sobre o sistema construído, não fato extraído dele.

## Consequências para o desenho

- A tarefa do modelo é decompor um monolito a partir da especificação. É a
  pergunta da indústria, e é mais defensável do que extrair serviços nomeados.
- O rótulo de fronteira continua textual, como em D7. A estrutura do código
  serve de evidência para escrever o motivo, em D10, e nunca como regra de
  rotulagem. Se a regra fosse estrutural, todo serviço do Jokul viraria decisão,
  porque o código não separa nenhum dos três, e o rótulo perderia o sentido.
- A referência precisa ser publicada no kit de reprodutibilidade. Ela não está
  no repositório público do projeto, e sem ela o benchmark não é reproduzível.

## Pendências

- Conferir o conteúdo da tradução por amostra, cinco requisitos por sistema,
  contra o original em português.
- Decidir se o identificador do requisito entra na entrada v2, já que a categoria
  sai por vazar o agrupamento.
