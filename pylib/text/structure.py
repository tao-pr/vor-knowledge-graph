"""
Sentence pattern semantic extraction module
@author Tao PR (github.com/starcolon)
CopyRight 2016-present
"""

import numpy as np
import os.path
import pickle
import json
from termcolor import colored
from textblob import TextBlob


# TAOTODO:
"""
Extract part of speech structure of the given text
@param {list} of tokenised text
@return {list} of {tuple} of text and its POS
"""
def pos_tag(texts):
  blobs = [(t,TextBlob(t).tags) for t in texts]
  return blobs

"""
Extract a keyword from the given list of words
with regards to the specified intent.
@param {list} of tokenised text
@param {string} intent
@return {string} of keyword
"""
def extract_keywords(texts,intent):
  pass