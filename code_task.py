import pandas as pd
from datetime import datetime, date, timedelta 
import math
import pprint
import plotly.express as px
#from google.colab import drive
#drive.mount('/content/drive')

# caminho, url ou link dos arquivos que contem as posições dos veículos (posições) e do arquivo da localização das pois

posicoes = '/content/drive/MyDrive/Code task - Mobi7/posicoes.csv'
pois = '/content/drive/MyDrive/Code task - Mobi7/base_pois_def.csv'

# converte os csv em pandas dataframes

df_posi = pd.read_csv(posicoes)
df_pois = pd.read_csv(pois)

# haversine - fórmula para encontrar distâncias de lat long em distância terrestre

#raio da terra
R = 6373.0 

# conversão das coordenadas para radianos

df_posi['lat_rad'] = df_posi['latitude'].apply(math.radians)
df_posi['long_rad'] = df_posi['longitude'].apply(math.radians)

df_pois['lat_rad'] = df_pois['latitude'].apply(math.radians)
df_pois['long_rad'] = df_pois['longitude'].apply(math.radians)

def poi(df_posi):
  
  lista = []

  global df_pois

  for j in df_pois.index:
    dlon = df_pois.loc[j,'long_rad'] - df_posi['long_rad']
    dlat = df_pois.loc[j,'lat_rad'] - df_posi['lat_rad']

    a = math.sin(dlat/2)**2 + math.cos(df_posi['lat_rad']) * math.cos(df_pois.loc[j,'lat_rad']) * math.sin(dlon/2)**2

    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c *1000

    # lista.append(distance)

    if distance <= df_pois.loc[j,'raio']:
      return j
    #else:
    #  return 'fora do poi'

  #return df_stop
  return 'fora do poi' 

df_posi['poi'] = df_posi.apply(poi, axis=1)

# Tratamento da data para um formato em que seja possível calcular o timedelta

df_posi['data_posicao'] = df_posi['data_posicao'].str.split('G', 1, True)
df_posi['data_posicao'] = df_posi['data_posicao'].apply(lambda x: x.rstrip())
df_posi['data_posicao'] = df_posi['data_posicao'].apply(lambda x: datetime.strptime(x, '%a %b %d %Y %H:%M:%S'))
df_posi.sort_values(by = ['placa','data_posicao'], ascending = True, inplace= True, ignore_index=True)

# encontrando os resultados e inserindo em um dicionário
# cada chave do dicionário tem o dado do poi / placa / situação da ignição

resultados = {}

data_inicial = None
estado_ignicao = None

for i in df_posi.index:
  
  if data_inicial != None and estado_ignicao == df_posi['ignicao'][i]:

    diff = df_posi['data_posicao'][i] - data_inicial

    #total placa
    if not df_posi['placa'][i] in resultados:
      resultados[df_posi['placa'][i]] = timedelta(0)
    resultados[df_posi['placa'][i]] += diff

    # total placa desligado

    if df_posi['ignicao'][i] == False:

      if not (df_posi['placa'][i]+'off') in resultados:
        resultados[df_posi['placa'][i]+'off'] = timedelta(0)
      resultados[df_posi['placa'][i]+'off'] += diff

    # total poi

    if not (df_posi['poi'][i]) in resultados:
      resultados[df_posi['poi'][i]] = timedelta(0) 
    resultados[df_posi['poi'][i]] += diff 

    # total parado por poi

    if df_posi['ignicao'][i] == False: 

      if not (str(df_posi['poi'][i])+'off') in resultados:
        resultados[str(df_posi['poi'][i])+'off'] = timedelta(0)
      resultados[str(df_posi['poi'][i])+'off'] += diff

    # total parado por poi por veículo

    if df_posi['ignicao'][i] == False:

      if not (str(df_posi['poi'][i])+df_posi['placa'][i]) in resultados:
        resultados[str(df_posi['poi'][i])+df_posi['placa'][i]] = timedelta(0)
      resultados[str(df_posi['poi'][i])+df_posi['placa'][i]] += diff
    
  data_inicial = df_posi['data_posicao'][i]
  estado_ignicao = df_posi['ignicao'][i]

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(resultados)

# fig = px.scatter_geo(df_pois, lat=df_pois['latitude'], lon=df_pois['longitude'], size="raio", hover_name = df_pois['nome'])
#fig.show()