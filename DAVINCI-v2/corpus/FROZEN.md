# Corpus congelado

Data do congelamento: 26 de novembro de 2026.

## O que está congelado

- `requirements-v2/`, 16 arquivos, 509 requisitos, em inglês e em português.
- `reference/`, 8 arquivos, 52 serviços.

## Como verificar

Na pasta `corpus/`:

```
sha256sum -c MANIFEST.sha256
```

Cada arquivo deve responder `OK`. Nenhum arquivo deve responder `FAILED`.

## O que este congelamento significa

Os arquivos acima não são alterados a partir desta data sem emenda registrada. A
execução, a etiquetagem e a análise usam exatamente este conteúdo. Mudança
depois do congelamento entra como emenda datada em `EMENDAS.md`, com o motivo, o
antes, o depois e o novo hash. Correção silenciosa não é permitida.

## Emendas

Nenhuma até a data do congelamento.

## Correções aplicadas antes do congelamento

1. Pet-clinic, RF-01: "The system must provide a home page for user input"
   substituído por "for user entry". O original em português diz "entrada do
   usuário", que é entrada no sistema, não entrada de dados.
2. TNTConcept: o texto do RF-ADM-04 aparece dentro da descrição de outro
   requisito, com quebra de linha. Espaços normalizados, conteúdo preservado.

## Origem

Tradução publicada pelo projeto, conferida contra o original em português nos
oito sistemas, 509 a 509. Referência copiada de
`Experimento_Multiagente/Dates/ground true/`, sem alteração, e a partir daqui sob
domínio de `DAVINCI-v2/`.

## O que não está congelado

- As etiquetas de fronteira, que são o passo 3 e serão congeladas em arquivo
  próprio.
- O código dos agentes.
- Os prompts.
