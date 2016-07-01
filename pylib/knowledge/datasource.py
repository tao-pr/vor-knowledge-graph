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
    self.src   = self.mongo[coll]

  def query(self,conditions):
    for n in self.src.find(conditions):
      yield n

  def insert(self,record):
    new_record = InsertOne(record)
    self.src.bulk_write([new_record])

  def insert_many(self,records):
    new_records = [InsertOne(r) for r in records]
    self.src.bulk_write(new_records)
