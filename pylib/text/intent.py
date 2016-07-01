"""
Sentence intent classifier
@author Tao PR (github.com/starcolon)
"""
import numpy as np
import os.path
import pickle
import json
from termcolor import colored

def new():
  pass # TAOTODO:

def save(operations,path):
  with open(path,'wb+') as f:
    pickle.dump(operations,f)

def load(path):
  with open(path,'rb') as f:
    return pickle.load(f)

"""
Load the existing operations or create new if not exist
"""
def safe_load(path):
  if os.path.isfile(path): 
    print(colored('Text intent classifier loaded.','cyan'))
    return load(path)
  else: 
    print(colored('Text intent classifier created...','yellow'))
    return new()


