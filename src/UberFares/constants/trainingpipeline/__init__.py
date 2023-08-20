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