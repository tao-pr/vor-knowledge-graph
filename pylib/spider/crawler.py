"""
Website crawler with specific reader
"""

import urllib.request
from htmldom import htmldom
from termcolor import colored

"""
Download and scrape the content from the given URL
@param {string} URL locator of the website to scrape
@param {list} of tuples: (field name, selector function)
@param {bool} turn on/off verbose output
@return {object} scraped content
"""
def download_page(url,selectors,verbose=False):
  # Download the entire page HTML, processed as a DOM tree
  print(colored('Fetching: ','green') + colored(url,'cyan'))
  page = htmldom.HtmlDom(url).createDom()

  # Apply selector functions in order to create 
  # a content package
  content = {}
  for tup in selectors:
    field, selector = tup
    if verbose:
      print(colored('   Mapping : ','green'), field)
    content[field]  = selector(page)

  return content