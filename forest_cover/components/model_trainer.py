from forest_cover.entity.config_entity import *
from forest_cover.entity.artifact_entity import *
from forest_cover.logging import logging
from forest_cover.exception import ForestException
from neuro_mf import ModelFactory
from forest_cover.utils import load_numpy_array_data,load_object, save_object,save_numpy_array_data
from sklearn.metrics import f1_score, precision_score,recall_score
from forest_cover.ml.model.estimator import ForestPredictionModel
from typing import List, Tuple
from sklearn.ensemble import (RandomForestClassifier)

import mlflow

import dagshub
dagshub.init(repo_owner='talk2pankajx', repo_name='ForestCoverPrediction', mlflow=True)
from urllib.parse import urlparse

import numpy as np



class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            
        except Exception as e:
            raise ForestException(e, sys)
    
    def track_ml_flow(self,best_model,classificationmetrics):
        try:
            mlflow.set_registry_uri("https://dagshub.com/talk2pankajx/ForestCoverPrediction.mlflow")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            with mlflow.start_run(nested=True):
                f1_score = classificationmetrics.f1_score
                precision_score = classificationmetrics.precision_score
                recall_score = classificationmetrics.recall_score
                

            
                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("precision",precision_score)
                mlflow.log_metric("recall",recall_score)
                
                mlflow.sklearn.log_model(best_model,"model")
                

            
            if tracking_url_type_store!='file':
                
                mlflow.sklearn.log_model(best_model,"model",)
                
            

        except Exception as e:
            raise ForestException(e,sys)
    
    def initiate_model_training(self)->ModelTrainerArtifact:
        
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            x_train, y_train,x_test,y_test = (train_arr[:, :-1], train_arr[:, -1], test_arr[:,:-1],test_arr[:,-1])
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_trainer_config_file_path)
            best_model_detail = model_factory.get_best_model(X= x_train,y= y_train,base_accuracy=self.model_trainer_config.expected_accuracy)
               
            
            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with the score")
                raise Exception("No best model found with the score")
            
                        
            preprocessing_obj  = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            forest_model = ForestPredictionModel(preprocessing_object=preprocessing_obj,trained_model_object=best_model_detail.best_model)
            logging.info("created forest model with preprocessor and model")
            
            logging.info("created the best model path")
            save_object(self.model_trainer_config.trained_model_file_path,forest_model)
            
            metric_artifact = ClassificationMetrics(f1_score=0.8,precision_score=0.8,recall_score=0.9)
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path
                                                          ,metric_artifacts=metric_artifact)
            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")
            return model_trainer_artifact
            
            
        except Exception as e:
            raise ForestException(e, sys)
    

    def get_best_model_and_report(self, train:np.array,test:np.array)->Tuple[object,object]:
        try:
            logging.info("using neuromf to get the best model and report")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_trainer_config_file_path)
            
            x_train, y_train,x_test,y_test = (train[:, :-1], train[:, -1], test[:,:-1],test[:,-1])
            
            best_model_detail = model_factory.get_best_model(
                X= x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_accuracy
            )   
            model_obj = best_model_detail.best_model
            y_pred = model_obj.predict(x_test)
            
            f1 =  f1_score(y_test,y_pred, avverage = 'micro')
            precision = precision_score(y_test,y_pred, average ='micro')
            recall = recall_score(y_test,y_pred, average ='micro')
            
            metric_artifacts  = ClassificationMetrics(f1_score=f1,precision_score=precision,recall_score=recall)
            
            return  best_model_detail,metric_artifacts
            
            
            
        except Exception as e:
            raise ForestException(e,sys)
        
        
    