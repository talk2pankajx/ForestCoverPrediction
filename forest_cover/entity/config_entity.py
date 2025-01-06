from dataclasses import dataclass
import os, sys
from datetime import datetime
from forest_cover.exception import ForestException
from forest_cover.constants import training_pipe


class TrainingPipelineConfig:
    def __init__(self,):
        timestamp = datetime.now().strftime('%m-%m-%Y %H-%M-%S')
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
            
            