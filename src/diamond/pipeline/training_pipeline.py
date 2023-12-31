import sys
import os
from src.diamond.logger import logging
from src.diamond.exception import CustomException
from src.diamond.components.data_ingestion import DataIngestion
from src.diamond.components.data_validation import DataValidation
from src.diamond.components.data_transformation import DataTransformation
from src.diamond.components.model_evaluation import ModelEvaluation
from src.diamond.components.model_pusher import ModelPusher
from src.diamond.components.model_trainer import ModelTrainer
from src.diamond.entity.artifact import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from src.diamond.entity.config import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig


class TrainingPipeline:
    '''
    This class is used to create the training pipeline object
    '''

    is_pipeline_running = False

    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()

        self.data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=training_pipeline_config)

        self.data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config)

        self.data_transformation_config = DataTransformationConfig(
            training_pipeline_config=training_pipeline_config)

        self.model_trainer_config = ModelTrainerConfig(
            training_pipeline_config=training_pipeline_config)

        self.model_evaluation_config = ModelEvaluationConfig(
            training_pipeline_config=training_pipeline_config)

        self.model_pusher_config = ModelPusherConfig(
            training_pipeline_config=training_pipeline_config)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Started Data Ingestion >>>>>")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info(f"Completed Data Ingestion {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_validation(self, data_ingetion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Started Data Validation >>>>>")
            logging.info(data_ingetion_artifact)
            data_validation = DataValidation(
                data_ingetion_artifact,
                data_validation_config=self.data_validation_config)

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info(
                f"Completed Data Validation {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info("Started  start_data_transformation >>>>>")
            data_transformation = DataTransformation(
                data_validation_artifact,
                data_transformation_config=self.data_transformation_config)
            logging.info("end  start_data_transformation >>>>>")
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info("Started  start_model_trainer >>>>>")

            model_trainer = ModelTrainer(
                data_transformation_artifact,
                model_trainer_config=self.model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_training()
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact, data_validation_artifact: DataValidationArtifact) -> ModelEvaluationArtifact:
        try:
            logging.info("Started  start_model_evaluation >>>>>")

            model_evaluation = ModelEvaluation(
                model_trainer_artifact,
                data_validation_artifact,
                model_evaluation_config=self.model_evaluation_config
            )
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_pusher(self, model_eval_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:
            model_pusher = ModelPusher(self.model_pusher_config,
                                       model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()

            return model_pusher_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        try:
            TrainingPipeline.is_pipeline_running =True
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(
                data_ingetion_artifact=data_ingestion_artifact)

            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact)

            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact)

            model_evaluation_artifact = self.start_model_evaluation(
                model_trainer_artifact=model_trainer_artifact,
                data_validation_artifact=data_validation_artifact
            )

            model_pusher_artifact = self.start_model_pusher(
                model_eval_artifact=model_evaluation_artifact
            )

            TrainingPipeline.is_pipeline_running =False
        except Exception as e:
            raise CustomException(e, sys)
