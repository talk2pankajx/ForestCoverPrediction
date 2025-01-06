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


## Constants related to DataIngestion Var name

DATA_INGESTION_COLLECTION_NAME :str = "forest_cols"
DATA_INGESTION_DATABASE_NAME:str = "forest_db"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float = 0.2 