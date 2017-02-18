"""
Study the distribution and relations between words
@author TaoPR (github.com/starcolon)
"""

import sys
import json
import os.path
import pyorient
import word2vec
import argparse
import numpy as np
from termcolor import colored
from collections import Counter
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
  top_kws = dict({kw.w : kw.cnt for kw in kb.top_keywords()})

  # Iterate through each topic
  print(colored('Iteration started...','cyan'))
  for topic in kb:
    print(colored('Analysing topic : ','cyan'), topic.title)
    kws = kb.keywords_in_topic(topic.title)

    # T: G(t,W)
    # ----------------
    # Definition of topic set [T]
    # [t] is a topic title
    # [W] is a set of keywords

    # List all keywords [W] belong to the current topic
    all_keywords = list([kw.w.lower().strip() for kw in kws])

    # for w <- W
    for w in all_keywords:

      # List all topics this [w] belong to
      other_parents = Counter(kb.topics_which_have(w))
      top_other_parents = sorted(other_parents, key=other_parents.get, reverse=True)

      # Let neighbours [N] of [w] defined by
      #
      # N(w) : {w' | (w.w')/(norm(w,w')) > threshold}
  
      # List top closest neighbours (sorted by cosine similarity)
      try:
        indexes, metrics = model.cosine(w)
        neighbours = [(c,score) for (c,score) in \
          model.generate_response(indexes, metrics).tolist()\
          if score>0.93] # Mimimally accepted cosine similarity
        
        # TAOTODO: Single out strong & unique keywords
        #         which belong to this topic
        #         but potentially SCARCELY occur in any other topics

        for c,score in neighbours:
          pass

      except Exception:
        print(colored('... No definition in word2vec model : ','yellow'), w)

