"""
Mining dataset maker
---
The program reads in a set of input text from a physical file,
prompt for sentence annotations, and saves the results 
in the MongoDB collection as annotated patterns of sentences.
"""

import csv
import sys
import argparse
from termcolor import colored
from pylib.text import structure as TextStructure
from pylib.knowledge.datasource import MineDB

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--db', type=str, default='vor', help='Specify the database name to store input.')
arguments.add_argument('--col', type=str, default='text', help='Specify the collection name to store input.')
arguments.add_argument('--input', type=str, default=None, help='Specify an input text file as input patterns.') 
args = vars(arguments.parse_args(sys.argv[1:]))

def cli_input(dbsrc,sentence):
  print(colored("Sentence : ","cyan"), sentence)
  TextStructure.tag_with_color(sentence.split(' '))
  part_removal  = input(colored(" ¶ Reduced POS form : ","cyan"))

  # Add to the database
  add_to_db(dbsrc, sentence, subj, dest, link, when)
  print(colored("[ADDED]","green"))

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