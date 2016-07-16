"""
Sentence pattern semantic extraction module
@author Tao PR (github.com/starcolon)
CopyRight 2016-present
"""

import numpy as np
import os.path
import pickle
import json
from collections import deque
from termcolor import colored
from textblob import TextBlob


"""
Extract part of speech structure of the given text
@param {list} of tokenised words
"""
def pos_tag(words):
  def generate(t):
    tags = TextBlob(t).tags
    return tags[0]

  blobs = [generate(t) for t in words]
  return blobs

def tag_with_color(words):
  pos    = pos_tag(words)
  tokens = ' | '.join([colored(tag,'yellow') + ':' + t for t,tag in pos])
  print(tokens)

"""
Read in the list of POS structure from a text file
"""
def read_pos_patterns(path):
  with open(path,'r') as f:
    return [p.replace('\n','') for p in f.readlines()]

"""
Save a list of POS structure to a text file
"""
def save_pos_patterns(path,patterns):
  with open(path,'w') as f:
    for p in patterns:
      f.write(p+"\n")



