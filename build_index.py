"""
Knowledge index maker
@author Tao PR (github.com/starcolon)
"""

import os
import sys
import argparse
import word2vec
from termcolor import colored
from collections import Counter
from pylib.knowledge.graph import Knowledge
from pylib.knowledge.datasource import MineDB
from nltk.tokenize.punkt import PunktSentenceTokenizer

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--limit', type=int, default=100, help='Maximum number of topics we want to build index')
arguments.add_argument('--root', type=str, default=None, help='Supply the OrientDB password for root account.')
arguments.add_argument('--modelpath', type=str, default='./models/word2vec.bin', help='Path of the word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))

def collect_wordbag(kb):
  bag = []
  
  print(colored('Iterating through topics...','cyan'))
  n = 0
  for topic in kb:
    n += 1
    cnt = Counter([kw for kw in kb.keywords_in_topic(topic)])
    bag.append(cnt)
    print('...#{} {}'.format(n, cnt))
    print('--------------')

  return bag


def create_index(kb, model):
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
  print(colored('Initialising knowledge graph database...','cyan'))
  kb = Knowledge('localhost','vor','root',args['root'])
  
  # Collect topic wordbag
  wb = collect_wordbag(kb)