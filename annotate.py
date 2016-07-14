"""
Annotate the wiki dataset with knowledge link
----
The script walks through the downloaded wikipedia dataset in MongoDB,
prompts the user to annotate each of the extracted sentence with 
the highlighted knowledge links.
"""

import sys
import argparse
from termcolor import colored
from pylib.text import structure as TextStructure
from pylib.knowledge.datasource import MineDB
from nltk.tokenize.punkt import PunktSentenceTokenizer

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
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
def raw_records(crawl_collection):

  # Prepare a naive sentence tokeniser utility
  pst = PunktSentenceTokenizer()

  # The unannotated wiki page will not have
  # attribute "annotated"
  for rec in crawl_collection.query({'downloaded': False, '$exists':{'annotated' : False}}):
    _id     = rec['_id']
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
  def annotate(_id,text):
    # Annotate and mark the wiki ID as annotated
    pass # TAOTODO:

  return annotate

if __name__ == '__main__':
  # Prepare a connection to the crawled dataset
  # and the annotation collection respectively
  crawl_collection = init_crawl_collection()
  ann_collection   = init_annotate_collection()

  # Make an annotator function
  annotate = cli_annotate(crawl_collection, ann_collection)

  # Iterate through each unannotated sentence
  [annotate(_id,t) for (_id,t) in raw_records(crawl_collection)]
