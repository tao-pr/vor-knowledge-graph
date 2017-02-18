"""
Study the distribution and relations between words
@author TaoPR (github.com/starcolon)
"""

import sys
import json
import heapq
import os.path
import pyorient
import word2vec
import argparse
import numpy as np
from termcolor import colored
from pybloom_live import ScalableBloomFilter
from pyorient.exceptions import PyOrientSchemaException
from pylib.knowledge.graph import Knowledge
from pylib.knowledge.datasource import MineDB

arguments = argparse.ArgumentParser()
arguments.add_argument('--root', type=str, default=None, help='Supply the OrientDB password for root account.')
arguments.add_argument('--limit', type=int, default=100, help='Maximum number of topics we want to import')
arguments.add_argument('--modelpath', type=str, default='./models/word2vec.bin', help='Path of the word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))


def init_graph():
  # Initialise a knowledge database
  print(colored('Initialising knowledge graph database...','cyan'))
  kb = Knowledge('localhost','vor','root',args['root'])
  return kb

if __name__ == '__main__':
  # Load the word2vec model
  model_path = os.path.realpath(args['modelpath'])
  if not os.path.isfile(model_path):
    print(colored('[ERROR] word2vec model does not exist.','red'))
    raise RuntimeError('Model does not exist')
  print(colored('[Model] loading binary model.','cyan'))
  model = word2vec.WordVectors.from_binary(model_path, encoding='ISO-8859-1')
  
  # Load graph KB
  kb = init_graph()

  # List all top keywords (most connected)
  # (as a dict of [word => count])
  print(colored('Enumurating keywords by their strength of connections...','cyan'))
  top_kws = dict({kw['w']:kw['cnt'] for kw in kb.top_keywords()})

  # Iterate through each topic
  print(colored('Iteration started...','cyan'))
  for topic in kb:
    print(colored('Analysing topic : ','cyan'), topic.title)
    kws = kb.keywords_in_topic(topic.title)

    # List all keywords belong to the current topic
    all_keywords = list(kws)

    for w in all_keywords:

      # TAOTODO: Find a way to remove,skip
      #          weak keywords by some empirical metric
  
      # List top closest neighbours (sorted by cosine similarity)
      indexes, metrics = model.cosine(w)
      closests = model.generate_response(indexes, metrics).tolist()[:6]
      
      # TAOTODO:
      for c in closests:
        pass


