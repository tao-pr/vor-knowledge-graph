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
from pylib.text import structure as TextStructure
from pylib.knowledge.datasource import MineDB

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
args = vars(arguments.parse_args(sys.argv[1:]))

if __name__ == '__main__':
  main()