"""
Spider / crawler test suite
"""

from pylib.spider import wiki

def test_wiki_crawl():
  wiki_url = 'https://en.wikipedia.org/wiki/Celery'
  content  = wiki.download_wiki(wiki_url,verbose=True)

  assert content['title'] == 'Celery'
  # TAOTODO: 