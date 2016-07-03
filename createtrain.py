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
arguments.add_argument('--db', type=str, default='vor') # DB source to take
arguments.add_argument('--col', type=str, default='text') # Collection source to take
arguments.add_argument('--input', type=str, default=None) # Specify an input CSV file path for file mode
args = vars(arguments.parse_args(sys.argv[1:]))

def cli_input(dbsrc):
  sentence = input(colored("Sentence : ","cyan"))
  intent   = input(colored(" ≈ Intent : ","cyan"))
  keyword  = input(colored(" ≈ Keyword : ","cyan"))
  # Add to the database
  add_to_db(dbsrc, sentence, intent, keyword)
  print(colored("[ADDED]","green"))

def file_input(dbsrc,path):
  with open(path, 'rb') as csvfile:
    io = csv.reader(csvfile, delimeter=',')
    for row in io:
      sentence = row[0]
      intent   = row[1]
      keyword  = row[2]
      add_to_db(dbsrc, sentence, intent, keyword)

def add_to_db(db,sentence,intent,keyword)
  db.insert_one({
    'raw':    sentence,
    'intent': intent,
    'key':    keyword
  })

if __name__ == '__main__':

  db_name         = args['db']
  collection_name = args['col']
  mine_src        = MineDB('localhost',db_name,collection_name)

  if args['input'] is not None:
    # Input CSV file mode
    print(colored('[Reading CSV input] : ','magenta') + args['input'])
    file_input(args['input'])
  else:
    # Input CLI mode
    cli_input(mine_src)