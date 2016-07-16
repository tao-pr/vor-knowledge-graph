"""
Knowledge graph builder
@author TaoPR (github.com/starcolon)
---
Process the entire bulk of the crawled dataset (MongoDB)
and potentially create a knowledge graph (OrientDB)
"""

import sys
import argparse
from termcolor import colored
from pylib.knowledge.graph import Knowledge

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--start', type=int, default=0, help='Starting index of the crawling record to annotate.')
arguments.add_argument('--root', type=str, default=None, help='Supply the OrientDB password for root account.')
args = vars(arguments.parse_args(sys.argv[1:]))

if __name__ == '__main__':

  # Initialise a knowledge database
  kb = Knowledge('localhost','vor','root',args['root'])

  pass
