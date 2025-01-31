import sys
from forest_cover.exception import ForestException
from forest_cover.logging import logging
from forest_cover.entity.artifact_entity import *
from forest_cover.entity.config_entity import *
from forest_cover.entity.s3_estimator import ForestEstimator
from forest_cover.cloud_storage.aws_storage import SimpleStorageService

class   ModelPusher:
    def __init__(self, model_trainer_artifact: ModelTrainerArtifact, model_pusher_config: ModelPusherConfig):
        self.s3 = SimpleStorageService()
        self.model_pusher_config =  model_pusher_config
        self.model_trainer_artifact = model_trainer_artifact
        self.forest_estimator = ForestEstimator(bucket_name=model_pusher_config.bucket_name,model_path=self.model_pusher_config.s3_model_key_path)
    
    def initiate_model_pusher(self)-> ModelPusherArtifact:
        logging.info("Entered the model pusher method of ModelPusher")
        
        try:
            logging.info("uploading artifacts to s3 bucket")
            self.forest_estimator.save_model(from_file=self.model_trainer_artifact.trained_model_file_path)
            model_pusher_artifact  = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,s3_model_key_path=self.model_pusher_config.s3_model_key_path)
            logging.info("uploaded artifacts folder to s3 bucket")
            
            logging.info("Exited the initiate model_pusher method of ModelPusher Class")
            return model_pusher_artifact
        except Exception as e:
            raise ForestException(e, sys)

    