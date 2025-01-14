from forest_cover.components import *
from forest_cover.entity.artifact_entity import *
from forest_cover.entity.config_entity import *
from forest_cover.exception import ForestException
from forest_cover.logging import logging
import pandas as pd
import numpy as np
from forest_cover.constants.training_pipe import TARGET_COLUMN_NAME

from imblearn.combine import SMOTEENN
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder

from forest_cover.constants import *
from forest_cover.utils import *



class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config:DataTransformationConfig):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config
        
    @staticmethod
    def read_data(file_path: str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
            
        except Exception as e:
            raise ForestException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Initiating Data Transformation")
            preprocessor  = self.get_data_transformer_object()
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN_NAME],axis=1)
            target_feature_train_df =train_df[TARGET_COLUMN_NAME]
    
            
            logging.info("Got the input and target features from the training data")
            
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN_NAME],axis=1)
            target_feature_test_df =test_df[TARGET_COLUMN_NAME]
            logging.info("Got the input and target features from the test data")
            
            input_feature_train_array = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessor.transform(input_feature_test_df)
            
            logging.info("Transformed the input features for train and test data")
            
            smt = SMOTEENN(sampling_strategy='minority')
            
            input_feature_train_final,target_feature_train_final = smt.fit_resample(input_feature_train_array,target_feature_train_df)
            logging.info("Balanced the training data using SMOTEENN")
            
            input_feature_test_final,target_feature_test_final = smt.fit_resample(input_feature_test_array,target_feature_test_df)
            logging.info("Balanced the test data using SMOTEENN")
            
            train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final,np.array(target_feature_test_final)]
            logging.info("Cocantenating the train and test arrays")
            
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,arr=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,arr=test_arr)
            
            logging.info("Saving the transformer object")
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            return data_transformation_artifact
            
            
        except Exception as e:
            raise ForestException(e,sys)
    
    def get_data_transformer_object(self)->object:
        try:
            _schema_config = read_yaml_file(training_pipe.SCHEMA_FILE_PATH)
            num_features = _schema_config['numerical_columns']
            
            numeric_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='mean')),
                ('scaler',RobustScaler())
            ])
            
            preprocessor = ColumnTransformer(
                [('Numerical_Pipeline',numeric_pipeline,num_features)]
            )
            
            logging.info("Transformer object created")
            
            return preprocessor
            
            
        except Exception as e:
            raise ForestException(e,sys)