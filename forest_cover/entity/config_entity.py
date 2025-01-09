import os, sys
from datetime import datetime
from forest_cover.exception import ForestException
from forest_cover.constants import training_pipe


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime('%m-%m-%Y %H-%M-%S')
        self.pipeline_name = training_pipe.PIPELINE_NAME
        self.artifact_name = training_pipe.ARTIFACTS_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp :str = timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_ingestion_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipe.DATA_INGESTION_DIR_NAME)
            self.feature_store_file_path :str = os.path.join(self.data_ingestion_dir,training_pipe.DATA_INGESTION_FEATURE_STORE_DIR,
                                                        training_pipe.FILE_NAME)
            self.train_file_path :str = os.path.join(self.data_ingestion_dir,training_pipe.DATA_INGESTION_INGESTED_DIR,training_pipe.TRAIN_FILE_NAME)
            self.test_file_path :str = os.path.join(self.data_ingestion_dir,training_pipe.DATA_INGESTION_INGESTED_DIR,training_pipe.TEST_FILE_NAME)
            self.train_test_split_ratio :float = training_pipe.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name :str = training_pipe.DATA_INGESTION_COLLECTION_NAME
            self.database_name :str = training_pipe.DATA_INGESTION_DATABASE_NAME
            
        except Exception as e:
            raise ForestException(e,sys)
            
class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir :str = os.path.join(training_pipeline_config.artifact_dir,training_pipe.DATA_VALIDATION_DIR_NAME)
            self.valid_dir :str = os.path.join(self.data_validation_dir,training_pipe.DATA_VALIDATION_VALID_DIR)
            self.invalid_dir :str = os.path.join(self.data_validation_dir,training_pipe.DATA_VALIDATION_INVALID_DIR)
            self.valid_train_file_path :str = os.path.join(self.valid_dir,training_pipe.TRAIN_FILE_NAME)
            self.valid_test_file_path :str =os.path.join(self.valid_dir,training_pipe.TEST_FILE_NAME)
            self.invalid_train_file_path :str = os.path.join(self.invalid_dir,training_pipe.TRAIN_FILE_NAME)
            self.invalid_test_file_path :str = os.path.join(self.invalid_dir,training_pipe.TEST_FILE_NAME)
            self.drift_report_file_path : str = os.path.join(self.data_validation_dir,training_pipe.DATA_VALIDATION_DRIFT_REPORT_DIR,training_pipe.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
            
        except Exception as e:
            raise ForestException(e,sys)
        

class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipe.DATA_TRANSFORMATION_DIR_NAME)
            self.transformed_train_file_path:str = os.path.join(self.data_transformation_dir,training_pipe.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipe.TRAIN_FILE_NAME.replace("csv","npy"))
            self.transformed_test_file_path:str = os.path.join(self.data_transformation_dir,training_pipe.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipe.TEST_FILE_NAME.replace("csv","npy"))
            self.transformed_object_file_path:str = os.path.join(self.data_transformation_dir,training_pipe.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,training_pipe.PREPROCESSED_OBJECT_FILE_NAME)
        except Exception as e:
            raise ForestException(e,sys)    