from config import mongo_client
import logging
import pandas as pd
import json
from forest_cover.exception import ForestException
import os, sys
import yaml

def dump_csv_to_mongo_collection(database_name: str, collection_name: str, file_path: str) -> None:
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Rows and Columns {df.shape}")
        df.reset_index(drop=True,inplace=True)
        json_records = list(json.loads(df.T.to_json()).values())
        mongo_client[database_name][collection_name].insert_many(json_records)    
        
    
    except Exception as e:
        raise e
    
def export_collection_as_dataframe(database_name: str, collection_name: str)->pd.DataFrame:
    try:
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        if "_id:" in df.columns.to_list():
            df.drop_index("_id:", axis = 1)
        return df   
         
    except Exception as e:
        raise ForestException

def read_yaml_file(file_path: str)->dict:
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data   
         
    except Exception as e:
        raise ForestException(e,sys)