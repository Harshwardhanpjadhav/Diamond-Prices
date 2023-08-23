import os

# Target column name form dataset
TAREGT_COLUMN_NAME: str = 'fare_amount'
# Name of the pipeline
PIPELINE_NAME: str ='uber'
# Name of the artifact DIR
ARTIFACT_DIR: str = 'artifact'
# Dataset file name
FILE_NAME: str = 'uber.scv'

# Train File name
TRAIN_FILE_NAME: str = "train.csv"
# Test File name
TEST_FILE_NAME: str = "test.csv"
 
# Preprocessing PKL file name
PREPROCESSING_PIPELINE_OBJECT = "preprocessing.pkl"

# Model PKL file name
MODEL_FILE_NAME = "model.pkl"

# Schema file path
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")

#
SCHEMA_DROP_COLUMNS= 'drop_columns'

# Data ingestion 

DATA_INGESTION_COLLECTION_NAME:str = "uber"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:str="0.2"