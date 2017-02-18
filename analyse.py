"""
Study the distribution and relations between words
@author TaoPR (github.com/starcolon)
"""

import json
import os.path
import pyorient
import numpy as np
from termcolor import colored
from pybloom_live import ScalableBloomFilter
from pyorient.exceptions import PyOrientSchemaException
from pylib.knowledge.graph import Knowledge
from pylib.knowledge.datasource import MineDB

def init_crawl_collection():
  crawl_collection = MineDB('localhost','vor','crawl')
  return crawl_collection

def load_word2vec(model_path):
  pass

def iter_crawl_collection(minDB):
  # TAOTOREVIEW: Following loop is entirely duplicated from
  #               [build_wordvec.py], may need refactoring
  for wiki in mineDB.query({'downloaded': True},field=None):
      
    # Skip empty content or the added one
    if wiki['content'] is None or 'added_to_graph' in wiki:
      continue

    content = wiki['content']

    # A wiki page may probably comprise of multiple content
    for c in content['contents']:
      # Explode content into sentences
      sentences = pst.sentences_from_text(c)
      print('... content #{} ==> {} sentences extracted.'.format(m, len(sentences)))

      for s in sentences:
        # Cleanse the sentence
        s_ = cleanse(s)
        # Filter out noise by length
        if len(s_)<5 or len(s_.split(' '))<3:
          continue

        yield s.lower()

