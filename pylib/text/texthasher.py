"""
Text hashing (vectoriser)
@author Tao PR (github.com/starcolon)
CopyRight 2016-present
"""

import numpy as np
import os.path
import pickle
import json
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import SparsePCA
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation

decomposers = {
  'LDA': lambda n: 
    LatentDirichletAllocation( # TFIDF --> Topic term
      n_topics=n,
      max_iter=15
    ),
  'PCA': lambda n:
    SparsePCA( # NOTE: PCA is supposed to perform slow, so we limit num of iterations
      n_components=n,
      alpha=1,
      max_iter=10
    ),
  'SVD': lambda n:
    TruncatedSVD(n) # SVD may introduce some estimation losses
}

# Create a text process pipeline (vectorizer)
def new(n_components=None,stop_words=[],decomposition='SVD'):

  # Word stemming (English)
  # TAOTODO:

  # Prepare vectoriser engines
  idf = TfidfVectorizer(
    ngram_range=(1,3), #Unigram,bigram,& trigram
    stop_words=stop_words
  )

  # Prepare normaliser
  norm = Normalizer(norm='l2') # Cosine similarity 

  # Prepare dimentionality reducer
  if n_components:
    reducer = decomposers[decomposition](n_components)
    return [idf,reducer,norm]
  else:
    return [idf,norm]


def save(operations,path):
  with open(path,'wb+') as f:
    pickle.dump(operations,f)

def load(path):
  with open(path,'rb') as f:
    return pickle.load(f)

"""
Load the transformer pipeline object
from the physical file,
or initialise a new object if the file doesn't exist
"""
def safe_load(path,n_components,stop_words,decomposition):
  if os.path.isfile(path): 
    print(colored('Text hasher loaded.','cyan'))
    return load(path)
  else: 
    print(colored('Text hasher created...','yellow'))
    return new(n_components,stop_words,decomposition)


def hash(operations,learn=False):
  # @param {iterable} of string
  def hash_me(dataset):
    x = dataset

    if learn:
      for i in range(len(operations)): 
        print(colored('Processing ... #{0} : {1}'.format(i,type(operations[i])),'grey'))
        x = operations[i].fit_transform(x)
    else:
      for i in range(len(operations)): 
        x = operations[i].transform(x)

    return iter(x)
  return hash_me



