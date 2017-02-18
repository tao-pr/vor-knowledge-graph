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
  # (only top 300)
  top_kws = [kw for kw in kb.top_keywords()][:300]
  top_kw_pool = set([kw['w'] for kw in top_kws])

  # Iterate through each topic
  connections = []
  for topic in kb:
    print(colored('Analysing topic : ','cyan'), topic.title)
    kws = kb.keywords_in_topic(topic.title)
    for w in kws:
      # List all neighbour keywords of [kw]
      neighbours = kb.related_keywords(w)

      # List all closest neighbors (by word2vec cosine similarity) 
      # of [kw]
      indexes, metrics = model.cosine(w)
      similars = model.vocab[indexes]
      
      # TAOTODO:


