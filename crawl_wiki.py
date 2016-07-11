"""
Wikipedia crawler service
---
The service runs in background and keeps crawling raw knowledge data.
The downloaded data from Wikipedia is senquentially pushed to 
the specified RabbitMQ.
"""

import sys
import asyncio
import argparse
from termcolor import colored
from pylib.spider import wiki as Wiki
from pylib.knowledge.datasource import MineDB

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--depth', type=int, default=128, help='Indicate maximum depth of crawling level')
args = vars(arguments.parse_args(sys.argv[1:]))

"""
Initialise a lazy connection to the crawling record collection
"""
def init_crawl_collection():
  crawl_collection = MineDB('localhost','vor','crawl')
  return crawl_collection

"""
Check whether a wiki has been downloaded
"""
def is_downloaded(crawl_collection,title):
  return crawl_collection.count({'title': title, 'downloaded': True})>0

"""
Mark a wiki page as downloaded
"""
def mark_as_downloaded(crawl_collection,title):
  if crawl_collection.count({'title': title})>0:
    crawl_collection.update({'title': title},{'$set':{'downloaded':True}})
  else:
    crawl_collection.insert({'title': title, 'downloaded': True, 'rels':[]})


def list_crawl_pending(crawl_collection):
  return [t['title'] for t in crawl_collection.query({'downloaded': False})]

"""
Add a fresh new wiki page as yet to be downloaded
"""
def add_pending(crawl_collection,title):
  crawl_collection.insert({'title': title, 'downloaded': False})

"""
Execute a crawling subprocess on the destination wiki page title
"""
@asyncio.coroutine
def crawl(crawl_collection,title,depth):
  pass # TAOTODO:

if __name__ == '__main__':

  depth = args['depth']

  # Prepare the crawling record handler
  crawl_collection = init_crawl_collection()

  # Load all list of pending wiki pages
  pendings = list_crawl_pending(crawl_collection)

  # If there is no pending list, add a default seed
  if len(pendings)==0:
    pendings.append('Jupiter')

  # For each of the pending list, spawns a new crawler subprocess
  # to download those data
  for title in pendings:
    print(colored('Pending for crawling: ','green'), title)
    crawl(crawl_collection, title, depth)

