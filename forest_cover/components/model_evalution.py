import  sys
import pandas as pd
from forest_cover.entity.artifact_entity import *
from forest_cover.entity.config_entity import *
from forest_cover.exception import ForestException
from forest_cover.logging import logging
from dataclasses import dataclass
from typing import Optional
from forest_cover.entity.s3_estimator import ForestEstimator
from forest_cover.utils import *
from sklearn.metrics import f1_score
from forest_cover.constants.training_pipe import TARGET_COLUMN_NAME


@dataclass
class EvaluateModelResponse(object):
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted : bool
    difference : float
    
    
class ModelEvaluation:
    def __init__(self,model_evaluation_config : ModelEvaluationConfig, data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
            try:
                self.model_evaluation_config = model_evaluation_config
                self.data_validation_artifact = data_validation_artifact
                self.model_trainer_artifact = model_trainer_artifact
            except Exception as e:
                raise ForestException(e,sys)
    
    def get_best_model(self)->Optional[ForestEstimator]:
        try:
            bucket_name = self.model_evaluation_config.bucket_name
            model_path =  self.model_evaluation_config.s3_model_key_path
            f_estimator = ForestEstimator(bucket_name=bucket_name,model_path=model_path)
            
            if f_estimator.is_model_present(model_path=model_path):
                return f_estimator
            return None
        except Exception as e:
            raise ForestException(e,sys)
    
    def evaluate_model(self)->EvaluateModelResponse:
        try:
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)
            if test_df.columns == 'Cover_Type':
                X = test_df.drop(columns=[TARGET_COLUMN_NAME],axis=1, inplace=True)
                y = test_df[TARGET_COLUMN_NAME]
            trained_model = load_object(file_path=self.model_trainer_artifact.trained_model_file_path)
            y_hat_trained_model  = trained_model.predict(X)
            
            trained_model_f1_score = f1_score(y,y_hat_trained_model,average='micro')
            best_model_f1_score = None
            best_model= self.get_best_model()
            if best_model is not None:
                y_hat_best_model = best_model.predict(X)
                best_model_f1_score = f1_score(y,y_hat_best_model,average='micro')
                
            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score
            result = EvaluateModelResponse(
                trained_model_f1_score = trained_model_f1_score,
                best_model_f1_score = best_model_f1_score,
                is_model_accepted=trained_model_f1_score>tmp_best_model_score,
                difference = trained_model_f1_score - tmp_best_model_score
            )
            
            logging.info(f"Result: {result}")
            return result

        except Exception as e:
            raise ForestException(e,sys)
    def initiate_model_evaluation(self):
        try:
            eval_model_response = self.evaluate_model()
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=eval_model_response.is_model_accepted,
                best_model_path=self.model_trainer_artifact.trained_model_file_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=eval_model_response.difference
            )
            
            logging.info(f"Model Evaluation: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise ForestException(e,sys) from e
    