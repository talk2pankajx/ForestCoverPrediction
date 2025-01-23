from forest_cover.constants.training_pipe import MODEL_FILE_NAME,SAVED_MODELS_DIR
from forest_cover.exception import ForestException
from forest_cover.logging import logging
from sklearn.pipeline import Pipeline
from pandas import DataFrame
import os
import sys


class ForestPredictionModel:
    def __init__(self,preprocessing_object:Pipeline,trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
       
        
    def predict(self,dataframe : DataFrame)->DataFrame:
        try:
            transformed_feature = self.preprocessing_object.transform(dataframe)
            return self.trained_model_object.predict(transformed_feature)
        
                   
        except  Exception as e:
            raise ForestException(e, sys)
    
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"
        
        