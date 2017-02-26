"""
Knowledge index maker
@author Tao PR (github.com/starcolon)
"""

import os
import sys
import argparse
from termcolor import colored
from nltk.tokenize.punkt import PunktSentenceTokenizer

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--limit', type=int, default=100, help='Maximum number of topics we want to build index')
arguments.add_argument('--modelpath', type=str, default='./models/word2vec.bin', help='Path of the word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))

def collect_wordbag(kb):
  bag = []
  
  # Prepare a naive sentence tokeniser utility
  pst = PunktSentenceTokenizer()

  for wiki in kb.query({'downloaded': True},field=None):
    # Skip empty content or the added one
    if wiki['content'] is None or 'added_to_graph' in wiki:
      continue

    topic_bag = []  
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

        topic_bag.append(s_)

    bag.append(topic)

  return bag


def create_index(kb, model):
  pass

def load_word2vec_model(path):
  if not os.path.isfile(model_path):
    print(colored('[ERROR] word2vec model does not exist.','red'))
    raise RuntimeError('Model does not exist')
  print(colored('[Model] loading binary model.','cyan'))
  return word2vec.WordVectors.from_binary(model_path, encoding='ISO-8859-1')

if __name__ == '__main__':
  # Load word2vec model
  model_path = os.path.realpath(args['modelpath'])
  model = load_word2vec_model(model_path)

  # Initialise a knowledge database
  print(colored('Initialising knowledge graph database...','cyan'))
  kb = Knowledge('localhost','vor','root',args['root'])
  
  # Collect topic wordbag
  wb = collect_wordbag(kb)