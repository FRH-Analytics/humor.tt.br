import sys

if len(sys.argv) != 3:
  print "Uso: python agrupaporhora.py <arquivo de tweets polarizados> <arquivosaida>"
  #sys.exit()

dicionario_data_humor = {}

def processaTimeStamp(timestamp):
  try:
    campos = timestamp.split(' ')
    hora = campos[4].split(':')[0]
    return "%s/%s/%s/%s"%(campos[1],campos[2],campos[3],hora)
  except IndexError:
    print 'linha mal-formatada'

arquivo_polarizado = open(sys.argv[1],'r')
for linha in arquivo_polarizado.readlines():
  linha_campos = linha.split('\t')
  chave_para_dicionario = processaTimeStamp(linha_campos[0])
  if dicionario_data_humor.has_key(chave_para_dicionario):
    dicionario_data_humor[chave_para_dicionario] = float(dicionario_data_humor[chave_para_dicionario]) + float(linha_campos[len(linha_campos) - 1]) 
  else:
    dicionario_data_humor[chave_para_dicionario] = float(linha_campos[len(linha_campos) - 1])

arquivo_saida = open(sys.argv[2],'a')

for chave in dicionario_data_humor.keys():
  if chave != None:
    arquivo_saida.write("%s\t%s\n"%(chave,dicionario_data_humor[chave]))

arquivo_saida.close()
