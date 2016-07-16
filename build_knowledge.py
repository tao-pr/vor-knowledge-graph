"""
Knowledge graph builder
@author TaoPR (github.com/starcolon)
---
Process the entire bulk of the crawled dataset (MongoDB)
and potentially create a knowledge graph (OrientDB)
"""

import sys
import argparse
from termcolor import colored
from nltk.tokenize.punkt import PunktSentenceTokenizer
from pylib.knowledge.graph import Knowledge
from pylib.text import structure as TextStructure
from pylib.text.pos_tree import PatternCapture
from pylib.knowledge.datasource import MineDB

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--start', type=int, default=0, help='Starting index of the crawling record to annotate.')
arguments.add_argument('--root', type=str, default=None, help='Supply the OrientDB password for root account.')
args = vars(arguments.parse_args(sys.argv[1:]))

"""
Initialise a lazy connection to the crawling record collection
"""
def init_crawl_collection():
  crawl_collection = MineDB('localhost','vor','crawl')
  return crawl_collection


def iter_topic(crawl_collection,start):
  
  # Prepare a naive sentence tokeniser utility
  pst = PunktSentenceTokenizer()
  
  n = 0
  
  for wiki in crawl_collection.query({'downloaded': True},field=None,skip=start):
    # Explode topic content into sentences
    if wiki['content'] is None:
      continue
    m = 0
    content = wiki['content']
    print(colored('[Extracting wiki] : ','cyan'), content['title'])
    # A wiki page may probably comprise of multiple content
    for c in content:
      # Explode a long topic into list of sentences
      sentences = pst.sentences_from_text(c)
      for s in sentences:
        m += 1
        yield (content['title'],s)

    # TAOTODO: After all sentences are processed,
    # mark the current wiki record as 'processed'

    n += 1
    print(content['title'] + " processed with {0} nodes.".format(m))
    print(colored("{0} wiki documents processed so far...".format(n),'blue'))


if __name__ == '__main__':

  # Initialise a knowledge database
  if args['verbose']:
    print(colored('Initialising knowledge graph database...','cyan'))
  kb = Knowledge('localhost','vor','root',args['root'])

  # Load existing pos patterns
  if args['verbose']:
    print(colored('Loading POS patterns...','cyan'))
  patterns = PatternCapture()
  patterns.load('./pos-patterns')

  # Initialise a crawling dataset connection
  if args['verbose']:
    print(colored('Initialising wikipedia crawling collection...'))
  crawl_collection = init_crawl_collection()

  # Iterate through the crawling database
  if args['verbose']:
    print(colored('Starting...','magenta'))
  for topic,sentence in iter_topic(crawl_collection,args['start']):
    # Break the sentence into knowledge nodes
    pos      = TextStructure.pos_tag(sentence)
    kb_nodes = patterns.capture(pos)

    # Create a set of knowledge links
    for node in kb_nodes:
      kb.add(topic,node,'related')
      for node_ in filter(lambda n: n != node,kb_nodes):
        kb.add(node,node_,'friend')
  

