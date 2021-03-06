#!__ENV__ __PYTHON__

#
# 1. Leer .idx extrayendo palabras en las dos lenguas
# 2. Traducir palabras en los segundos documentos
# 3. Hacer interseccion entre cada par de documentos
# 4. Se muestran los 10 documentos de la segunda lengua mas parecidos a cada
#    uno de la primera
#
# Formato final del documento:
# num_doc_lang1    [num_doc_lang2:frequency]+
#
# Genera .ridx -> reverse index
#

import sys
import argparse
from sets import Set
from collections import defaultdict
from operator import itemgetter
import re

def readLETT(f, docs):
  file = open(f, "r")
  fileid = 1
  for i in file:
    fields = i.strip().split("\t")
    if len(fields) >= 5:
      #To compute the edit distance at the level of characters, HTML tags must be encoded as characters and not strings:
      docs[fileid] = fields[3]
    fileid += 1
  file.close()

#
# Se rellenan los indices de palabras en las dos lenguas a partir del
# .idx de la entrada.
#
def rellenarIndex(file, lang1, lang2, index1, index2):
  for i in file:
    campos = i.strip().split("\t")
    if len(campos) == 3:
      if campos[0] == lang1 or campos[0] == lang2:
        documentos = campos[2].split(":")
        acum = 1

        for j in documentos:
          acum += int(j)
          if campos[0] == lang1:
            index1[acum].add(campos[1])
          else:
            index2[acum].add(campos[1])
  file.close()

#
# Se cargan los dos diccionarios en las dos lenguas a partir del .dic de la entrada.
#
def cargarDiccionarios(diccionario, lang1, lang2, dic):
  col_dic1 = -1
  col_dic2 = -1
  file = open(diccionario, "r")
  campos = file.readline().strip().split("\t")
  ind = 0
  for j in campos:
    if j == lang1:
      col_dic1 = ind
    elif j == lang2:
      col_dic2 = ind
    ind += 1
  for i in file:
    campos = i.strip().split("\t")
    if len(campos) == 2:
      dic[campos[col_dic2]].append(campos[col_dic1])
  file.close()

#
# En el segundo documento, se traducen las palabras encontradas en el
# diccionario de su idioma por las equivalentes en el otro idioma.
# Esto se hace para todos los documentos encontrados en el segundo idioma.
#
def traducirPalabras(index, dic, dictp, translatedindex):
  for i in index:
    translatedindex[i] = Set([])
    contador = 0
    for word in index[i]:
      if word in dic:
        contador += 1
        translatedindex[i].update(dic[word])
    dictp[i] = contador

def feedDictWithIdenticalWords(index1, index2, dic):
  words_lang1=Set()
  for key, words in index1.items():
    words_lang1=words_lang1.union(words)

  words_lang2=Set()
  for key, words in index2.items():
    words_lang2=words_lang2.union(words)

  for w in words_lang1.intersection(words_lang2):
    dic[w].append(w)

oparser = argparse.ArgumentParser(description="Script that reads the input of bitextor-ett2lett or bitextor-lett2lettr and uses the information about the files in a crawled website to produce an index with all the words in these files and the list of documents in which each of them appear")
oparser.add_argument('idx', metavar='FILE', nargs='?', help='File produced by bitextor-lett2idx containing an index of the different words for every language in the website and the list of documents in which they appear (if undefined, the script will read from the standard input)', default=None)
oparser.add_argument('-d', help='Dictionary containing translations of words for the languages of the website; it is used to compute the overlapping scores which allow to relate documents in both languages)', dest="diccionario", required=True)
oparser.add_argument('-l', help='LETT file; if it is provided, document pair candidates are provided only if they belong to the same domain', dest="lett", required=False, default=None)
oparser.add_argument("--lang1", help="Two-characters-code for language 1 in the pair of languages", dest="lang1", required=True)
oparser.add_argument("--lang2", help="Two-characters-code for language 2 in the pair of languages", dest="lang2", required=True)
options = oparser.parse_args()

index_text1 = defaultdict(set)
index_text2 = defaultdict(set)
dic = defaultdict(list)
lista_palabras = []
encontrados = {}
dict_palabras = {}
translated_index_text2 = {}

cargarDiccionarios(options.diccionario, options.lang1, options.lang2, dic)

if options.idx == None:
  reader = sys.stdin;
else:
  reader = open(options.idx, "r")

rellenarIndex(reader, options.lang1, options.lang2, index_text1, index_text2)

feedDictWithIdenticalWords(index_text1, index_text2, dic)

#
# Para cada par de documentos, tras llamar a traducirPalabras, se realiza una
# interseccion entre ellos y se divide por el numero de palabras traducidas en
# ese documento en la funcion traducirPalabras. El resultado de la interseccion
# entre el numero de palabras traducidas en traducirPalabras dara un
# porcentaje de cuanto se parecen eso documentos. Se muestra una lista con
# los 10 documentos mas parecidos a cada uno de ellos.
#
traducirPalabras(index_text2, dic, dict_palabras, translated_index_text2)

if options.lett != None:
  documents = {}
  readLETT(options.lett, documents)

for i in index_text1:
  if options.lett != None:
    rx = re.match('(https?://)([^/]+)([^\?]*)(\?.*)?', documents[i])
    ihost = rx.group(2)

  parecidos = {}
  for j in index_text2:
    validpair = True
    if options.lett != None:
      rx = re.match('(https?://)([^/]+)([^\?]*)(\?.*)?', documents[j])
      jhost = rx.group(2)
      if jhost != ihost:
        validpair = False
#     c3 = filter(lambda x: x in translated_index_text2[j], index_text1[i])
    if validpair:
      c3 = index_text1[i].intersection(translated_index_text2[j])
      if len(c3) > 0 and int(dict_palabras[j]) > 0:
        max_vocab=max(len(index_text1[i]),len(index_text2[j]))
        min_vocab=min(len(index_text1[i]),len(index_text2[j]))
        num_intersect_words=len(c3)
        num_trans_words_text2=dict_palabras[j]
        parecidos[j] = (float(min_vocab)/float(max_vocab))*(float(num_intersect_words)/float(num_trans_words_text2))

  if len(parecidos) > 0:
    parecidos = sorted(parecidos.items(), key=itemgetter(1), reverse=True)
  encontrados[i] = []
  for j in parecidos:
    encontrados[i].append(str(j[0]) + ":" + str(j[1]))

# Se saca el numero de documento y sus 10 mas parecidos.
for i in encontrados:
  if len(encontrados[i]) > 10:
    contador = 10
  else:
    contador = len(encontrados[i])
  primera = True
  cadena = str(i) + "\t"
  for j in range(contador):
    if primera == True:
      cadena += str(encontrados[i][j])
      primera = False
    else:
      cadena += "\t" + str(encontrados[i][j])
  print cadena
