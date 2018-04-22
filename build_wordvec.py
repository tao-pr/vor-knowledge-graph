"""
Create word vector space from the crawled dataset
@author TaoPR (github.com/starcolon)

---

@input    : topic sentences (mine.txt)
@outputs  : wordvector model
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
from pylib.text.cleanser import *

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--out', type=str, default='./models/word2vec.bin', help='Output path of the word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))

def model_from_mine(output_path):
  # Train word2vec model
  print(colored('Training word2vec...','cyan'))
  model = create_model('mine.txt', output_path)
  print(colored('[Done]','green'))
  print('Word2Vec model is saved at : {}'.format(output_path))

  return model

def create_model(input_path, output_path):
  word2vec.word2vec(\
    input_path, \
    output_path, \
    size=10, binary=1, verbose=True)
  assert(os.path.isfile(output_path))
  return word2vec.WordVectors.from_binary(output_path, encoding='ISO-8859-1')

def repl(model):
  while True:
    w = input('Enter a word to try: ')
    indexes, metrics = model.cosine(w)
    print('... Similar words : {}', model.vocab[indexes])

if __name__ == '__main__':
  model = model_from_mine(os.path.realpath(args['out']))

  # Examine the model properties
  if model is None:
    print(colored('[ERROR] Model is empty.','red'))
  else:
    print(colored('[Word2Vec model spec]','cyan'))
    print('... Model shape : {}'.format(model.vectors.shape))
    # Execute a playground REPL
    print(colored('[Word2Vec REPL]:','cyan'))
    repl(model)