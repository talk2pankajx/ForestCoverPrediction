from forest_cover.components.data_ingestion import DataIngestion
from forest_cover.entity.config_entity import DataIngestionConfig
from forest_cover.entity.config_entity import TrainingPipelineConfig
from forest_cover.logging import logging
from forest_cover.exception import ForestException
import sys




if __name__ == '__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiating data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        
    except Exception as e:
        raise ForestException(e,sys)