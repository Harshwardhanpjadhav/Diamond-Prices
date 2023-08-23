from src.UberFares.entity.config import TrainingPipelineConfig,DataIngestionConfig
from src.UberFares.logger import logging
from src.UberFares.exception import CustomException
import sys,os
from src.UberFares.entity.artifact import DataIngestionArtifact

class TrainingPipeline:
    '''
    This class is used to create the training pipeline object
    '''
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("startes data ingestion")
            logging.info("completed data ingestion")
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_validation(self):
        try:
            pass 
        except Exception as e:
            raise CustomException(e,sys)

    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact= self.start_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) 