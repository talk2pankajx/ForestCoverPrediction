from forest_cover.components.data_ingestion import DataIngestion

from forest_cover.components.data_validation import DataValidation

from forest_cover.components.data_transformation import DataTransformation

from forest_cover.components.model_trainer import ModelTrainer

from forest_cover.components.model_evalution import ModelEvaluation
from forest_cover.components.model_pusher import ModelPusher

from forest_cover.entity.config_entity import *
from forest_cover.entity.artifact_entity import *

from forest_cover.exception import ForestException

from forest_cover.logging import logging
import sys

from forest_cover.constants.training_pipe import *


class TrainingPipeline:
    
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
        except Exception as e:
            raise ForestException(e,sys)
        
    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Finishing data ingestion")
            return data_ingestion_artifact
            
            
        except Exception as e:
            raise ForestException(e,sys)
    
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data validation")
            data_validation  = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Finishing data validation")
            return data_validation_artifact
            
        except Exception as e:
            raise ForestException(e,sys)
        
    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config= DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data transformation")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Finishing data transformation")
            return data_transformation_artifact

        except Exception as e:
            raise ForestException(e,sys)
        
    def start_model_training(self,data_transformation_artifact: DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("starting Model Training")
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_training()
            logging.info("Finishing Model Training")
            return model_trainer_artifact

        except Exception as e:
            raise ForestException(e,sys)
    
    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                               model_trainer_artifact: ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("starting Model Evaluation")
            
            model_evaluation  = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                                                data_validation_artifact=data_validation_artifact,
                                                 model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info("Finishing Model Evaluation")
            return model_evaluation_artifact
        except Exception as e:
            raise ForestException(e,sys)
    
    def start_model_pusher(self,model_trainer_artifact: ModelTrainerArtifact):
        try:
            logging.info("starting Model Pusher")
            model_pusher_config = ModelPusherConfig()
            model_pusher = ModelPusher(model_trainer_artifact=model_trainer_artifact, model_pusher_config=model_pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("Finishing Model Pusher")
            return model_pusher_artifact
        except Exception as e:
            raise ForestException(e,sys)

    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_traniner_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            model_evalution_artifact = self.start_model_evaluation(data_validation_artifact=data_validation_artifact,model_trainer_artifact=model_traniner_artifact)
            model_pusher_artifact = self.start_model_pusher(model_trainer_artifact=model_traniner_artifact)
            return model_pusher_artifact 
            
            
            
        except Exception as e:
            raise ForestException(e,sys)
    


        

