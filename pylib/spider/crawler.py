"""
Website crawler with specific reader
"""

import urllib.request
from htmldom import htmldom
from termcolor import colored

"""
Download and scrape the content from the given URL
@param {string} URL locator of the website to scrape
@param {string} DOM selector which locates the content element
@param {function} defines how to format the DOM element into a data package
@return {object} scraped content
"""
def download_page(url,selector,formatter):
  # Download the entire page HTML, processed as a DOM tree
  print(colored('Fetching: ','green') + colored(url,'cyan'))
  page = htmldom.HtmlDom(url).createDom()

  # Apply the specified selector the fetch the content
  # out of the downloaded DOM tree
  if page.find(selector):
    dom_content = page.find(selector)
    pass
  else:
    print(colored('Unable to locate the content element','yellow'))
    return None
