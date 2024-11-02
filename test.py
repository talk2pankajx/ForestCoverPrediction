from forest_cover.utils import dump_csv_to_mongo_collection

from dotenv import load_dotenv

load_dotenv()



if __name__=='__main__':
    file_path = 'notebooks\covtype.csv'
    database_name = "forest_db"
    collection_name = "forest_cols"


dump_csv_to_mongo_collection(database_name,collection_name,file_path)