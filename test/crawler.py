"""
Spider / crawler test suite
"""

import re
from pprint import pprint
from pylib.spider import wiki

def test_wiki_crawl():
  wiki_url = 'https://en.wikipedia.org/wiki/Celery'
  content  = wiki.download_wiki(wiki_url,verbose=True)

  celery_first_content = ["Celery",
    "(Apium graveolens",
    "), a marshland plant variety",
    "in the family Apiaceae",
    ", has been cultivated as a vegetable",
    "since antiquity. Depending on location and cultivar, either its stalks, leaves, or hypocotyl",
    "are eaten and used in cooking."
  ]

  assert content['title'] == 'Celery'
  assert len(content['contents']) > 0
  assert content['contents'][0] == "\n".join(celery_first_content)
  assert content['rels'][:3] == [
    '/wiki/Microgram',
    '/wiki/Milligram',
    '/wiki/International_unit'
  ]