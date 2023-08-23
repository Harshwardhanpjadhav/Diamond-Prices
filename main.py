from src.UberFares.configuration.mongo_conn import MongodbClient
from src.UberFares.exception import CustomException
from src.UberFares.logger import logging
from src.UberFares.pipeline.training_pipeline import TrainingPipeline

import os,sys

if __name__ == '__main__':
    t = TrainingPipeline()
    t.run_pipeline()
