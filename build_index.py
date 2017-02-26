"""
Knowledge index maker
@author Tao PR (github.com/starcolon)
"""

import os
import sys
import argparse
from termcolor import colored

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose', dest='verbose', action='store_true', help='Turn verbose output on.')
arguments.add_argument('--limit', type=int, default=100, help='Maximum number of topics we want to build index')
args = vars(arguments.parse_args(sys.argv[1:]))

