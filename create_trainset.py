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
  who      = input(colored(" ≈ who : ","cyan"))
  how      = input(colored(" ≈ how : ","cyan"))
  where    = input(colored(" ≈ where : ","cyan"))
  when     = input(colored(" ≈ when : ","cyan"))
  # Add to the database
  add_to_db(dbsrc, sentence, who, how, where, when)
  print(colored("[ADDED]","green"))

def file_input(dbsrc,path,verbose):
  with open(path, 'rb') as csvfile:
    io = csv.reader(csvfile, delimeter=',')
    for row in io:
      sentence,who,how,where,when = row
      who   = None if len(who)==0 else who
      how   = None if len(how)==0 else how
      where = None if len(where)==0 else where
      when  = None if len(when)==0 else when
      add_to_db(dbsrc, sentence, who, how, where, when)

def add_to_db(db,sentence,who,how,where,when):
  db.insert({
    'raw':   sentence,
    'who':   who,
    'how':   how,
    'where': where,
    'when':  when
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