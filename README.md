# Code Task Mobi7 

## Objetivo

O objetivo desse projeto é encontrar respostas sobre a permanência de certos veículos rastreados em pontos de interesse específicos (POIs). Os principais dados que queremos encontrar são:
- Quantidade de tempo que os veículos passaram parados dentro de cada POI
- Quantidade de tempo que os veículos estavam dentro de cada POI
- Tempo total da frota gasto parado em cada POI
- Tempo total parado por veículo, independente do POI

A aplicação gera os dados em um dicionário em que teremos como chave a resposta do problema (por exemplo: placa do veículo + POI + estado da ignição do carro)

O código foi escrito em python e utilizei como IDE o Google Colab. Os arquivos CSV usados como base de dados estarão nesse repositório.

## Método

O primeiro passo foi encontrar em qual ponto cada veículo estava no momento em que o sinal do rastreamento foi captado. Para isso utilizou-se da equação de Haversine, que transforma distâncias entre pontos com latitude e longitude em distâncias terrestres. Caso essa distância fosse menor ou igual ao raio do POI, considera-se o veículo dentro do poi e esse dado é inputado em uma nova coluna do dataframe. Caso contrário, é indicado que o carro está fora dos POIs.

Em seguida trata-se os dados de data, para que possamos fazer operações matemáticas com eles usando python.

O último passo é validar as condições e inserir os dados dentro de um dicionário, com a soma dos tempos para cada pergunta diferente que temos. 
Então, por exemplo, para o caso onde precisamos identificar o tempo que o veículo passou parado em cada POI, temos uma chave com o Veículo (placa) + estado da ignicação (aqui sempre queremos desligado) + o POI em que o veículo está.

## Como utilizar a aplicação

Nesse repositório teremos os arquivos csv, o python notebook (.ipynb) e um arquivo .py. Assim o usuário pode escolher a melhor forma para testar o código. 
Em cada etapa do código há comentários sobre o que está acontecendo, caso exista alguma dúvida.

Para subir os arquivos via Google Colab, tem um import e mount do Google Drive. Caso for utilizar Jupyter ou outra IDE, há outras formas de subir o CSV, como localmente ou via URL.

O arquivo será convertido em um pandas dataframe e tratado assim durante todo o processamento.

## Leitura do resultado final

Conforme já exemplificado, o resultado final será um dicionário contendo a chave (problema proposto) e o tempo calculado.

Para a leitura da chave é importante ter 3 dados em mente: 

- POI (número do ponto de referência). Aqui estará indicado de 0 a 23, sendo 0 o primeiro item da lista de POIs (POI 1) e 23 e último (POI 24)
- Placa (identificador do veículo)
- Ignição True (ligada) ou False (desligada).

Outro fator importante ressaltar é que quando o veículo não se enquadrar em nenhum POI, haverá a flag "fora do poi" na coluna "poi" do dataframe gerado.
