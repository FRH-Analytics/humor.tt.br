import sys

#TODO fazer a saida ser ordenada pelo tempo

dicionario_humor_dia  = {}
dicionario_humor_hora = {}

if len(sys.argv) != 3:
  print "Uso: python agrupapordia.py <arquivo entrada> <arquivo saida>"
  sys.exit()

arquivo = open(sys.argv[1],'r')
linhas = arquivo.readlines()

def extraiDiaMes(timestamp):
  try:
    res = timestamp.split(' ')
    return "%s/%s"%(res[1],res[2])
  except IndexError:
    return None
  
for linha in linhas:
  try:
    linha_campos = linha.split('\t')
    dia_mes = extraiDiaMes(linha_campos[0])
    if dicionario_humor_dia.has_key(dia_mes):
      dicionario_humor_dia[dia_mes] = dicionario_humor_dia[dia_mes] + float(linha_campos[len(linha_campos) -2])
    else:
      dicionario_humor_dia[dia_mes] = float(linha_campos[2])
  except ValueError:
    continue

arquivo_out = open(sys.argv[2],'a')
for chave in dicionario_humor_dia.keys():
  arquivo_out.write("%s,%s\n"%(chave, dicionario_humor_dia[chave]))
arquivo_out.close()
