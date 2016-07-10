"""
Knowledge graph
@author Tao PR (github.com/starcolon)
"""

import pyorient
import numpy as np
import os.path
import json
from termcolor import colored

class Knowledge:

  """
  Create a new knowledge graph connection.
  The constructor itself is idemponent which means it creates 
  a new database and fill in the structure if it doesn't exist.
  Otherwise, it just open the existing connection.
  """
  def __init__(self,host,dbname,usrname,psw):
    self.orient    = pyorient.OrientDB(host,2424)
    self.__session = self.orient.connect(usrname,psw)
    if self.orient.db_exists(dbname,pyorient.DB_TYPE_GRAPH):
      self.orient.db_open(dbname.usrname,psw)
    else:
      self.orient.db_create(dbname,pyorient.DB_TYPE_GRAPH)
      self.orient.db_open(dbname,usrname,psw)

  """
  Add a new knowledge link from a -> b
  """
  def add(self,a,b,link):
    # TAOTODO: Add new knowledge nodes and link
    pass

  """
  Unlink an existing knowledge link from a -> b
  """
  def unlink(self,a,b):
    pass

  def visualise(self):
    pass

