from forest_cover.entity.artifact_entity import *
from forest_cover.entity.config_entity import *
from forest_cover.logging import logging
from forest_cover.exception import ForestException
from forest_cover.utils import read_yaml_file, write_yaml_file
import os, sys
from scipy.stats import ks_2samp
from forest_cover.constants.training_pipe import SCHEMA_FILE_PATH
import pandas as pd



class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_file_config = read_yaml_file(SCHEMA_FILE_PATH)       
            
        except Exception as e:
            raise ForestException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            train_df =DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            
            ## validate number of columns
            status = self.validate_columns(df=train_df)
            if not status:
                error_message = "Number of columns in train file does not match with schema file"
            status=self.validate_columns(df=test_df)
            if not status:
                error_message = "Number of columns in test file does not match with schema file"
            
            
            ## check dataset drift 
            
            status = self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,header=True,index=False
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,header=True,index=False
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact
        
        except Exception as e:
            raise ForestException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
            
        except Exception as e:
            raise ForestException(e,sys)
        
    def validate_columns(self,df:pd.DataFrame)->bool:
        try:
            no_of_columns = len(self._schema_file_config)
            logging.info(f"no of columns in schema file: {no_of_columns}")
            logging.info(f"no of columns in dataframe: {len(df.columns)}")
            if len(df.columns) == no_of_columns:
                return True
            else:
                return False
                
        except Exception as e:
            raise ForestException(e,sys)

    def detect_dataset_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold<=is_same_dist.pvalue:  
                    is_found = False
                else:
                    is_found = True
                    status= False
                report.update({column: {
                        "p_value" :float(is_same_dist.pvalue),
                        "drift_status": is_found
                    }})
                
            # creating the drift report
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
        except Exception as e:
            raise ForestException(e,sys)
        
        

