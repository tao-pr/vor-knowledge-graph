"""
Indexed content segmentation
@author TaoPR (github.com/starcolon)
---
Build content segmentation model

---

@inputs   : wordvector model
          : knowledge data (OrientDB : vor)
@outputs  : segmentation model
"""

import os
import re
import sys
import codecs
import argparse
import word2vec
from termcolor import colored
from nltk.tokenize.punkt import PunktSentenceTokenizer
from pylib.knowledge.datasource import MineDB
from pylib.knowledge.graph import Knowledge
from pylib.text.cleanser import *

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--root', type=str, default=None, help='Supply the OrientDB password for root account.')
arguments.add_argument('--limit', type=int, default=100, help='Maximum number of topics we want to import')
arguments.add_argument('--out', type=str, default='./models/segments.ml', help='Segmentation model path to save.')
arguments.add_argument('--modelpath', type=str, default='./models/word2vec.bin', help='Path of the input word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))

def model_from_index(indexDB, model):
  # Iterate through entire word space, create word2vec feature space
  map_keyword_to_feature = dict()
  print(colored('Iterating through topics...','cyan'))
  n = 0
  for topic in indexDB:
    n += 1
    kws = list(indexDB.keywords_in_topic(topic.title, with_edge_count=True))

    pass

    if n > args['limit']:
      break


  # for k in indexDB.iterate_keywords():
  #   n_skip = 0
  #   if k.w not in map_keyword_to_feature and k.w in model:
  #     v = model[k.w]
  #     map_keyword_to_feature[k.w] = v
  #   else:
  #     n_skip += 1

  #   if len(map_keyword_to_feature) > args['limit']:
  #     break

  print()
  print("{} keywords collected".format(len(map_keyword_to_feature)))
  print("{} MB used as a storage of keyword vectors".format(sys.getsizeof(map_keyword_to_feature)/1024**2))
  print()

  return # TAODEBUG:

def load_word2vec_model(path):
  if not os.path.isfile(model_path):
    print(colored('[ERROR] word2vec model does not exist.','red'))
    raise RuntimeError('Model does not exist')
  print(colored('[Model] loading binary model.','cyan'))
  return word2vec.WordVectors.from_binary(model_path, encoding='ISO-8859-1')


if __name__ == '__main__':
  # Load word2vec model
  model_path = os.path.realpath(args['modelpath'])
  model = load_word2vec_model(model_path)
  # TAODEBUG: When upgraded word2vec, following has to change to [model.wv.vocab]
  print('Word2vec model loaded ({} keywords)'.format(len(model.vocab)))

  # Initialise a knowledge database
  print(colored('Initialising index database...','cyan'))
  index = Knowledge('localhost','vorindex','root',args['root'])

  cluster = model_from_index(index, model)

  # Save model
  pass