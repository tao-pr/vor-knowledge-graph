"""
Knowledge graph
@author TaoPR (github.com/starcolon)
"""

import pyorient
from pyorient.exceptions import PyOrientSchemaException
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
      self.orient.command('create class HAS extends E')
    except PyOrientSchemaException as e:
      print(colored('[WARNING] Preparing graph schema','yellow'))
      print(colored(e,'yellow'))
    


  """
  Add a set of new knowledge links
  @param {str} topic
  @param {list} of {str} words
  @param {bool} verbose
  """
  def add(self,topic,words,verbose):

    if verbose: print(colored('Adding : ','green'), topic, ' ===> ', words)

    # Add a new topic if not exist
    queryTopic = "select from TOPIC where title='{0}'".format(topic)
    if len(self.orient.command(queryTopic))==0:
      if verbose: print(colored('New topic added: ','green'), topic)
      self.orient.command("create vertex TOPIC set title='{0}'"
        .format(topic))

    # Add new words which don't exist
    for w in words:
      queryWord = "select from KEYWORD where w='{0}'".format(w)
      if len(self.orient.command(queryWord))==0:
        if verbose: print(colored('New word added: ','green'), w)
        self.orient.command("create vertex KEYWORD set w='{0}'".format(w))

      # Add a link from {topic} => {word}
      self.orient.command("create edge HAS from ({0}) to ({1})"
        .format(queryTopic,queryWord))

    # Add links between words
    for w in words:
      # Add a link to sibling words (words which co-exist in same sentence)
      siblings = (u for u in words if not w == u)
      for s in siblings:
        querySib = "select from KEYWORD where w='{0}'".format(s)
        self.orient.command("create edge REL from ({0}) to ({1})".
          format(queryWord,querySib))

  """
  Enumerate all keywords in a topic
  @param {str} topic title
  """
  def keywords_in_topic(self,topic):
    query = "select expand(out()) from topic where title = '{0}'".format(topic)
    keywords = iter([rec.oRecordData for rec in self.orient.command(query)])
    return keywords

