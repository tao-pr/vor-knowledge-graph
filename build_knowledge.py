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
from pybloom_live import ScalableBloomFilter

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--start', type=int, default=0, help='Starting index of the crawling record to annotate.')
arguments.add_argument('--root', type=str, default=None, help='Supply the OrientDB password for root account.')
arguments.add_argument('--limit', type=int, default=100, help='Maximum number of topics we want to import')
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
    
    # Skip empty content or the added one
    if wiki['content'] is None or 'added_to_graph' in wiki:
      continue

    m = 0
    content = wiki['content']
    
    if args['verbose']:
      print(colored('[Extracting wiki] : ','cyan'), content['title'])
    
    # A wiki page may probably comprise of multiple content
    for c in content['contents']:
      # Explode a long topic into list of sentences
      sentences = pst.sentences_from_text(c)
      for s in sentences:
        m += 1
        yield (content['title'],s.split(' '))

    # After all sentences are processed,
    # mark the current wiki record as 'processed'
    crit = {'_id': wiki['_id']}
    crawl_collection.update(crit, {'$set':{'added_to_graph':True}})

    n += 1
    if args['verbose']:
      print(content['title'] + " processed with {0} nodes.".format(m))
      print(colored("{0} wiki documents processed so far...".format(n),'blue'))


if __name__ == '__main__':

  # Initialise a knowledge database
  print(colored('Initialising knowledge graph database...','cyan'))
  kb = Knowledge('localhost','vor','root',args['root'])
  kb.clear()

  # Load existing pos patterns
  print(colored('Loading POS patterns...','cyan'))
  patterns = PatternCapture()
  patterns.load('./pos-patterns')

  # Initialise a crawling dataset connection
  print(colored('Initialising wikipedia crawling collection...','cyan'))
  crawl_collection = init_crawl_collection()

  # Iterate through the crawling database
  n = 0
  print(colored('Iterating over crawling database...','cyan'))
  bf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
  for topic,sentence in iter_topic(crawl_collection,args['start']):
    
    # Check if the number of processed topic exceed the limit?
    if topic not in bf:
      bf.add(topic)
      if len(bf) > args['limit']:
        print(colored('[Topics limit reached] ... BYE','cyan'))
        sys.exit(0)

    # Break the sentence into knowledge nodes
    pos      = TextStructure.pos_tag(sentence)
    kb_nodes = patterns.capture(pos)  

    if args['verbose']:
      print(kb_nodes)

    # Create a set of knowledge links
    kb.add(topic,kb_nodes,args['verbose'])

    n += 1
    if n%100 == 0 and n>0:
      print('... {} topics done so far.'.format(n))
  

