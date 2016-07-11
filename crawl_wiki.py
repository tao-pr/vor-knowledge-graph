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
arguments.add_argument('--depth', type=int, default=4, help='Indicate maximum depth of crawling level')
args = vars(arguments.parse_args(sys.argv[1:]))

"""
Initialise a lazy connection to the crawling record collection
"""
def init_crawl_collection():
  crawl_collection = MineDB('localhost','vor','crawl')
  return crawl_collection

"""
Save the content of the wikipedia page
"""
def save_content(crawl_collection,title,content):
  if crawl_collection.count({'title': title})>0:
    crawl_collection.update(
      {'title': title},
      {'$set':{'downloaded':True, 'content': content}}
    )
  else:
    crawl_collection.insert({'title': title, 'downloaded': True, 'content':content})

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
    crawl_collection.insert({'title': title, 'downloaded': True, 'content':None})


def list_crawl_pending(crawl_collection):
  return [t['title'] for t in crawl_collection.query({'downloaded': False})]

"""
Add a fresh new wiki page as yet to be downloaded
"""
def add_pending(crawl_collection,title):
  if crawl_collection.count({'title': title})==0:
    crawl_collection.insert({'title': title, 'downloaded': False, 'content':None})

"""
Execute a crawling subprocess on the destination wiki page title
"""
@asyncio.coroutine
def crawl(crawl_collection,title,depth,verbose):
  loop = asyncio.get_event_loop()
  
  # Skip if downloaded
  if is_downloaded(crawl_collection, title):
    print('Already downloaded, skipped.')
    loop.close()
    return

  # Crawl the content
  add_pending(crawl_collection, title)

  if depth>0:
    content = Wiki.download_wiki('http://en.wikipedia.org/' + title, verbose)
    
    # Store the downloaded content in MongoDB
    save_content(crawl_collection, title, content)

    # Now recursively download the related links
    subtasks = []
    for rel in content['rels']:
      print('#',depth-1,colored(' Pending for crawling: ','green'), rel)
      subtasks.append(asyncio.async(
        crawl(crawl_collection, rel, depth-1, verbose)
      ))

    loop.run_until_complete(asyncio.wait(subtasks))

  loop.close()


if __name__ == '__main__':

  depth = args['depth']
  print(colored('# Max depth to run: ','cyan'), depth)
  loop  = asyncio.get_event_loop()

  # Prepare the crawling record handler
  crawl_collection = init_crawl_collection()

  # Load all list of pending wiki pages
  pendings = list_crawl_pending(crawl_collection)

  # If there is no pending list, add a default seed
  if len(pendings)==0:
    pendings.append('wiki/Jupiter')

  # For each of the pending list, spawns a new crawler subprocess
  # to download those data
  tasks = []
  for title in pendings:
    print(colored('Pending for crawling: ','green'), title)
    tasks.append(asyncio.async(
      crawl(crawl_collection, title, depth, args['verbose'])
    ))

  # Wait until all top-level async crawling tasks end
  loop.run_until_complete(asyncio.wait(tasks))
  loop.close()


