"""
Indexed content segmentation
@author TaoPR (github.com/starcolon)
---
Categorise the entire crawled content into segments
based on word2vec vectors
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
  for k in indexDB.iterate_keywords():
    n_skip = 0
    if k.w not in map_keyword_to_feature:
      v = model[k.w]
      # TAOTODO: Make sure word2vec keywords are consistent
      # with the OrientDB index
    else:
      n_skip += 1

  print()
  print("{} keywords skipped".format(n_skip))
  print("{} keywords collected".format(len(map_keyword_to_feature)))
  print()

  return # TAODEBUG:

  # Iterate through topics, create feature vectors
  for t in indexDB:
    print(t.title)
    for kw in indexDB.iterate_index(t.title):
      k = kw.w
      w = indexDB.get_weight_of_edge(t._rid, kw._rid)
      # TAOTODO:
  pass

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

  # Initialise a knowledge database
  print(colored('Initialising index database...','cyan'))
  index = Knowledge('localhost','vorindex','root',args['root'])

  cluster = model_from_index(index, model)

  # Save model
  pass