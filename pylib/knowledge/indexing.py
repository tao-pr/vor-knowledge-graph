"""
Solr interface
@author Tao PR (github.com/starcolon)
"""

import os
import pysolr
from shutil import copyfile
from termcolor import colored

LOCAL_PREFIX  = 'http://localhost:8983/solr/'
SOLR_PATH     = os.getenv('SOLR','/usr/local/solr/solr-5.3.1')
SOLR_COLLECTION_PATH = '{}/server/solr/vor'.format(SOLR_PATH)
SCRIPT_PATH   = os.path.dirname(os.path.realpath(__file__))
REPO_PATH     = os.path.abspath('{}/../../'.format(SCRIPT_PATH))

class IndexDomain:
  def __init__(self, solr_svr_addr=LOCAL_PREFIX)
    self.solr = pysolr.Solr(url, timeout=8)

  """
  Create a new Solr index if does not exist
  """
  def create_index():
    if not is_index_exist:
      print(colored('[Index] No existing collection found','yellow'))
      print(colored('[Index] Creating a fresh new','cyan'))
      for path in ['/conf','/data']:
        os.makedirs(SOLR_COLLECTION_PATH + path)
        # Copy initial Solr config files across
        srcdir = REPO_PATH + '/solr' + path
        for file in os.listdir(srcdir):
          srcpath = srcdir + '/' + file
          if os.path.isfile(srcpath):
            destpath = SOLR_COLLECTION_PATH + path + '/' + file
            print('... copying {}'.format(path + '/' + file))
            copyfile(srcpath, destpath) # TAOTODO:
      print('[done] all collection files initialised')

  """
  Dirty way of checking whether the collection exists
  """
  def is_index_exist():
    return os.path.isdir(SOLR_COLLECTION_PATH) and 
      os.path.isdir(SOLR_COLLECTION_PATH + '/conf') and 
      os.path.isdir(SOLR_COLLECTION_PATH + '/data') and 
      os.path.isfile(SOLR_COLLECTION_PATH + 'core.properties')

  def add_to_index(node):
    pass

  def search(phrases,max_results=25):
    for res in self.solr.search(query,**{'rows': max_results}):
      yield res