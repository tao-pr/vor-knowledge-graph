"""
Make pos patterns which represent knowledge node
from the downloaded wikipedia topics.
"""

import sys
import argparse
from termcolor import colored
from pylib.text import structure as TextStructure
from pylib.text.pos_tree import PatternCapture
from pylib.knowledge.datasource import MineDB
from nltk.tokenize.punkt import PunktSentenceTokenizer

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--start', type=int, default=0, help='Starting index of the crawling record to annotate.')
args = vars(arguments.parse_args(sys.argv[1:]))

"""
Initialise a lazy connection to the crawling record collection
"""
def init_crawl_collection():
  crawl_collection = MineDB('localhost','vor','crawl')
  return crawl_collection

"""
Initialise an annotation collection
"""
def init_annotate_collection():
  ann_collection = MineDB('localhost','vor','annotate')
  return ann_collection

"""
Iterate through the unannotated recordset in the crawled collection,
and generate each of the sentence from the topic.
"""
def raw_records(crawl_collection,start):

  # Prepare a naive sentence tokeniser utility
  pst = PunktSentenceTokenizer()

  for rec in crawl_collection.query({'downloaded': True},field=None,skip=start):
    _id     = rec['_id']
    if rec['content'] is None:
      continue
    content = rec['content']['contents']
    # A wiki page may probably comprise of multiple content
    for c in content:
      # Explode a long topic into list of sentences
      sentences = pst.sentences_from_text(c)
      for s in sentences:
        yield (_id,s)


"""
Prompt the user to annotate the given text sentence
"""
def cli_annotate(crawl_collection,ann_collection):
  # Load existing pos patterns
  patterns = PatternCapture()
  patterns.load('./pos-patterns')

  print(colored('Existing patterns :','green'))
  print(patterns.join(' , '))

  def annotate(_id,text):
    # Analyse the POS structure of the sentence
    tokens = text.split(' ')
    pos    = TextStructure.pos_tag(tokens)
    TextStructure.tag_with_color(tokens)

    # Test POS pattern parsing and show the result
    print(patterns.capture(pos))

    # Extract the pure list of POS
    pos_ = [tag for t,tag in pos]

    # POS token sample form: NN-JJ,NN,NN-NNS
    nodes = input(colored("POS token patterns: ","cyan"))

    if len(nodes)>0:
      # Add patterns to the registry if not yet
      nodes = [n.strip() for n in nodes.split(',')]
      for n in nodes:
        if n not in patterns:
          print(colored('New pattern added: ','green'), n)
          patterns.append(n)

      # Save right away
      patterns.save('./pos-patterns')
      print("Patterns saved!")

  return annotate

if __name__ == '__main__':

  # Prepare a connection to the crawled dataset
  # and the annotation collection respectively
  crawl_collection = init_crawl_collection()
  ann_collection   = init_annotate_collection()

  # Make an annotator function
  annotate = cli_annotate(crawl_collection, ann_collection)

  # Iterate through each unannotated sentence
  [annotate(_id,t) for (_id,t) in raw_records(crawl_collection,args['start'])]
