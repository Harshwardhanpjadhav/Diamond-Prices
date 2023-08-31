import os
import sys
import pandas as pd
from src.diamond.logger import logging
from src.diamond.utils import main_util as utils
from scipy.stats import ks_2samp, chi2_contingency
from src.diamond.exception import CustomException
from src.diamond.entity.config import DataValidationConfig
from src.diamond.constants.trainingpipeline import SCHEMA_FILE_PATH
from src.diamond.utils.main_util import write_yaml_file, read_yaml_file
from src.diamond.entity.artifact import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config=DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        logging.info("Startes reading Data")
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

    def validate_no_of_columns(self, dataframe=pd.DataFrame) -> bool:
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
            raise CustomException(e, sys)

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

    def detect_numeric_drift(self, base_df, current_df, threshold=0.05) -> bool:
        logging.info("Started Detect Dataset Drift >>>>>")
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                P_value = is_same_dist.pvalue
                logging.info(f"{P_value} and {threshold}")
                if threshold <= P_value:
                    is_found = False
                else:
                    is_found = True
                    status = False

                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found

                }})

            drift_report_file_path = self.data_validation_config.drift_report_file_num

            # Create directory
            dir_path = os.path.dirname(drift_report_file_path)

            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status

        except Exception as e:
            raise CustomException(e, sys)

    def detect_categorical_drift(self, base_df, current_df, threshold=0.05) -> bool:
        status = True
        report = {}
        for co in base_df.columns:
            freq_table_train = base_df[co].value_counts()
            freq_table_operational = current_df[co].value_counts()
            expected_freqs = freq_table_train / freq_table_train.sum()
            chi2_stat, p_val, dof, _ = chi2_contingency(
                [freq_table_operational, expected_freqs * len(current_df)])

            if p_val <= threshold:
                is_found = True
            else:
                is_found = False
                status = True

                report.update({co: {
                    "p_value": float(p_val),
                    "drift_status": is_found

                }})

        drift_report_file_path = self.data_validation_config.drift_report_file_cat

        dir_path = os.path.dirname(drift_report_file_path)

        write_yaml_file(file_path=drift_report_file_path, content=report)

        return status

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:

            error_message = ""

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            logging.info("-------- Calling Read Data --------")
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
            status = self.is_categorical_columns_exist(
                dataframe=train_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all categorical columns"
            else:
                logging.info("Train dataset contains all categorical columns")

            status = self.is_categorical_columns_exist(
                dataframe=test_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all categorical columns"
            else:
                logging.info("Test dataset contains all categorical columns")

            if len(error_message) > 0:
                raise Exception(error_message)

            train_df_nu = utils.numerical_col(df=train_dataframe)
            test_df_nu = utils.numerical_col(df=test_dataframe)

            train_df_cat = utils.categorical_col(df=train_dataframe)
            test_df_cat = utils.categorical_col(df=test_dataframe)

            status = self.detect_categorical_drift(
                base_df=train_df_cat,
                current_df=test_df_cat

            )

            status = self.detect_numeric_drift(
                base_df=train_df_nu,
                current_df=test_df_nu

            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file
            )

            logging.info(
                f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)
