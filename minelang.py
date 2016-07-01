"""
Language miner
---
The program explores the annotated text set, 
creates a set of intent classifiers and keyword taggers.
---
@author Tao PR (github/starcolon)
"""

import argparse
from pylib.text import structure as TextStructure
from pylib.text import texthasher as TextHash
from pylib.knowledge.graph import Knowledge

arguments = argparse.ArgumentParser()
arguments.add_argument('--db', type=str, default='vor') # DB source to take
arguments.add_argument('--col', type=str, default='text') # Collection source to take
arguments.add_argument('--outdir', type=str, default='./models') # Where to store output models
args = vars(arguments.parse_args(sys.argv[1:]))


if __name__ == '__main__':
  # TAOTODO: Implement the sequence of process
  db_name         = args['db']
  collection_name = args['col']
  output_dir      = args['outdir']

  # Reads in the raw annotated sentence list

  # Train intent classifiers

  # Train keyword taggers

  pass