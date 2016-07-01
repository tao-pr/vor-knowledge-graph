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
@param {object} tagger model
@param {list} of tokenised text
@return {string} of keyword
"""
def extract_keyword(tagger_model,texts):
  pos = pos_tag(texts)
  if len(pos)==0:
    return None
  else:
    # Tag the position of the keyword in the POS components
    keyword_pos = tagger_model.tag(pos)
    # Extract the keyword from the matched POS position, if any
    matched = [w for (p,w) in pos if p==keyword_pos]
    if len(matched)>0:
      return matched[0]
    else:
      return None

"""
Train the keyword tagger model from the annotated training set
@param {list} of Y : annotated POS as a keyword
@param {list} of X : raw text
"""
def train_keyword_tagger(labels,dataset):
  # TAOTODO: HMM-based training
  pass