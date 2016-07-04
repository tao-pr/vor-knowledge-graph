"""
Language trained model examiner script
---
The program loads in the trained models and 
examines the predictors against the specified dataset
---
@author Tao PR (github.com/starcolon)
"""

import sys
import argparse
import numpy as np
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
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--db', type=str, default='vor', help='Specify the database name to read input from.')
arguments.add_argument('--col', type=str, default='text', help='Specify the collection name to read input from.')
arguments.add_argument('--dir', type=str, default='./models', help='Specify the physical directory where to models are located.')
args = vars(arguments.parse_args(sys.argv[1:]))



if __name__ == '__main__':
  db_name         = args['db']
  collection_name = args['col']
  model_dir       = args['dir']
  verbose         = args['verbose']

  # Initialise the mining datasource
  mine_src = MineDB('localhost',db_name,collection_name)
  print(colored('[✔️] Mining datasource initiated...','cyan'))

  # Reads in all models
  clf       = Intent.safe_load(model_dir + PATH_CLF)
  hasher    = TextHash.safe_load(model_dir + PATH_HASHER,n_components=3,stop_words=[],decomposition='SVD')
  tagger    = TextStructure.load(model_dir + PATH_TAGGER)
  
  vectorise = TextHash.hash(hasher)
  predict   = Intent.classify(clf)
  print(colored('[✔️] Classifier models initiated...','cyan'))

  texts, texts2     = tee(mine_src.query({},field='raw'))
  intents, intents0 = tee(mine_src.query({},field='intent'))
  testset_vector    = vectorise(texts)

  pred_intents      = predict(testset_vector)

  # Validate prediction results against ground truth
  for i,i0,text in zip(pred_intents,intents0,texts2):
    if i==i0:
      print(colored('[{0}] : {1}'.format(i0,text),'green'))
    else:
      print(colored('[{0}] : {1} '.format(i0,text),'red'), ' Got => ', i)
  

