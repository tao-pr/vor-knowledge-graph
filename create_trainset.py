"""
Mining dataset maker
---
The program helps creating a mining dataset easy and convenient.
Two modes of inputs are eligible: CSV file / CLI inputs.
"""

import csv
import sys
import argparse
from termcolor import colored
from pylib.knowledge.datasource import MineDB

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--db', type=str, default='vor', help='Specify the database name to store input.')
arguments.add_argument('--col', type=str, default='text', help='Specify the collection name to store input.')
arguments.add_argument('--input', type=str, default=None, help='Specify an input CSV file path for file mode.') 
args = vars(arguments.parse_args(sys.argv[1:]))

def cli_input(dbsrc):
  sentence = input(colored("Sentence : ","cyan"))
  intent   = input(colored(" ≈ Intent : ","cyan"))
  keyword  = input(colored(" ≈ Keyword : ","cyan"))
  # Add to the database
  add_to_db(dbsrc, sentence, intent, keyword)
  print(colored("[ADDED]","green"))

def file_input(dbsrc,path,verbose):
  with open(path, 'rb') as csvfile:
    io = csv.reader(csvfile, delimeter=',')
    for row in io:
      sentence = row[0]
      intent   = row[1]
      keyword  = row[2]
      add_to_db(dbsrc, sentence, intent, keyword)

def add_to_db(db,sentence,intent,keyword):
  db.insert({
    'raw':    sentence,
    'intent': intent,
    'key':    keyword if len(keyword.strip())>0 else None
  })

if __name__ == '__main__':

  db_name         = args['db']
  collection_name = args['col']
  verbose         = args['verbose']
  mine_src        = MineDB('localhost',db_name,collection_name)

  if args['input'] is not None:
    # Input CSV file mode
    print(colored('[Reading CSV input] : ','magenta') + args['input'])
    file_input(mine_src,args['input'],verbose)
  else:
    # Input CLI mode
    while True:
      cli_input(mine_src)