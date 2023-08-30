import sys,os
from src.diamond.logger import logging
from src.diamond.exception import CustomException
from src.diamond.components.data_ingestion import DataIngestion
from src.diamond.components.data_validation import DataValidation
from src.diamond.entity.artifact import DataIngestionArtifact,DataValidationArtifact
from src.diamond.entity.config import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig

class TrainingPipeline:
    '''
    This class is used to create the training pipeline object
    '''
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        self.data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Started Data Ingestion >>>>>")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Completed Data Ingestion {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_validation(self,data_ingetion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info("Started Data Validation >>>>>") 
            data_validation = DataValidation(data_ingetion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Completed Data Validation {data_validation_artifact}")
            return data_validation_artifact
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
            data_validation_artifact = self.start_data_validation(data_ingetion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise CustomException(e,sys) 