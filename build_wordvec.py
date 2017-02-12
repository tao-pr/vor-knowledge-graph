"""
Create word vector space from the crawled dataset
@author TaoPR (github.com/starcolon)
"""

import os
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
arguments.add_argument('--limit', type=int, default=100, help='Maximum number of topics we want to import')
arguments.add_argument('--out', type=str, default='./models/word2vec.bin', help='Output path of the word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))

def model_from_crawl_collection(mineDB, output_path):
  # Dump sentences out of the DB
  print(colored('Exporting crawled data to text file...','cyan'))
  text_path = export_crawl_to_text(mineDB)
  print(colored('[Done]','green'))

  # Train word2vec model
  print(colored('Training word2vec...','cyan'))
  model = create_model(text_path, output_path)
  print(colored('[Done]','green'))
  print('Word2Vec model is saved at : {}'.format(output_path))

  return model

def export_crawl_to_text(mineDB):
  
  # Prepare a naive sentence tokeniser utility
  pst = PunktSentenceTokenizer()

  text_path = os.path.realpath('./mine.txt')

  with codecs.open(text_path, 'w', 'utf-8') as f:
    m = 0
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
          f.write(s_.lower() + '\n')

      m += 1

      if m>=args['limit']:
        print(colored('[Ending] Maximum number of topics reached.','yellow'))
        break

  return text_path

def create_model(input_path, output_path):
  word2vec.word2vec(\
    input_path, \
    output_path, \
    size=10, binary=1, verbose=True)
  assert(os.path.isfile(output_path))
  #return word2vec.load(output_path)
  return word2vec.WordVectors.from_binary(output_path, encoding='ISO-8859-1')

def repl(model):
  while True:
    w = input('Enter a word to try: ')
    indexes, metrics = model.cosine(w)
    print('... Similar words : {}', model.vocab[indexes])

if __name__ == '__main__':
  mineDB = crawl_collection = MineDB('localhost','vor','crawl')
  model = model_from_crawl_collection(mineDB, os.path.realpath(args['out']))

  # Examine the model properties
  if model is None:
    print(colored('[ERROR] Model is empty.','red'))
  else:
    print(colored('[Word2Vec model spec]','cyan'))
    print('... Model shape : {}'.format(model.vectors.shape))
    # Execute a playground REPL
    print(colored('[Word2Vec REPL]:','cyan'))
    repl(model)