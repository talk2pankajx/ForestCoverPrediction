import os
import pandas as pd
import numpy as np
from forest_cover.constants.training_pipe.s3_bucket import TRAINING_BUCKET_NAME,PREDICTION_BUCKET_NAME

## common constants

TARGET_COLUMN_NAME:str = "Cover_Type"
PIPELINE_NAME:str = "ForesCoverTypePrediction"
ARTIFACTS_DIR:str = "artifact"
FILE_NAME:str = "Covtype.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH:str = os.path.join("data_schema","schema.yaml")

SAVED_MODELS_DIR:str = os.path.join("saved_models")
MODEL_FILE_NAME:str = "model.pkl"


## Constants related to DataIngestion Var name

DATA_INGESTION_COLLECTION_NAME :str = "forest_cols"
DATA_INGESTION_DATABASE_NAME:str = "forest_db"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float = 0.2 

## constants related to Data Validation Var name

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "data_drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME :str = "report.yaml"

## constant related to Data Transformation Var name

DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
PREPROCESSED_OBJECT_FILE_NAME = "preprocessor.pkl"

## constants related to Model Trainer Var name

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_FILE_NAME = "model.pkl"
MODEL_TRAINER_CONFIG_FILE_PATH : str = os.path.join("data_schema","model.yaml")


## constants related to Model Evaluation var name

MODEL_EVALUATION_CHANGED_THRESHOLD :float = 0.02
MODEL_PUSHER_BUCKET_NAME = 'forestcoverbucket2'
MODEL_PUSHER_S3_KEY = 'model_registry'

PREDICTION_DATA_BUCKET =PREDICTION_BUCKET_NAME
PREDICTION_INPUT_FILE_NAME = "test.csv"
PREDICTION_OUTPUT_FILE_NAME = "forest_prediction.csv"
MODEL_BUCKET_NAME = TRAINING_BUCKET_NAME





