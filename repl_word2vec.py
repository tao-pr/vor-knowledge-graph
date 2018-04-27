"""
Play with word2vec model
@author TaoPR (github.com/starcolon)
"""

import os
import sys
import argparse
import word2vec
from termcolor import colored

arguments = argparse.ArgumentParser()
arguments.add_argument('--modelpath', type=str, default='./models/word2vec.bin', help='Path of the word2vec binary model.')
args = vars(arguments.parse_args(sys.argv[1:]))

"""
Find the best identical twin of the specified word.
Identical twins are a couple of words which score the highest similarity both ways.
"""
def find_twin(w, model):
  try:
    indexes, metrics = model.cosine(w)
    candidates = model.generate_response(indexes, metrics).tolist()
    reverse_candidates = []
    for c,score in candidates:
      _indexes, _metrics = model.cosine(c)
      for _c,_score in model.generate_response(_indexes, _metrics):
        if _c == w:
          reverse_candidates.append((c,_score * score))
    
    if len(reverse_candidates)==0:
      return None
    return sorted(reverse_candidates, key=lambda x: -x[1])[0]
  except:
   return None

def repl(model):
  print(colored('[Model] Loaded:','cyan'))
  print('... Model shape : {}'.format(model.vectors.shape))
  print('... Clusters    : {}'.format(model.clusters))
  while True:
    w = input('Enter word to test : ')
    try:
      indexes, metrics = model.cosine(w)
      print(colored('... indexes  : ', 'cyan'), indexes)
      print(colored('... metrics  : ', 'cyan'), metrics)
      print(colored('... similar  : ', 'cyan'), model.vocab[indexes])
      print(colored('... response : ', 'cyan'))
      print(model.generate_response(indexes, metrics).tolist())
    except Exception:
      print(colored('... Vocab not recognised by the model.','red'))

    print(colored('... twin : ', 'green'), find_twin(w, model))


if __name__ == '__main__':
  # Load the word2vec model
  model_path = os.path.realpath(args['modelpath'])
  if not os.path.isfile(model_path):
    print(colored('[ERROR] word2vec model does not exist.','red'))
    raise RuntimeError('Model does not exist')
  print(colored('[Model] loading binary model.','cyan'))
  model = word2vec.WordVectors.from_binary(model_path, encoding='ISO-8859-1')
  repl(model)