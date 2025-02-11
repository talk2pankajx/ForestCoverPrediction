import os, sys
from datetime import datetime
from forest_cover.exception import ForestException
from forest_cover.constants import training_pipe
from forest_cover.constants.training_pipe.s3_bucket import PREDICTION_BUCKET_NAME,TRAINING_BUCKET_NAME

from dataclasses import dataclass

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime('%d-%m-%Y %H-%M-%S')
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
class ModelTrainerConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,training_pipe.MODEL_TRAINER_DIR_NAME)
            self.trained_model_file_path= os.path.join(training_pipeline_config.artifact_dir,training_pipe.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                       training_pipe.MODEL_TRAINER_TRAINED_MODEL_NAME)
            self.expected_accuracy = training_pipe.MODEL_TRAINER_EXPECTED_SCORE
            self.model_trainer_config_file_path = os.path.join(training_pipe.MODEL_TRAINER_CONFIG_FILE_PATH)
            
        except Exception as e:
            raise ForestException(e,sys)
        
class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.changed_threshold_score : float = training_pipe.MODEL_EVALUATION_CHANGED_THRESHOLD
            self.bucket_name : str = training_pipe.MODEL_PUSHER_BUCKET_NAME
            self.s3_model_key_path : str = os.path.join(training_pipeline_config.artifact_dir,training_pipe.MODEL_PUSHER_S3_KEY,training_pipe.MODEL_FILE_NAME)
        except Exception as e:
            raise ForestException(e,sys)

@dataclass
class ModelPusherConfig:
        try:
            bucket_name : str = training_pipe.MODEL_PUSHER_BUCKET_NAME
            s3_model_key_path : str = os.path.join(training_pipe.MODEL_PUSHER_S3_KEY,training_pipe.MODEL_FILE_NAME)
            
        except Exception as e:
            raise ForestException(e,sys)

@dataclass
class PredictionPipelineConfig:
    training_pipeline_config = TrainingPipelineConfig()
    data_bucket_name : str = training_pipe.PREDICTION_DATA_BUCKET
    data_file_path : str = training_pipe.PREDICTION_INPUT_FILE_NAME
    model_file_path :str = os.path.join(training_pipe.MODEL_PUSHER_S3_KEY,training_pipe.MODEL_FILE_NAME)
    model_bucket_name : str = training_pipe.MODEL_BUCKET_NAME
    output_file_name : str = training_pipe.PREDICTION_OUTPUT_FILE_NAME
    model_trainer_dir :str = os.path.join(training_pipeline_config.artifact_dir,training_pipe.ARTIFACTS_DIR,training_pipe.MODEL_TRAINER_DIR_NAME)
    trained_model_file_path :str = os.path.join(model_trainer_dir,training_pipe.MODEL_TRAINER_TRAINED_MODEL_DIR,training_pipe.MODEL_FILE_NAME)
    