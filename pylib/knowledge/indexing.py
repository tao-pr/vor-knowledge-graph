"""
Solr interface
@author Tao PR (github.com/starcolon)
"""

import pysolr
from termcolor import colored

LOCAL_PREFIX  = 'http://localhost:8983/solr/'

class IndexDomain:
  def __init__(self, solr_svr_addr=LOCAL_PREFIX)
    self.solr = pysolr.Solr(url, timeout=8)

  """
  Create a new Solr index if does not exist,
  otherwise, load the existing
  """
  def create_index(collection_name):
    # TAOTODO: Check whether the collection already exists

    # If the collection is not there,
    # create a new one
    pass

  def is_index_exist(collection_name):
    pass

  def add_to_index(node):
    pass

  def search(phrases,max_results=25):
    for res in self.solr.search(query,**{'rows': max_results}):
      yield res