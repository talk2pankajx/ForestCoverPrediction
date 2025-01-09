import os
import pandas as pd
import numpy as np

## common constants

TARGET_COLUMN_NAME:str = "Cover_Type"
PIPELINE_NAME:str = "ForesCoverTypePrediction"
ARTIFACTS_DIR:str = "artifact"
FILE_NAME:str = "Covtype.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH:str = os.path.join("data_schema","schema.yaml")


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