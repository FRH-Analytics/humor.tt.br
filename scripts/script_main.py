# -*- coding: utf-8 -*-

import re
import csv
import ast
from BeautifulSoup import BeautifulSoup

#TODO substituir esse script por mapReduce

#Preparacao do dicionario de palavras com suas polaridades
dicionario = {}

palavra_polaridade = open('palavra_polaridade_pt.txt','r')
for linha in palavra_polaridade.readlines():
  try:
    linha_split = linha.split('|')
    dicionario[linha_split[0].strip().lower()] = linha_split[1].strip().replace(',','.').replace(' ','')
  except IndexError:
    continue
#Fim da preparacao

emotions_pos = (' =)',' :)',' :-)',' :D',' ;)',' ;D')
emotions_neg = (' =(',' :(',' :-(',' ;(',' :/',' :[')

stopwords = open('stopwords.txt','rb').read().split('\n')

arquivo = open('tweets_dump_5k.txt', 'r')
dados = []
for linha in arquivo.readlines():
  aux_list = []
  try:
    linha_split = linha.split('","')
    aux_list.append(linha_split[0])
    aux_list.append(linha_split[1])
    aux_list.append(linha_split[2])
    aux_list.append(linha_split[3])
    dados.append(aux_list)
  except:
    continue

#Analisa se o tweet possui emotion
def containsEmotion(tweet, emotions):
  for emotion in emotions:
    if emotion in tweet:
      return True
  return False

#Ja retorna a linha pronta em lowercase apenas do texto do tweet.
#Nao esquecer de que para comparar com o texto do senticnet deve-se
#colocar para uppercase tambem, para que seja possivel a comparacao
def preprocessamento(linha):
  colunaText = linha[2]
  colunaText = colunaText.split(' ')
  linhaPreprocessada = []
  for token in colunaText:
    token = token.replace(' ','')
    if not (re.match("^RT", token) or re.match("^#", token) or re.match("^http://", token) or re.match("^@", token)):
      token = token.replace('!','').replace('?','').replace('.','').replace(',','').replace('\'','').replace('\"','')
      if not token.lower() in stopwords:
        linhaPreprocessada.append(token)
  return ' '.join(linhaPreprocessada).strip().lower()

DATA_TIME = 3
lista_resultados = []
n_tweet = 0
for linha in dados:
  linhaTimeStamp = linha[DATA_TIME]
  linhaText = preprocessamento(linha)
  if containsEmotion(linhaText, emotions_pos) and not containsEmotion(linhaText, emotions_neg):
    lista_resultados.append((linhaText, 1))
  elif not containsEmotion(linhaText, emotions_pos) and containsEmotion(linhaText, emotions_neg):
    lista_resultados.append((linhaText, -1))
  else:
    palavras = linhaText.split(' ')
    soma = 0
    
    for palavra in palavras:
      try:
        soma = soma + float(dicionario[palavra.strip().lower()])
      except KeyError:
        continue

    if soma == 0:
      for i in range(0, len(palavras) - 1):
        try:
          bigrama = palavras[i].strip()+" "+palavras[i+1].strip()
          soma = soma + float(dicionario[bigrama.lower()])
        except KeyError, IndexError:
          continue

    if soma == 0 and len(palavras) >= 3:
      for i in range(0, len(palavras) - 2):
        try:
          trigrama = palavras[i].strip()+" "+palavras[i+1].strip()+" "+palavras[i+2].strip()
          soma = soma + float(dicionario[trigrama.lower()])
        except KeyError, IndexError:
          continue
    lista_resultados.append((linhaTimeStamp,linhaText, soma))
  n_tweet = n_tweet + 1
  print "Numero de tweets processados: %s"%(str(n_tweet))

arq_saida = open('amostra_500k_polarizada.txt','a')

for i in lista_resultados:
  try:
    if i[2] != 0:
      print "================================================================"
      print "Timestamp: %s"%i[0]
      print "Tweet: %s"%i[1]
      print "Polaridade: %s"%str(i[2])
      print "================================================================"
      arq_saida.write("%s\t%s\t%s\n"%(str(i[0]),str(i[1]), str(i[2])))
  except:
    continue
arq_saida.close()