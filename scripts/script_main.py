# -*- coding: utf-8 -*-

import re
import sys
import csv
import ast
from BeautifulSoup import BeautifulSoup

#TODO substituir esse script por mapReduce, se houver necessidade

if len(sys.argv) != 4:
  print "Uso: python script_main.py <arquivo com palavraXpolaridade> <arquivo com stopwords> <arquivo de tweets>"
  sys.exit()

#Preparacao do dicionario de palavras com suas polaridades
dicionario = {}

palavra_polaridade = open(sys.argv[1],'r')
for linha in palavra_polaridade.readlines():
  try:
    linha_split = linha.split('\t')
    dicionario[linha_split[0].strip().lower()] = float(linha_split[1].strip().replace(',','.').replace(' ',''))
  except IndexError:
    continue
#Fim da preparacao

#Obrigado Andre Aranha, pelos emotions.
emotions_pos = (":-)", "(-:", "(-8", ":)", "(:", "(8", ";-)", "(-;", ";)", "(;","=-)", "(-=", "=)", "(=",":D", ";D", "=D", ":-D", ";-D", "=-D", "8D", "8-D",
":-O", "O-:", "8-O", "O-8", ":-o", "o-:", "8-o", "o-8", ":-0", "0-:", "8-0", "0-8", ";-O", "O-;", ";-o", "o-;", ";-0",
"0-;", "=-O", "O-=", "=-o", "o-=", "=-0", "0-=",":O", "O:", ":o", "o:", ":0", "0:", ";O", "O;", ";o", "o;", ";0", "0;", "=O", "O=", "=o", "o=", "=0", "0=",
"8O", "O8", "8o", "o8","B-)", "B)", "BD","*_*", "*-*", "*=*", "*.*", "**", "*o*", "*O*", "*0*", "*__*", "*--*", "*==*", "*___*", "*---*", "*===*",
"^_^", "^-^", "^=^", "^.^", "^^", "^o^", "^O^", "^0^", "^__^", "^--^", "^==^", "^___^", "^---^", "^===^","XD", "xD", "X-D", "x-D", "X)", "x)", "X-)", "x-)", "(X", "(x", "(-X", "(-x",":-]", "[-:", ":]", "[:", ";-]", "[-;", ";]", "[;", "=-]", "[-=", "=]", "[=", "x-]", "[-x", "x]", "[x","X-]", "[-X", "X]", "[X",
":')", "(':", ";')", "(';", "=')", "('=", ":'D", ";'D", "='D", ":']", "[':", ";']", "[';", "=']", "['=",
"\\o/", "\\O/", "\\0/", "o/", "O/", "0/", "\\o", "\\O", "\\0",":-*", "*-:", ":*", "*:", ";-*", "*-;", ";*", "*;","=-*", "*-=", "=*", "*=",":-P", ":P", ";-P", ";P", "=-P", "=P", ":-p", ":p", ";-p", ";p", "=-p", "=p","C-:", "C-;", "C-=", "C:", "C;", "C=", "c-:", "c-;", "c-=", "c:", "c;", "c=",":-3", ":3", ";-3", ";3", "=-3", "=3",
":-8", ":3", ";-3", ";3", "=-3", "=3","<3")

emotions_neg = (":-(", ")-:", ")-8", ":(", "):", ")8", ";-(", ")-;", ";(", ");","=-(", ")-=", "=(", ")=",":-/", "/-:", "/-8", ":/", "/:", ";-/", "/-;", ";/", "/;",
"=-/", "/-=", "=/", "/=",":-\\", "\\-:", "\\-8", ":\\", "\\:", ";-\\", "\\-;", ";\\", "\\;","=-\\", "\\-=", "=\\", "\\=",
">_<", ">.<", "> <", ">__<", ">___<","-_-", "-.-", "- -", "-__-", "-___-", "-_-'", "-.-'", "- -'", "-__-'", "-___-'", "'-_-", "'-.-", "'- -", "'-__-", "'-___-",
":-T", "T-:", "T-8", ":T", "T:", "T8", ";-T", "T-;", ";T", "T;","=-T", "T-=", "=T", "T=","X(", "x(", "X-(", "x-(", ")X", ")x", ")-X", ")-x", "XT", "xT", "X-T", "x-T", "TX", "Tx", "T-X", "T-x","X/", "x/", "X-/", "x-/", "/X", "/x", "/-X", "/-x", "X\\", "x\\", "X-\\", "x-\\", "\\X", "\\x", "\\-X", "\\-x", 
":-[", "]-:", ":[", "]:", ";-[", "]-;", ";[", "];", "=-[", "]-=", "=[", "]=", "x-[", "]-x", "x[", "]x","X-[", "]-X", "X[", "]X",
":-c", ":c", ";-c", ";c", "=-c", "=c", "x-c", "xc", "X-c", "Xc",":-C", ":C", ";-C", ";C", "=-C", "=C", "x-C", "xC", "X-C", "XC",
":-S", "S-:", "S-8", ":S", "S:", "S8", ";-S", "S-;", ";S", "S;","=-S", "S-=", "=S", "S=", "x-S", "S-x", "xS", "Sx", "X-S", "S-X", "XS", "SX",
":-$", "$-:", "$-8", ":$", "$:", "$8", ";-$", "$-;", ";$", "$;","=-$", "$-=", "=$", "$=", "x-$", "$-x", "x$", "$x", "X-$", "$-X", "X$", "$X", 
"o.o", "o_o", "O.O", "O_O", "0.0", "0_0","o.O", "o_O", "O.o", "O_o", "Oo", "Oo","</3", "<\\3", "¬¬")

stopwords = open(sys.argv[2],'rb').read().split('\n')

arquivo = open(sys.argv[3], 'r')
dados = []
for linha in arquivo.readlines():
  aux_list = []
  try:
    linha_split = linha.split('","')
    aux_list.append(linha_split[0])
    aux_list.append(linha_split[1])
    aux_list.append(linha_split[2])
    aux_list.append(linha_split[3])
    aux_list.append(linha_split[4])
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
  return ' '.join(linhaPreprocessada).strip().lower().replace('\t','')

DATA_TIME = 3
DATA_TT   = 4
lista_resultados = []
n_tweet = 0

for linha in dados:
  linhaTimeStamp = linha[DATA_TIME]
  linhaTT        = linha[DATA_TT]
  linhaText      = preprocessamento(linha)

  #Analisa presenca de emotions
  if containsEmotion(linhaText, emotions_pos) and not containsEmotion(linhaText, emotions_neg):
    lista_resultados.append((linhaText, 1))
  elif not containsEmotion(linhaText, emotions_pos) and containsEmotion(linhaText, emotions_neg):
    lista_resultados.append((linhaText, -1))
  else:
  #Analise textual em si.
    palavras = linhaText.split(' ')
    soma = 0
    n_expressoes = 0    
    
    #Tenta classificar por tri-gramas
    if soma == 0 and len(palavras) >= 3:

      for i in range(0, len(palavras) - 2):
        try:
          trigrama = palavras[i].strip()+" "+palavras[i+1].strip()+" "+palavras[i+2].strip()
          soma = soma + float(dicionario[trigrama.lower()])
          n_expressoes = n_expressoes + 1
        except KeyError, IndexError:
          continue

    #Tenta classificar por bi-gramas
    if soma == 0 and len(palavras) >= 2:
 
      for i in range(0, len(palavras) - 1):
        try:
          bigrama = palavras[i].strip()+" "+palavras[i+1].strip()
          soma = soma + float(dicionario[bigrama.lower()])
          n_expressoes = n_expressoes + 1
        except KeyError, IndexError:
          continue

    #Classifica por palavras individuais
    if soma == 0:

      for palavra in palavras:
         try:
           soma = soma + float(dicionario[palavra.strip().lower()])
           n_expressoes = n_expressoes + 1
         except KeyError, IndexError:
           continue

    try:      
      lista_resultados.append((linhaTimeStamp,linhaText, soma/n_expressoes, linhaTT))
    except ZeroDivisionError:
      continue

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
      print "TT: %s"%str(i[3])
      print "================================================================"
      arq_saida.write("%s\t%s\t%s\t%s\t%s\n"%(str(i[0]),str(i[1]), str(i[2]), str(i[3]), str(i[4])))
  except:
    continue
arq_saida.close()
