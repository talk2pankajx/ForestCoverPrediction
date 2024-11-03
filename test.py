from forest_cover.utils import dump_csv_to_mongo_collection
from forest_cover.exception import ForestException
from forest_cover.logging import logging
from dotenv import load_dotenv
import os,sys

load_dotenv()

def storing_record_in_mongodb():
    try:
        
        file_path = 'notebooks\covtype.csv'
        database_name = "forest_db"
        collection_name = "forest_cols"
        dump_csv_to_mongo_collection(database_name,collection_name,file_path)
        
    except Exception as e:
        raise e
    
def test_exception_and_logger():
    try:
        x = 1/0
    except Exception as e:
        raise ForestException(e, sys)


if __name__ == "__main__":
    try:
        test_exception_and_logger()
    except Exception as e:
        print(e)