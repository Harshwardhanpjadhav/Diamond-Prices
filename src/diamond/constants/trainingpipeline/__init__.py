import os

# Target column name form dataset
TAREGT_COLUMN_NAME: str = 'fare_amount'
# Name of the pipeline
PIPELINE_NAME: str ='uber'
# Name of the artifact DIR
ARTIFACT_DIR: str = 'artifact'
# Dataset file constant name
FILE_NAME: str = 'uber.csv'

# Train File constant name
TRAIN_FILE_NAME: str = "train.csv"
# Test File constant name
TEST_FILE_NAME: str = "test.csv"
 
# Preprocessing PKL constant file name
PREPROCESSING_PIPELINE_OBJECT = "preprocessing.pkl"

# Model PKL file constant name
MODEL_FILE_NAME = "model.pkl"

# Schema file path constant
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")
SCHEMA_DROP_COLUMNS= 'drop_columns'

# Data ingestion constant
DATA_INGESTION_COLLECTION_NAME:str = "uberfareprice"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2

# Data Validation Constant
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR_NAME:str= "validated"
DATA_VALIDATION_INVALID_DIR_NAME:str= "invalid"
DATA_VALIDATION_DRIFY_REPORT_DIR_NAME:str = "drift_report"
DATA_VALIDATION_DRIFY_REPORT_FILE_NAME:str = "report.yaml"