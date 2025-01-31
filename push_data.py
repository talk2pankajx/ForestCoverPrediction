import os
import sys
import json

import pandas as pd
import numpy as np
import pymongo
from forest_cover.exception import ForestException
from forest_cover.logging import logging


MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

class ForestDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise ForestException(e,sys)


    def csv_to_json_converter(self, file_path):
        try:
            data =pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            json_data  = json.loads(data.T.to_json()) #
            records = list(json_data.values())
            return records
        except Exception as e:
            raise ForestException(e,sys)
    
    def insert_data_to_mongodb(self,records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)   
            
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
            
            
        except Exception as e:
            raise ForestException(e,sys)
