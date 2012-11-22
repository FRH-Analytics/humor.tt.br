import sys

meses = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','Mai':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
dic_dia_polaridades = {}

def ordenaPorData(datas):
  lista_aux = []
  for i in range(0,len(datas)):
    dia = datas[i].split('/')[0]
    lista_aux.append((int(dia),i))
  lista_aux.sort()
  lista_ordenada = []
  for dia,i in lista_aux:
    lista_ordenada.append(datas[i])
  return lista_ordenada
    

def calculaMedia(lista):
  lista_aux = []
  for polaridade in lista:
    try:
      lista_aux.append(float(polaridade))
    except ValueError:
      continue
  return sum(lista_aux)/len(lista_aux)

def capturadia(linha):
  linha_campos = linha.split('\t')
  timestamp_split = linha_campos[0].split(' ')
  ano = timestamp_split[3]
  mes = meses[timestamp_split[2]]
  dia = timestamp_split[1]
  return "%s/%s/%s"%(dia,mes,ano)

if len(sys.argv) != 3:
  print "Uso: python agrega_por_dia.py <arquivo com tweets classificados> <arquivo de saida>"
  sys.exit()

POLARIDADE = 2

arquivo_de_tweets = open(sys.argv[1], 'r')

for linha in arquivo_de_tweets.readlines():
  try:  
    dia = capturadia(linha)
    linha_sep = linha.split('\t')

    if len(linha_sep) != 5:
      continue

    else:
      if dic_dia_polaridades.has_key(dia):
        dic_dia_polaridades[dia].append(linha_sep[POLARIDADE])
      else:
        dic_dia_polaridades[dia] = []
        dic_dia_polaridades[dia].append(linha_sep[POLARIDADE])
  except (KeyError, IndexError):
    continue

arquivo_de_saida = open(sys.argv[2],'a')

for dia in ordenaPorData(dic_dia_polaridades.keys()):
  media = calculaMedia(dic_dia_polaridades[dia])
  tamanho = len(dic_dia_polaridades[dia])
  arquivo_de_saida.write("%s\t%s\t%s\n"%(dia,tamanho,media))

arquivo_de_saida.close()
arquivo_de_tweets.close()  
