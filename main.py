from src.diamond.configuration.mongo_conn import MongodbClient
from src.diamond.exception import CustomException
from src.diamond.logger import logging
from src.diamond.pipeline.training_pipeline import TrainingPipeline

import os
import sys

if __name__ == '__main__':
    t = TrainingPipeline()
    t.run_pipeline()
