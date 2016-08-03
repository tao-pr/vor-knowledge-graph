"""
Knowledge graph
@author TaoPR (github.com/starcolon)
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
    if self.orient.db_exists(dbname):
      print(colored('Connecting OrientDB: {0}'.format(dbname),'green'))
      self.orient.db_open(dbname,usrname,psw)
    else:
      print(colored('Creating OrientDB: {0}'.format(dbname),'magenta'))
      self.orient.db_create(
        dbname,
        pyorient.DB_TYPE_GRAPH
      )
      self.orient.db_open(dbname,usrname,psw)

    # Make sure {Edge} and {Vertex} classes are recognised by the DB
    self.__prepare_classes()

  """
  Create initial classes (Edge + Vertex)
  """
  def __prepare_classes(self):
    try:
      self.orient.command('create class TOPIC extends V')
      self.orient.command('create class KEYWORD extends V')
      self.orient.command('create class REL extends E')
    except PyOrientSchemaException as e:
      print(colored('[ERROR] Preparing graph schema','red'))
      print(colored(e,'red'))
    


  """
  Add a new knowledge link from a -> b
  """
  def add(self,a,b,rel):
    # TAOTODO: Add new knowledge nodes and link

    print(colored('Adding : ','green'), a, ' ===> ', b)

    # Make sure node [a] exists

    # Make sure node [b] exists

    # Make sure link [a] <-> [b] exists
    pass

  """
  Unlink an existing knowledge link from a -> b
  """
  def unlink(self,a,b):
    pass

  def visualise(self):
    pass

