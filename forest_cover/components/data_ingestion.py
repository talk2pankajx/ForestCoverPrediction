from forest_cover.exception import ForestException
from forest_cover.logging import logging
from forest_cover.entity.artifact_entity import DataIngestionArtifact
from forest_cover.entity.config_entity import DataIngestionConfig
from forest_cover.utils import export_collection_as_dataframe
from forest_cover.utils import read_yaml_file
import os,sys
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion():
    
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ForestException(e,sys)
        
        
    
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Exporting collection as dataframe")  
            df = export_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name)
            self.export_data_into_feature_store(df)
            self.split_data_into_train_and_test(df)         
            
            logging.info("Preparing data ingestion artifact")
            
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.train_file_path
                                   ,test_file_path=self.data_ingestion_config.test_file_path)
            
            return data_ingestion_artifact
            
        except Exception as e:
            raise ForestException(e,sys)

    def export_data_into_feature_store(self,df:pd.DataFrame):
        try:
            logging.info("Exporting dataframe to feature store")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe = df.to_csv(feature_store_file_path,index=False,header=True)
            logging.info(f"Data exported to feature store at: {feature_store_file_path}")
            return dataframe
                        
        except Exception as e:
            raise ForestException(e,sys)
        
    def split_data_into_train_and_test(self,df:pd.DataFrame):
        try:
            logging.info("Splitting the dataset into test and train")
            train_df, test_df = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed the train test split")
            
            dir_path =os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting the train and test file path")
            
            train_df.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("Train and test data exported successfully")        
            
            
        except Exception as e:
            raise ForestException(e,sys)
    
    



