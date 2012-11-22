import sys

meses = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','Mai':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
dic_dia_polaridades = {}

def calculaMedia(lista):
  lista_aux = []
  for polaridade in lista:
    try:
      lista_aux.append(float(polaridade))
    except ValueError:
      continue
  return sum(lista_aux)/len(lista_aux)

def capturatt(linha):
  linha_campos_tt = linha.split('\t')[3]
  return linha_campos_tt.replace('\n','').replace('\t','').replace('"','').strip()

if len(sys.argv) != 3:
  print "Uso: python agrega_por_tt.py <arquivo com tweets classificados> <arquivo de saida>"
  sys.exit()

POLARIDADE = 2

arquivo_de_tweets = open(sys.argv[1], 'r')

for linha in arquivo_de_tweets.readlines():
  try:  
    tt = capturatt(linha)
    linha_sep = linha.split('\t')

    if len(linha_sep) != 5:
      continue

    else:
      if dic_dia_polaridades.has_key(tt):
        dic_dia_polaridades[tt].append(linha_sep[POLARIDADE])
      else:
        dic_dia_polaridades[tt] = []
        dic_dia_polaridades[tt].append(linha_sep[POLARIDADE])
  except (KeyError, IndexError):
    continue

arquivo_de_saida = open(sys.argv[2],'a')
dias = dic_dia_polaridades.keys()
dias.sort()

for dia in dias:
  media = calculaMedia(dic_dia_polaridades[dia])
  tamanho = len(dic_dia_polaridades[dia])
  arquivo_de_saida.write("%s\t%s\t%s\n"%(dia,tamanho,media))

arquivo_de_saida.close()
arquivo_de_tweets.close()  
