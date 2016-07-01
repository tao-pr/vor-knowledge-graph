"""
Language miner
---
The program explores the annotated text set, 
creates a set of intent classifiers and keyword taggers.
---
@author Tao PR (github/starcolon)
"""

import argparse
from termcolor import colored
from pylib.text import structure as TextStructure
from pylib.text import texthasher as TextHash
from pylib.knowledge.graph import Knowledge
from pylib.knowledge.datasource import MineDB

# Paths to models
PATH_HASHER = '/texthash.pkl'
PATH_CLF    = '/intentclf.pkl'
PATH_TAGGER = '/tagger.pkl'

arguments = argparse.ArgumentParser()
arguments.add_argument('--db', type=str, default='vor') # DB source to take
arguments.add_argument('--col', type=str, default='text') # Collection source to take
arguments.add_argument('--outdir', type=str, default='./models') # Where to store output models
args = vars(arguments.parse_args(sys.argv[1:]))

def train_intent_classifiers(mine_src,out_dir):
  def generate_src(src):
    for s in mine_src:
      y = s['intent']
      x = list(filter(lambda _x: len(_x)>0, s['raw'].split(' ')))
      yield (y,x)

  trainset = generate_src(mine_src)

  # Train a new text hasher (vectoriser model)
  model = TextHash.new()
  fit   = TextHash.hash(model,learn=True)
  fit(trainset)
  TextHash.save(model,out_dir + PATH_HASHER)

  # Train a new intent classifier
  clf = None
  
  return model, clf

def train_keyword_taggers(mine_src,out_dir):
  def generate_src(src):
    for s in mine_src:
      y = s['key']
      x = list(filter(lambda _x: len(_x)>0, s['raw'].split(' ')))
      yield (y,x)
  
  trainset = generate_src(mine_src)
  # TAOTODO:


if __name__ == '__main__':
  # Collect arguments
  db_name         = args['db']
  collection_name = args['col']
  output_dir      = args['outdir']

  # Initialise the mining datasource
  mine_src = MineDB('localhost',db_name,collection_name)

  # Train intent classifiers
  clfs, hasher = train_intent_classifiers(mine_src,output_dir)

  # Train keyword taggers
  taggers = train_keyword_taggers(mine_src,output_dir)

