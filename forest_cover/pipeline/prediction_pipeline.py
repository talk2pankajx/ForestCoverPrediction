from forest_cover.entity.config_entity import *
from forest_cover.entity.artifact_entity import *
from forest_cover.exception import ForestException
from forest_cover.logging import logging
import sys, os
import pandas as pd
import numpy as np
from pandas import DataFrame
from forest_cover.entity.s3_estimator import ForestEstimator
from forest_cover.cloud_storage.aws_storage import SimpleStorageService



class PredictionPipeline:
    def __init__(self,prediction_pipeline_config: PredictionPipelineConfig = PredictionPipelineConfig(),):
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
            self.s3 = SimpleStorageService()
        except Exception as e:
            raise ForestException(e,sys)
        
    def get_data(self)->DataFrame:
        try:
            logging.info("entered the get_data methode of the prediction pipeline class")
            prediction_df : DataFrame = self.s3.read_csv(filename=self.prediction_pipeline_config.data_file_path,
                                                        bucket_name=self.prediction_pipeline_config.data_bucket_name)
            logging.info("Read the prediction file to the s3 bucket")
            logging.info("Exited the get_data method of the prediction pipeline class")
        
            return prediction_df
        except Exception as e:
            raise ForestException(e,sys)
        
    def predict(self, dataframe: DataFrame)->np.ndarray:
        try:
            logging.info("Entered the predict method of the prediction pipeline")
            forest_estimator = ForestEstimator(self.prediction_pipeline_config.model_bucket_name,model_path=self.prediction_pipeline_config.model_file_path)
            logging.info("Exited the predict method of the prediction pipeline")
            return forest_estimator.predict(dataframe)
        except Exception as e:
            raise ForestException(e,sys)
    
    def initiate_prediction(self,)->None:
        try:
            logging.info("Entering the initiate method of the prediction pipeline")
            dataframe = self.get_data()
            predicted_arr =  self.predict(dataframe)
            prediction = pd.DataFrame(list(predicted_arr))
            prediction.columns = ["Cover_type"]
            predicted_dataframe  = pd.concat([dataframe, prediction], axis=1)
            
            self.s3.upload_df_as_csv(
                predicted_dataframe,
                self.prediction_pipeline_config.output_file_name,
                self.prediction_pipeline_config.output_file_name,
                self.prediction_pipeline_config.data_bucket_name
            )
        
            logging.info("uploading the artifacts on the s3 bucket")
            
            logging.info(f"file has been uploaded to {predicted_dataframe}")
            
            logging.info("Exited the initiate method of the prediction pipeline")
            return predicted_dataframe
        
        except Exception as e:
            raise ForestException(e,sys)
    