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

  # The unannotated wiki page will not have
  # attribute "annotated"
  for rec in crawl_collection.query({'downloaded': False, '$exists':{'annotated' : False}}):
    yield rec

"""
Prompt the user to annotate the given text sentence
"""
def cli_annotate(ann_collection,text):
  pass # TAOTODO:

if __name__ == '__main__':
  # Prepare a connection to the crawled dataset
  # and the annotation collection respectively
  crawl_collection = init_crawl_collection()
  ann_collection   = init_annotate_collection()

  # Iterate through each unannotated sentence
  [cli_annotate(t,ann_collection) for t in raw_records(crawl_collection)]
