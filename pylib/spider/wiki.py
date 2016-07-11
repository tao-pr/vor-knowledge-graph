"""
Wikipedia page crawler and scraper
"""

from . import crawler

def download_wiki(url):
  pass

def wiki_title(page):
  return page.find('h1#firstHeading').text()

"""
Scrape the main article content from the specified 
wikipedia page
"""
def wiki_contents(page):
  return [] # TAOTODO:

"""
Scrape all related links (to other wiki pages)
from the current wikipedia page
"""
def wiki_rels(page):
  links = []
  for li in page.find('ul li'):
    link = li.find('a')
    # The item must locate a link to another wiki page
    links.push(link.attr('href'))

  return links