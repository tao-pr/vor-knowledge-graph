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
  Permanently remove all edges and vertices
  """
  def clear(self):
    self.orient.command('delete vertex TOPIC')
    self.orient.command('delete vertex KEYWORD')
    self.orient.command('delete edge') # May this be redundant?
    print(colored('[Graph clearance] done','yellow'))

  """
  Add a set of new knowledge links
  @param {str} topic
  @param {list} of {str} words
  @param {float} weight of the link
  @param {bool} verbose
  """
  def add(self,topic,words,weight,verbose):

    if verbose: print(colored('Adding : ','green'), topic, ' ===> ', words)

    # Escape some unwanted characters from topic and words
    unwanted = "'"
    topic = topic.replace(unwanted," ")
    words = map(lambda w: w.replace(unwanted, " "), words)

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
      if verbose: print(colored('New link [{0}] HAS => [{1}]'.format(topic,w),'green'))
      
      # If [weight] is specified,
      # Create an inverted-index edge from
      # [keyword] => [topic]
      if weight is None:
        # General relation
        self.orient.command("create edge HAS from ({0}) to ({1})"\
          .format(queryTopic, queryWord))
      else:
        # Invert-index
        self.orient.command("create edge INDEX from ({0}) to ({1}) SET weight={2}"\
          .format(queryWord, queryTopic, weight))

    # Add links between words
    for w in words:
      # Add a link to sibling words (words which co-exist in same sentence)
      siblings = (u for u in words if not w == u)
      for s in siblings:
        querySib = "select from KEYWORD where w='{0}'".format(s)
        self.orient.command("create edge REL from ({0}) to ({1})".
          format(queryWord,querySib))

  """
  {Generator} Enumurate keywords by strength of connections
  """
  def top_keywords(self):
    query = "select w, in().size() as cnt from keyword order by cnt desc"
    for k in self.orient.query(query):
      yield k

  """
  {Generator} Enumurate all topics
  """
  def __iter__(self):
    query = "select from topic"
    for k in self.orient.query(query):
      yield k

  """
  {Generator} Enumerate all keywords in a topic
  @param {str} topic title
  """
  def keywords_in_topic(self, topic, with_edge_count=False):
    subquery = "select expand(out()) from topic where title = '{0}'".format(topic)
    query = "select w from ({0})".format(subquery) \
      if not with_edge_count \
      else "select w, in().size() as freq from (select expand(out()) from topic where title = '{}')".format(topic)
    for k in self.orient.query(query):
      yield k

  """
  {Generator} Enumerate all topics which the given keyword
  belong to
  @param {str} keyword to query
  """
  def topics_which_have(self,w):
    query = "select in().title from KEYWORD where w='{}'".format(w)
    for k in self.orient.query(query):
      yield k

