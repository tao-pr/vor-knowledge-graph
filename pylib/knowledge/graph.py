"""
Knowledge graph
@author Tao PR (github.com/starcolon)
"""

import pyorient
import numpy as np
import os.path
import pickle
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
    self.__db      = pyorient.OrientDB(host,2424)
    self.__session = self.__db.connect(usrname,psw)
    if self.__db.db_exists(dbname,pyorient.DB_TYPE_GRAPH)
      self.__db.db_open(dbname.usrname,psw)
    else:
      self.__db.db_create(dbname,pyorient.DB_TYPE_GRAPH)
      self.__db.db_open(dbname,usrname,psw)

  def add_knowledge(self,node):
    pass

  def add_link(self,src,dst,lnk):
    pass

  def remove_knowledge(self,node):
    pass

  def remove_link(self,src,dst):
    pass

  def recall_related(self,node,max_level=1):
    pass
