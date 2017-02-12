"""
Play with word2vec model
@author TaoPR (github.com/starcolon)
"""

import os
import sys
import argparse
import word2vec
from termcolor import colored

arguments = argparse.ArgumentParser()
arguments.add_argument('--modelpath', type=str, default='./models/word2vec.bin', help='Path of the word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))

def repl(model):
  print(colored('[Model] Loaded:','cyan'))
  print('... Model shape : {}', model.vectors.shape)
  pass

if __name__ == '__main__':
  # Load the word2vec model
  model_path = os.path.realpath(args['modelpath'])
  if not os.path.isfile(model_path):
    print(colored('[ERROR] word2vec model does not exist.','red'))
    raise RuntimeError('Model does not exist')
  print(colored('[Model] loading binary model.','cyan'))
  model = word2vec.WordVectors.from_binary(model_path, encoding='ISO-8859-1')
  repl(model)