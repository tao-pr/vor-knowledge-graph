"""
Sentence intent classifier
@author Tao PR (github.com/starcolon)
"""
import numpy as np
import os.path
import pickle
import json
from termcolor import colored
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

"""
Create a new instance of intent classifier, label encoder included.
@param {list} distinct list of intent labels (string)
@param {string} classification method
@return {object} classifier object along with the label encoder
"""
def new(intent_labels=[],method='kmeans'):
  
  # Classification methods
  methods = {
    'kmeans': KMeans(n_clusters = len(intent_labels))
  }

  # Label encoders
  encoder = LabelEncoder()
  encoder.fit(intent_labels)

  return {
    'clf':     methods[method],
    'encoder': encoder
  }


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

# Classify multiple vectors at a time using 
# the specified trained operations
def classify(opr):
  def classify_us(vectors):
    vs   = opr['clf'].predict(vectors)
    return opr['encoder'].inverse_transform(vs)
  return classify_us

def train(opr):
  def fit(vectors,labels):
    # Make labels numeric
    numeric_labels = opr['encoder'].transform(labels)
    opr['clf'].fit(vectors,numeric_labels)
  return fit

