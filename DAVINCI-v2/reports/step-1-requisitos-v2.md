# Passo 1, requisitos v2

Data: 26 de novembro de 2026. Status: concluído, anterior ao congelamento.

## Origem

Tradução publicada do projeto, 8 arquivos JSON, e os originais em português, 8
CSVs. Cópia local em `OneDrive\Auditorias-DAVINCI\corpus-publico\`, fora do
repositório.

## O que foi gerado

`corpus/requirements-v2/`, um arquivo por sistema e por idioma, 16 no total. Uma
linha por requisito, no formato `RF-01: texto`. O inglês é a entrada do
experimento; o português fica ao lado, para rastreabilidade.

| Sistema | Linhas |
|---|---|
| 7ep | 69 |
| Jokul | 62 |
| TNTConcept | 83 |
| acmeair | 52 |
| cargo-tracker | 67 |
| daytrader7 | 70 |
| jpetstore | 62 |
| pet-clinic | 44 |
| **Total** | **509** |

## Transformações aplicadas

1. **Categorias retiradas.** A tradução publicada traz uma categoria por
   requisito, e o nome da categoria entrega o agrupamento. Jokul tem "Movie
   catalog", "Media and storage" e "Access and user roles"; acmeair tem "Client
   Access and Session". Se entrassem na entrada, a pista voltaria por outra
   porta.
2. **Uma linha por requisito.** O texto de TNTConcept, RF-ADM-04, contém uma
   quebra de linha e um segundo identificador dentro da descrição de outro
   requisito. Espaços normalizados, sem perda de conteúdo.
3. **Identificador mantido.** Permite que o motivo declarado cite a restrição que
   o justifica, por exemplo RNF-48, sem indicar agrupamento.

## Verificação

- Contagem: 509 linhas, igual aos 509 requisitos do original. Nos oito sistemas,
  original e tradução batem um a um.
- Formato: nenhuma linha fora do padrão `ID: texto`.
- Pistas: zero ocorrências da varredura que encontrou 80 linhas de pista na
  entrada anterior (32 de fronteira e 48 de dependência).
- Amostra de conteúdo: 24 pares, três por sistema. Vinte e três fiéis. Uma falha,
  pet-clinic RF-01, "página inicial para entrada do usuário" traduzido como "home
  page for user input", que perde o sentido de entrada no sistema.

## Pendente antes de congelar

- Decidir sobre a falha de pet-clinic RF-01: corrigir o texto ou manter e
  registrar. Recomendação: corrigir, porque entrada no sistema é informação de
  acesso e toca a fronteira de autenticação.
- Congelamento com hash, que é o passo 2.
