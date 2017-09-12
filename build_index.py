"""
Knowledge index maker
@author Tao PR (github.com/starcolon)
"""

import numpy as np
import os
import sys
import argparse
import word2vec
from termcolor import colored
from collections import Counter
from nltk.tokenize.punkt import PunktSentenceTokenizer
from pylib.knowledge.graph import Knowledge
from pylib.knowledge.datasource import MineDB
from pylib.text.cleanser import *

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--limit', type=int, default=100, help='Maximum number of topics we want to build index')
arguments.add_argument('--root', type=str, default=None, help='Supply the OrientDB password for root account.')
arguments.add_argument('--modelpath', type=str, default='./models/word2vec.bin', help='Path of the word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))

def collect_wordbag(kb, model):
  print(colored('Iterating through topics...','cyan'))
  n = 0
  for topic in kb:
    n += 1
    kws = list(kb.keywords_in_topic(topic.title, with_edge_count=True))
    
    # Frequency of [w] in the current topic
    cnt0 = Counter([kw.w for kw in kws])
    # Normalise with global frequency
    norm = np.linalg.norm(list(cnt0.values()))
    for word in kws:
      cnt0[word.w] *= word.freq / norm

    # Generate similar words with word2vec
    cnt = {}
    for word, freq in cnt0.items():
      w_ = cleanse(''.join(filter(str.isalnum, word)))
      cnt[w_] = freq
      try:
        indexes, metrics = model.cosine(w_)
        synnonyms = model.generate_response(indexes, metrics).tolist()
        for syn, confidence in synnonyms:
          if confidence < 0.85: break
          cnt[syn] = confidence * freq
      except:
        pass

    yield (n,topic,cnt)
    if n>=args['limit']: break

def load_word2vec_model(path):
  if not os.path.isfile(model_path):
    print(colored('[ERROR] word2vec model does not exist.','red'))
    raise RuntimeError('Model does not exist')
  print(colored('[Model] loading binary model.','cyan'))
  return word2vec.WordVectors.from_binary(model_path, encoding='ISO-8859-1')

def add_to_index(index,bag):
  print('------------------------------------')
  n, topic, cnt = bag
  print('...Constructing : {}'.format(colored(topic.title,'magenta')))

  def filter_non_alpha(w):
    return ''.join(filter(str.isalnum, w))

  words, weights = zip(*[(filter_non_alpha(w),weight) for w,weight in cnt.items()])
  index.add(topic.title, words, weights, verbose=False)

if __name__ == '__main__':
  # Load word2vec model
  model_path = os.path.realpath(args['modelpath'])
  model = load_word2vec_model(model_path)

  # Initialise a knowledge database
  print(colored('Initialising knowledge graph database...','cyan'))
  kb = Knowledge('localhost','vor','root',args['root'])
  
  # Collect topic wordbag
  wb = collect_wordbag(kb, model)

  # Create knowledge index
  index = Knowledge('localhost','vorindex','root',args['root'])
  index.clear()
  for bag in wb:
    add_to_index(index, bag)

  print(colored('[DONE] all process ended','green'))