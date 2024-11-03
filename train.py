from forest_cover.pipeline.training_pipeline import TrainingPipeline
from forest_cover.entity.config_entity import TrainingPipelineConfig
from forest_cover.logging import logging



if __name__ == '__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        
        training_pipeline  = TrainingPipeline(training_pipeline_config=training_pipeline_config)
        
        training_pipeline.run_pipeline()
    except Exception as e:
        logging.info(e)
        print(e)
        