"""
Wikipedia page crawler and scraper
"""

from . import crawler

def download_wiki(url,verbose=False):
  selector = [
    ('title', wiki_title),
    ('contents', wiki_contents),
    ('rels', wiki_rels)
  ]
  content  = crawler.download_page(url,selector,verbose)
  return content

def wiki_title(page):
  return page.find('h1#firstHeading').text()

"""
Scrape the main article content from the specified 
wikipedia page
"""
def wiki_contents(page):
  contents   = []
  paragraphs = page.find('#bodyContent p')
  for p in paragraphs:
    contents.append(p.text())

  return contents

"""
Scrape all related links (to other wiki pages)
from the current wikipedia page
"""
def wiki_rels(page):
  links = []
  for li in page.find('ul li'):
    link = li.find('a')
    # The item must locate a link to another wiki page
    links.append(link.attr('href'))

  return links