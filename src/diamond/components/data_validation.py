import sys
import os
import pandas as pd
from src.diamond.logger import logging
from src.diamond.exception import CustomException
from src.diamond.entity.config import DataValidationConfig
from src.diamond.constants.trainingpipeline import SCHEMA_FILE_PATH
from src.diamond.utils.main_util import write_yaml_file, read_yaml_file
from src.diamond.entity.artifact import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config=DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        logging.info("Startes reading Data")
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)

    def validate_no_of_columns(self,dataframe=pd.DataFrame) -> bool:
        try:
            logging.info("Started Validating Number of columns >>>>>>")
            no_of_col = len(self._schema_config['columns'])
            logging.info(f"Required number of columns: {no_of_col}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")

            if len(dataframe.columns) == no_of_col:
                return True
            logging.info("calidation no of cloumns complete")
            return False
            
        except Exception as e:
            raise CustomException(e, sys)
        

    def is_numeric_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            logging.info("Started validating Numeric Col Exists >>>>>>>>>>>>")
            numeric_col = self._schema_config['numeric_columns']
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_col = []
            
            for num_col in numeric_col:
                if num_col not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_col.append(num_col)
                    
            logging.info(f"Missing numerical columns: {missing_numerical_col}")

            return numerical_column_present
        except Exception as e:
            raise CustomException(e,sys)
    

    def is_categorical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        logging.info("Started validating Categorical Col Exists >>>>>")
        cat_col = self._schema_config['categorical_columns']
        df_columns = dataframe.columns
        cat_col_present = True
        missing_cat_col = []
        for col in cat_col:
            if col not in df_columns:
                cat_col_present = False
                missing_cat_col.append(col)
        logging.info(f"Missing Categorical Column are {missing_cat_col}")

        return cat_col_present

    def detect_dataset_drift(self):
        pass

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:

            error_message=""

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            logging.info("------ Calling Read Data --------")
            train_dataframe = DataValidation.read_data(train_file_path)
            logging.info("Train Data Read sccessfull")
            test_dataframe = DataValidation.read_data(test_file_path)
            logging.info("Test Data Read sccessfull")

            logging.info("------ validate_no_of_columns --------")
            status = self.validate_no_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all columns"
            else:
                logging.info("Train dataset contains all columns")

            status = self.validate_no_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"test Datase Does not contain all columns"

            else:
                logging.info("Test dataset contains all columns")

            # is_numeric_columns_exist
            logging.info("------ is_numeric_columns_exist --------")
            status = self.is_numeric_columns_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all numeric columns"
            else:
                logging.info("Train dataset contains all numeric columns")
        
            status = self.is_numeric_columns_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all numeric columns"
            else:
                logging.info("Test dataset contains all numeric columns")

            # is_categorical_columns_exist
            logging.info("------ is_categorical_columns_exist --------")
            status = self.is_categorical_columns_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all categorical columns"
            else:
                logging.info("Train dataset contains all categorical columns")

            status = self.is_categorical_columns_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all categorical columns"
            else:
                logging.info("Test dataset contains all categorical columns")
            
            if len(error_message) > 0:
                raise Exception(error_message)


        except Exception as e:
            raise CustomException(e, sys)
