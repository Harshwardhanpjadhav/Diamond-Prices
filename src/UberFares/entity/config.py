from dataclasses import dataclass
from datetime import datetime
import os
from src.UberFares.constants.trainingpipeline import PIPELINE_NAME,ARTIFACT_DIR

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
       timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
       self.pipeline_name:str = PIPELINE_NAME
       self.artifact_dir:str = os.path.join(ARTIFACT_DIR,timestamp)
       self.timestamp:str = timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,)