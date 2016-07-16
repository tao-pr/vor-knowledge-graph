"""
POS pattern tree
---
Pattern tree is built from a list of POS patterns.
It is employed as a sentence parser which captures 
and build a mini knowledge graph.
"""

from collections import deque

class PatternCapture:
  def __init__(self):
    self.__patterns = []

  """
  Read in the list of POS structure from a text file
  """
  def load(self,path):
    with open(path,'r') as f:
      self.__patterns = set([p.replace('\n','') for p in f.readlines()])

  """
  Save a list of POS structure to a text file
  """
  def save(self,path):
    with open(path,'w') as f:
      for p in self.__patterns:
        f.write(p+"\n")

  def append(self,p):
    self.__patterns.append(p)

  def join(self,delim):
    return delim.join(self.__patterns)

  """
  Capture the keyword tree of the given sentence
  Sample output:
    [
      ['Ammonia','Phosphate'],
      ['Heated',['Potassiam','Nitrate'],'Solution']
    ]
  @param {list} of tuples of (word,tag)
  @return {list} represents a captured tree
  """
  def capture(self,pos_sentence):
    pos_deq = deque(pos_sentence)
    tree    = []

    # Iterate through the sentence POS tags (greedy capture)
    bichain, bichain_tag = deque(),deque()
    trichain, trichain_tag = deque(),deque()
    
    while len(pos_deq)>0:
      t,tag = pos_deq.popleft()

      # Accumulate the current chain
      bichain.append(t)
      bichain_tag.append(tag)
      trichain.append(t)
      trichain_tag.append(tag)

      # Check if the individual tag matches any of the patterns?
      if tag in self.__patterns:
        tree.append(t)

      # Check if current bichain matches any patterns?
      if len(bichain)==2:
        if '-'.join(bichain_tag) in self.__patterns:
          tree.append(' '.join(bichain))
        # Clean up for the next iteration
        bichain.popleft()
        bichain_tag.popleft()

      # Check if current trichain matches any patterns?
      if len(trichain)==3:
        if '-'.join(trichain_tag) in self.__patterns:
          tree.append(' '.join(trichain))
        # Clean up for the next iteration
        trichain.popleft()
        trichain_tag.popleft()

    return tree


