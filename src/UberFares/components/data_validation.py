from src.UberFares.constants.trainingpipeline import SCHEMA_FILE_PATH
from src.UberFares.entity.artifact import DataIngestionArtifact, DataValidationArtifact
from src.UberFares.entity.config import DataValidationConfig
from src.UberFares.utils.main_util import write_yaml_file,read_yaml_file
from src.UberFares.logger import logging
import pandas as pd
import os
import sys
from src.UberFares.exception import CustomException


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config=DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def read_data(self, file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

    def is_numeric_columns_exist(self,dataframe:pd.DataFrame) -> bool:
        numeric_col = self._schema_config('numeric_col')
        pass

    def validate_no_of_columns(self,dataframe=pd.DataFrame) -> bool:
        try:
            no_of_col =  self._schema_config('columns')
            if len(dataframe.columns) == no_of_col:
                return True 
            return False 
        except Exception as e:
            raise CustomException(e, sys)

    def detect_dataset_drift(self):
        pass

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            status = self.validate_no_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all columns"

            status = self.validate_no_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"test Datase Does not contain all columns"                


        except Exception as e:
            raise CustomException(e, sys)
