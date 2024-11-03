from forest_cover.exception import ForestException
from forest_cover.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from forest_cover.entity.artifact_entity import DataIngestionArtifact
from forest_cover.components.data_ingestion import DataIngestion
from forest_cover.logging import logging
import os,sys

class TrainingPipeline:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            
            self.training_pipeline_config = training_pipeline_config
        except Exception as e:
            raise ForestException(e,sys)  # Raise the exception if any error occurs in initialization
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config  = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        
        except ForestException as e:
            raise ForestException(e,sys) 
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
        except ForestException as e:
            raise ForestException(e,sys)        