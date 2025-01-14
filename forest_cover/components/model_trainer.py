from forest_cover.entity.config_entity import *
from forest_cover.entity.artifact_entity import *
from forest_cover.logging import logging
from forest_cover.exception import ForestException

from forest_cover.utils import load_numpy_array_data,load_object, save_object,save_numpy_array_data,evaluate_models
from forest_cover.ml.metrics.classification_metrics import classification_score
from forest_cover.ml.model.estimator import ForestPredictionModel

from sklearn.ensemble import (RandomForestClassifier,ExtraTreesClassifier)
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

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
            else:
                mlflow.sklearn.log_model(best_model,"model")
                
            

        except Exception as e:
            raise ForestException(e,sys)
    
    def initiate_model_training(self)->ModelTrainerArtifact:
        
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            x_train, y_train,x_test,y_test = (train_arr[:, :-1], train_arr[:, -1], test_arr[:,:-1],test_arr[:,-1])
            
                       
            x_train_sample, y_train_sample, x_test_sample, y_test_sample = self.random_train_samples(x_train, y_train,x_test,y_test)
            # this statement can be removed if we want to train the with the whole dataset instead of samples
            
            model= self.train_model(x_train_sample, y_train_sample, x_test_sample, y_test_sample)
            
            return model    
            
            
        except Exception as e:
            raise ForestException(e, sys)
        
    
    def random_train_samples(self,x_train, y_train, x_test, y_test, indices=30000):
        """ This function is solemly for the faster training due to large numbers of data points""" 
        logging.info(f"random sampling for training the data for {indices}")                       
        try:
                      
                sample_indices_train = np.random.choice(x_train.shape[0], size=indices, replace=False)
                x_train_sample = x_train[sample_indices_train]
                y_train_sample = y_train[sample_indices_train]
                sample_indices_test = np.random.choice(x_test.shape[0], size=indices, replace=False)
                x_test_sample = x_test[sample_indices_test]
                y_test_sample = y_test[sample_indices_test]
            
                return x_train_sample,y_train_sample,x_test_sample,y_test_sample
            
        except Exception as e:
                raise ForestException(e, sys)

            
        
    def train_model(self,x_train, y_train, x_test, y_test):
        models = {
            "RandomForestClassifier" : RandomForestClassifier(verbose=1,n_jobs=-1),
            "LightGBMClassifier" : LGBMClassifier(verbose=1,n_jobs=-1),
            "ExtraTreesClassifier" : ExtraTreesClassifier(verbose=1,n_jobs=-1),
            "CatBoostClassifier" : CatBoostClassifier(verbose=1)
            }
        
        params = {
            "RandomForestClassifier":{
                'criterion':['gini','entropy','log_loss'],
                'n_estimators': [10,20,40,50,100,300,500],
                'max_features':['sqrt','log2'],
                'max_depth':[None,2,4,6,8,10,20 ]
            },
            "LightGBMClassifier":{
            # 'objective':['multiclass'],
            # 'num_leaves': [2, 4, 6, 8, 10],
            # 'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],
            # 'n_estimators': [10,20,40,50,100,300,500,1000],
            # 'max_depth': [2, 4, 6, 8, 10]
            },
            
            "ExtraTreesClassifier":{
                # 'criterion':['gini','entropy','log_loss'],
                # 'n_estimators': [10,20,40,50,100,300,500,1000],
                # 'max_features':['sqrt','log2'],
                # 'max_depth':['None',2,4,6,8,10,20 ]
                
            },
            "CatBoostClassifier":{
                # 'loss_function': ['MultiClass'],
                # 'n_estimators': [10,20,40,50,100,300,500]
                # 'iterations': [10,20,40,50,100,300,500,1000],
                # 'depth': [2, 4, 6, 8, 10],
                # 'learning_rate': []         
                            
            }
        }
        
        model_report:dict = evaluate_models(x_train=x_train,y_train= y_train,x_test=x_test,y_test=y_test,models=models,params=params)
        
        best_model_score = max(sorted(model_report.values()))
        
        best_model_name  = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        
        best_model= models[best_model_name]
        
        print(best_model)
        
        y_train_pred  = best_model.predict(x_train)
        
        classification_train_metrics = classification_score(y_true = y_train,y_pred=y_train_pred)
        
        #track mlflow experiment
        
        self.track_ml_flow(best_model,classification_train_metrics)         
        
        y_test_pred = best_model.predict(x_test)
        
        classification_test_metrics = classification_score(y_true = y_test,y_pred=y_test_pred)
        
        self.track_ml_flow(best_model,classification_test_metrics)
        
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)
        
        Forest_Prediction_Model = ForestPredictionModel(preprocessor=preprocessor,model= best_model)
        save_object(self.model_trainer_config.trained_model_file_path,object=Forest_Prediction_Model)
        
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                      train_metric_artifact=classification_train_metrics,test_metric_artifact=classification_test_metrics)
        
        print(f"Model Trainer Artifact{model_trainer_artifact}")
        return model_trainer_artifact
    
    
        
        
        
        