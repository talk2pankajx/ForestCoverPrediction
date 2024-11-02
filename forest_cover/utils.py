from config import mongo_client
import logging
import pandas as pd
import json

def dump_csv_to_mongo_collection(database_name: str, collection_name: str, file_path: str) -> None:
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Rows and Columns {df.shape}")
        df.reset_index(drop=True,inplace=True)
        json_records = list(json.loads(df.T.to_json()).values())
        mongo_client[database_name][collection_name].insert_many(json_records)    
        
    
    except Exception as e:
        raise e