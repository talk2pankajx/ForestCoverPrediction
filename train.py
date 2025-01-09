from forest_cover.components.data_ingestion import DataIngestion
from forest_cover.components.data_validation import DataValidation
from forest_cover.components.data_transformation import DataTransformation
from forest_cover.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from forest_cover.entity.config_entity import TrainingPipelineConfig
from forest_cover.logging import logging
from forest_cover.exception import ForestException
import sys
NUMEXPR_MAX_THREADS = 16



if __name__ == '__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiating data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Data validation Initiated")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        
        logging.info("Data Transformation started")
        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed")
        
        
    except Exception as e:
        raise ForestException(e,sys)