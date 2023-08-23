import os,sys
from src.UberFares.exception import CustomException
from src.UberFares.logger import logging
from src.UberFares.entity.config import DataIngestionConfig
from src.UberFares.entity.artifact import DataIngestionArtifact
from pandas import DataFrame 


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        

    def export_data_to_feature_store(slef)->DataFrame:
        try:
            pass


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

