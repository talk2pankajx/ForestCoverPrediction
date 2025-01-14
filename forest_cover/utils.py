from config import mongo_client
import logging
import pandas as pd
import json
from forest_cover.exception import ForestException
import os, sys
import yaml
import dill
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, classification_report

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
        raise ForestException(e,sys)

def read_yaml_file(file_path: str)->dict:
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data   
         
    except Exception as e:
        raise ForestException(e,sys)

def write_yaml_file(file_path: str, content:object)->None:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content,file)
    
    except Exception as e:
        raise ForestException(e,sys)
    
def save_object(file_path :str, object:object)->None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            dill.dump(object, file)
    except Exception as e:
        raise ForestException(e,sys)
    

def save_numpy_array_data(file_path:str,arr:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file,arr)
            
    except Exception as e:
        raise ForestException(e,sys) from e

def load_numpy_array_data(file_path:str)->np.array:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        with open(file_path, 'rb') as file:
                return np.load(file)
                        
    except Exception as e:
        raise ForestException(e,sys) from e

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        with open(file_path, 'rb') as file:
                return pickle.load(file)
                        
    except Exception as e:
        raise ForestException(e,sys) from e
    
def evaluate_models(x_train,y_train,x_test,y_test,models:dict,params:dict):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]
            grd = GridSearchCV(model,para,cv=5)
            grd.fit(x_train, y_train)
            
            model.set_params(**grd.best_params_)
            model.fit(x_train,y_train)
            
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            
            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
        
        return report
    except Exception as e:
        raise ForestException(e,sys) 