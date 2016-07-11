"""
Wikipedia crawler service
---
The service runs in background and keeps crawling raw knowledge data.
The downloaded data from Wikipedia is senquentially pushed to 
the specified RabbitMQ.
"""

import sys
import argparse
from termcolor import colored
from pylib.spider import wiki as Wiki
from pylib.jobmq.rabbit import JobMQ
from pylib.text import structure as TextStructure
from pylib.knowledge.datasource import MineDB

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--page', type=str, default='Jupiter', help='Indicate the wikipedia page to start crawling')
arguments.add_argument('--depth', type=int, default=128, help='Indicate maximum depth of crawling level')
args = vars(arguments.parse_args(sys.argv[1:]))

if __name__ == '__main__':
  # Print out arguments
  print(colored('¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬','green'))
  print(colored('  Crawling:      ','green'), colored(args['page'],'magenta'))
  print(colored('  Ongoing depth: ','green'), args['depth'])
  print(colored('¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬','green'))
  
  # TAOTODO: