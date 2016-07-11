"""
Mining data source access
@author Tao PR (github.com/starcolon)
"""
from pymongo import MongoClient
from pymongo import InsertOne

class MineDB:

  def __init__(self,host,db,coll):
    addr       = "mongodb://{0}:27017/".format(host)
    self.mongo = MongoClient(addr)
    self.db    = self.mongo[db]
    self.src   = self.db[coll]

  def query(self,conditions={},field=None):
    for n in self.src.find(conditions):
      # No field name specified, generate the entire record
      if field is None:
        yield n
      # Generate the specified field
      else:
        yield n[field]

  def update(self,criteria,updater):
    self.src.update_one(criteria,updater)

  def insert(self,record):
    self.src.insert_one(record)

  def insert_many(self,records):
    new_records = [InsertOne(r) for r in records]
    self.src.bulk_write(new_records)
