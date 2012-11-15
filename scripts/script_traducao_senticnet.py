# -*- coding: utf-8 -*-

import time
from microsofttranslator import Translator
from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(open('senticnet.rdf', 'r'))
dicionario = {}
textos = soup.findAll('text')

polaridade = soup.findAll('polarity')

assert len(textos) == len(polaridade)

for i in range(0,len(textos)):
  dicionario[ textos[i].contents[0].lower() ] =  float(polaridade[i].contents[0])

assert dicionario['december'] == 0.611

tradutor = Translator("0ef986af-2384-4257-9562-8aa9ac02abb5","8iDU8Hv04E4bQXTCCFvL1oj/RIITad3yX8TYxx+UC4o=")

#Testa se o tradutor esta funcionando
#assert tradutor.translate(unicode("Olá","utf-8"), 'en', 'pt') == "Hello"

arq_out = open('senticnet_pt.txt','a')
dicionario_pt = {}
texto = []
i = 0
for palavra in dicionario.keys():
  try:
    if i >= 200:
      tradutor = Translator("0ef986af-2384-4257-9562-8aa9ac02abb5","8iDU8Hv04E4bQXTCCFvL1oj/RIITad3yX8TYxx+UC4o=")
      i = 0
    palavra_pt = tradutor.translate(palavra, 'pt', 'en')
    dicionario_pt[palavra_pt] = dicionario[palavra]
    text = "%s\t%s\n"%(palavra_pt, dicionario[palavra])
    arq_out.write(text)
    print "%s\t%s\n"%(palavra, palavra_pt)
    time.sleep(2)
    i = i + 1
  except UnicodeEncodeError:
    print "erro codificacao"
    continue
arq.close()
