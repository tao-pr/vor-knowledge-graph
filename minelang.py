"""
Language miner
---
The program explores the annotated text set, 
creates a set of intent classifiers and keyword taggers.
---
@author Tao PR (github/starcolon)
"""

import sys
import argparse
from itertools import tee
from termcolor import colored
from pylib.text import structure as TextStructure
from pylib.text import texthasher as TextHash
from pylib.text import intent as Intent
from pylib.knowledge.graph import Knowledge
from pylib.knowledge.datasource import MineDB

# Paths to models
PATH_HASHER = '/texthash.opr'
PATH_CLF    = '/intentclf.opr'
PATH_TAGGER = '/tagger.opr'

arguments = argparse.ArgumentParser()
arguments.add_argument('--db', type=str, default='vor') # DB source to take
arguments.add_argument('--col', type=str, default='text') # Collection source to take
arguments.add_argument('--outdir', type=str, default='./models') # Where to store output models
args = vars(arguments.parse_args(sys.argv[1:]))

def train_intent_classifiers(mine_src,out_dir):
  def generate_raw_text(src):
    for s in mine_src:
      x = list(filter(lambda _x: len(_x)>0, s['raw'].split(' ')))
      yield x

  def generate_labels(src):
    for s in mine_src:
      y = s['intent']
      yield y

  textset, textset2 = tee(generate_raw_text(mine_src))
  labels            = generate_labels(mine_src)

  # Train a new text hasher (vectoriser model)
  model = TextHash.new()
  fit   = TextHash.hash(model,learn=True)
  fit(textset)
  TextHash.save(model, out_dir + PATH_HASHER)

  # Train a new intent classifier
  clf   = Intent.new()
  train = Intent.train(clf)
  train(trainset,textset2,labels)
  Intent.save(clf, outdir + PATH_CLF)

  return model, clf

def train_keyword_taggers(mine_src,out_dir):
  
  def generate_trainset(src):
    for s in mine_src:
      x   = list(filter(lambda _x: len(_x)>0, s['raw'].split(' ')))
      y   = src['key'] # Tagged single word as a keyword
      iy  = x.index(y) if len(y)>0 else -1
      pos = TextStructure.pos_tag(x)
      yield (pos[iy],pos)

  def generate_x(trainset):
    for y,x in trainset:
      yield x

  def generate_y(trainset):
    for y,x in trainset:
      yield y
  
  trainset, trainset2 = tee(generate_trainset(mine_src))
  labels, pos         = generate_y(trainset), generate_x(trainset2)

  # Train the tagger models with given sets of labels and POS tags
  tagger = TextStructure.train_keyword_tagger(labels,pos)
  TextStructure.save(tagger,outdir + PATH_TAGGER)  
  return tagger


if __name__ == '__main__':
  # Collect arguments
  db_name         = args['db']
  collection_name = args['col']
  output_dir      = args['outdir']

  # Initialise the mining datasource
  mine_src = MineDB('localhost',db_name,collection_name)
  print(colored('[✔️] Mining datasource initiated...','cyan'))

  # Train intent classifiers
  print(colored('[✔️] Intent classifier training started...','cyan'))
  hasher, clf = train_intent_classifiers(mine_src.query({}),output_dir)
  print(colored('[done]','green'))

  # Train keyword taggers
  print(colored('[✔️] Keyword tagger training started...','cyan'))
  taggers = train_keyword_taggers(mine_src.query({}),output_dir)
  print(colored('[done]','green'))
