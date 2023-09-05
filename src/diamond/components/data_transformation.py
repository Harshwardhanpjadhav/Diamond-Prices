import os
import sys

from src.diamond.logger import logging
from src.diamond.exception import CustomException
from src.diamond.entity.config import DataTransformationConfig
from src.diamond.utils.main_util import save_preprocessing_object
from src.diamond.constants.trainingpipeline import TAREGT_COLUMN_NAME
from src.diamond.entity.artifact import DataValidationArtifact, DataTransformationArtifact

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, MinMaxScaler

class DataTransformation:
    def __init(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(sys, e)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        logging.info("Startes reading Data")
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

    @classmethod
    def get_data_transformation_object(self) -> Pipeline:
        try:

            target_column = 'price'
            numerica_columns = ['carat', 'depth', 'table', 'x', 'y', 'z']
            categorical_columns = ['cut', 'color', 'clarity']

            # Numerical Pipeline
            numerical_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', RobustScaler())
            ])

            categorical_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore'))
            ])

            full_pipeline = ColumnTransformer([
                ('numerical_pipeline', numerical_pipeline, numerica_columns),
                ('categorical_pipeline', categorical_pipeline, categorical_columns)
            ])

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)
