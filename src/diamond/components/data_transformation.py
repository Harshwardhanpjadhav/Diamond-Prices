import os
import sys

from src.diamond.logger import logging
from src.diamond.exception import CustomException
from src.diamond.entity.config import DataTransformationConfig
from src.diamond.utils.main_util import save_preprocessing_object,save_numpy_array_data
from src.diamond.constants.trainingpipeline import TAREGT_COLUMN_NAME
from src.diamond.entity.artifact import DataValidationArtifact, DataTransformationArtifact

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, MinMaxScaler,LabelEncoder,StandardScaler

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
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

            numerical_columns = ['carat','x']
            categorical_columns = ['cut', 'color', 'clarity']

            # Numerical Pipeline
            numerical_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                # ("scaler",StandardScaler())
            ])

            categorical_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore')),
                # ("scaler",StandardScaler(with_mean=False))
            ])

            logging.info("creating object")

            preprocessor = ColumnTransformer([
                ('numerical_pipeline', numerical_pipeline, numerical_columns),
                ('categorical_pipeline', categorical_pipeline, categorical_columns)
            ])

            return preprocessor


        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            preprocessor = self.get_data_transformation_object()

            input_train = train.drop(columns=[TAREGT_COLUMN_NAME,'y','z','depth','table'],axis=1)
            input_test = test.drop(columns=[TAREGT_COLUMN_NAME,'y','z','depth','table'],axis=1)

            output_train = train[TAREGT_COLUMN_NAME]
            output_test = test[TAREGT_COLUMN_NAME]

            input_feature_train = preprocessor.fit_transform(input_train)
            input_feature_test = preprocessor.transform(input_test)

            logging.info(f"input_feature_train{input_feature_train.shape}")
            logging.info(f"output_train{output_train.shape}")

            logging.info(f"input_feature_test{input_feature_test.shape}")
            logging.info(f"output_test{output_test.shape}")


            # preprocessor_object = preprocessor.fit(input_train)
            
            # logging.info(
            #     f"Applying preprocessing object on training dataframe and testing dataframe."
            # )

            
            # transformed_input_train_feature = preprocessor_object.transform(input_train)
            # transformed_input_test_feature =preprocessor_object.transform(input_test)
            # logging.info(transformed_input_test_feature)

            # smt = SMOTETomek(sampling_strategy="minority")

            # input_feature_train_final, target_feature_train_final = smt.fit_resample(
            #     transformed_input_train_feature, output_train
            # )

            # input_feature_test_final, target_feature_test_final = smt.fit_resample(
            #     transformed_input_test_feature, output_test
        
            logging.info(input_feature_train)
            logging.info(output_train)
            train_arr = np.c_[input_feature_train,np.array(output_train)]
            test_arr = np.c_[input_feature_test,np.array(output_test)]

            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_preprocessing_object( self.data_transformation_config.transformed_object_file_path, preprocessor,)

            data_transformation_artifact = DataTransformationArtifact(
                transformation_object_file_path = self.data_transformation_config.data_transformation_object_file_path,
                transformed_train_file_path = self.data_transformation_config.data_transformation_train_file_path,
                transformed_test_file_path = self.data_transformation_config.data_transformation_test_file_path
                )
            
            return data_transformation_artifact
        
        except Exception as e:
            raise CustomException(e, sys)
