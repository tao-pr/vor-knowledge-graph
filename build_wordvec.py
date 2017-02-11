"""
Create word vector space from the crawled dataset
@author TaoPR (github.com/starcolon)
"""

import sys
import argparse
import word2vec
from termcolor import colored
from nltk.tokenize.punkt import PunktSentenceTokenizer

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
  create_model(text_path, output_path)
  print(colored('[Done]','green'))
  print('Word2Vec model is saved at : {}'.format(output_path))

def export_crawl_to_text(mineDB):
  
  # Prepare a naive sentence tokeniser utility
  pst = PunktSentenceTokenizer()

  text_path = 'mine.txt'

  with open(text_path, 'w') as f:
    for wiki in mineDB.query({'downloaded': True},field=None,skip=start):
      
      # Skip empty content or the added one
      if wiki['content'] is None or 'added_to_graph' in wiki:
        continue

      m = 0
      s = 0
      content = wiki['content']

      # A wiki page may probably comprise of multiple content
      for c in content['contents']:
        # Explode content into sentences
        sentences = pst.sentences_from_text(c)
        print('... content #{} ==> {} sentences extracted.'.format(m, len(sentences)))

        for s in sentences:
          f.write(s + '\n')
          s += 1

      m += 1
      if m>=args['limit']:
        print(colored('[Ending] Maximum number of topics reached.','yellow'))
        break

def create_model(input_path, output_path):
  return word2vec.word2vec(\
    input_path, \
    output_bin, \
    size=10, binary=1, verbose=False)

if __name__ == '__main__':
  mineDB = crawl_collection = MineDB('localhost','vor','crawl')
  model_from_crawl_collection(mineDB, args['out'])