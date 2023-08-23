import os,sys
from src.UberFares.exception import CustomException
from src.UberFares.logger import logging
from src.UberFares.entity.config import DataIngestionConfig
from src.UberFares.entity.artifact import DataIngestionArtifact
from src.UberFares.data_ascess.uber_data import UberData
from pandas import DataFrame 


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        

    def export_data_to_feature_store(slef)->DataFrame:
        try:
            uber_data = UberData()
            dataframe = uber_data.export_collection_as_dataframe(collection_name=slef.data_ingestion_config.collection_name)
            feature_store_file_path = slef.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise CustomException(e,sys)
        

    def train_test_split_(slef,dataframe:DataFrame):
        try:
            pass


        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            pass


        except Exception as e:
            raise CustomException(e,sys)

