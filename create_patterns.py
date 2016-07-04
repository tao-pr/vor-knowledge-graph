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
arguments.add_argument('--input', type=str, default=None, help='Specify an input text file as input patterns.') 
args = vars(arguments.parse_args(sys.argv[1:]))

def cli_input(dbsrc,sentence):
  sentence = print(colored("Sentence : ","cyan"), sentence)
  subj     = input(colored(" ≈ subj : ","cyan"))
  dest     = input(colored(" ≈ dest : ","cyan"))
  link     = input(colored(" ≈ link : ","cyan"))
  when     = input(colored(" ≈ when : ","cyan"))
  # Add to the database
  add_to_db(dbsrc, sentence, subj, dest, link, when)
  print(colored("[ADDED]","green"))

# def file_input(dbsrc,path,verbose):
#   with open(path, 'rb') as csvfile:
#     io = csv.reader(csvfile, delimeter=',')
#     for row in io:
#       sentence,who,how,where,when = row
#       who   = None if len(who)==0 else who
#       how   = None if len(how)==0 else how
#       where = None if len(where)==0 else where
#       when  = None if len(when)==0 else when
#       add_to_db(dbsrc, sentence, who, how, where, when)

def add_to_db(db,sentence,subj,dest,link,when):
  db.insert({
    'raw':  sentence,
    'subj': subj,
    'dest': dest,
    'link': link,
    'when': when
  })

if __name__ == '__main__':

  db_name         = args['db']
  collection_name = args['col']
  verbose         = args['verbose']
  inputfile       = args['input']
  mine_src        = MineDB('localhost',db_name,collection_name)

  # Reads in the input file
  if inputfile is None:
    print(colored('You have to locate the input text file.','red'))
    raise ValueError('Input file has not been specified.')

  with open(inputfile) as f:
    for sentence in f:
      cli_input(mine_src,sentence)