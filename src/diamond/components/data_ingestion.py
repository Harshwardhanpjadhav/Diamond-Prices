import os
import sys
from pandas import DataFrame
from src.diamond.logger import logging
from src.diamond.exception import CustomException
from sklearn.model_selection import train_test_split
from src.diamond.entity.config import DataIngestionConfig
from src.diamond.entity.artifact import DataIngestionArtifact
from src.diamond.data_ascess.diamond_data_access import GetDiamondData


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def export_data_to_feature_store(slef) -> DataFrame:
        try:
            diamond = GetDiamondData()
            dataframe = diamond.export_collection_as_dataframe(
                collection_name=slef.data_ingestion_config.collection_name)
            feature_store_file_path = slef.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise CustomException(e, sys)

    def train_test_split(self, dataframe: DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class")

            dir_path = os.path.dirname(
                self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True)

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframee = self.export_data_to_feature_store()
            self.train_test_split(dataframe=dataframee)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)
