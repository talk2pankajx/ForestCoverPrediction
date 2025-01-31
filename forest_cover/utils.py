
import pandas as pd
from forest_cover.exception import ForestException
import os, sys
import yaml
import dill
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV

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
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
                          
    except Exception as e:
        raise ForestException(e,sys) from e

def load_object(file_path:str)->object:
    try:
        with open(file_path, 'rb') as file_obj:
            obj = dill.load(file_obj)
        return obj                      
    except Exception as e:
        raise ForestException(e,sys) from e
    
