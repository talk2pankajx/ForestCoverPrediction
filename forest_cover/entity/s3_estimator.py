import sys
from forest_cover.cloud_storage.aws_storage import SimpleStorageService
from forest_cover.exception import ForestException
from forest_cover.ml.model.estimator import ForestPredictionModel
from pandas import DataFrame


class ForestEstimator:
    
    def __init__(self,bucket_name,model_path):
        
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: ForestPredictionModel = None
        
    
    def is_model_present(self,model_path):
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, model_path=self.model_path)
        except Exception as e:
            raise ForestException(e,sys)
            print(e)
            return False
    
    def load_model(self)-> ForestPredictionModel:
        try:
            return self.s3.load_model(self.model_path,bucket_name=self.bucket_name)
            
        except Exception as e:
            raise ForestException(e,sys)

    def save_model(self,from_file,remove: bool= False):
        try:
            return self.s3.upload_file(from_file,to_filename=self.model_path,bucket_name=self.bucket_name, remove=remove)
        except Exception as e:
            raise ForestException(e,sys)
        
    
    def predict(self, dataframe: DataFrame):
      
      try:  
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
      except Exception as e:
          raise ForestException(e,sys)