"""
Word vectorisation
@author TaoPR (github.com/starcolon)
"""

from termcolor import colored
import word2vec

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
  for wiki in mineDB.query({'downloaded': True},field=None,skip=start):
    
    # Skip empty content or the added one
    if wiki['content'] is None or 'added_to_graph' in wiki:
      continue

    m = 0
    content = wiki['content']

def create_model(input_path, output_path):
  return word2vec.word2vec(\
    input_path, \
    output_bin, \
    size=10, binary=1, verbose=False)