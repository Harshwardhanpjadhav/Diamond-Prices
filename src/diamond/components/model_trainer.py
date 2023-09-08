import os
import sys
from src.diamond.logger import logging
from src.diamond.exception import CustomException
from src.diamond.entity.config import ModelTrainerConfig
from src.diamond.constants import trainingpipeline as tp
from src.diamond.ml.metrics import get_regression_score
from src.diamond.utils.main_util import load_numpy_array_data,load_object,save_object
from src.diamond.ml.estimator import diamond
from src.diamond.entity.artifact import ModelTrainerArtifact,DataTransformationArtifact

from sklearn.tree import DecisionTreeRegressor

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        
        try:
            self.model_trainer_config = model_trainer_config
            self.data_tranformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)
         


    def train_model(self,X_train,y_train):
        try:  
            model = DecisionTreeRegressor(max_depth=13,criterion='absolute_error')
            model.fit(X_train,y_train)
            return model
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_training(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_tranformation_artifact.transformed_train_file_path
            test_file_path = self.data_tranformation_artifact.transformed_test_file_path

            train_data = load_numpy_array_data(train_file_path)
            test_data = load_numpy_array_data(test_file_path)

            X_train = train_data[:, :-1]
            y_train = train_data[:, -1]
            X_test = test_data[:, :-1]
            y_test = test_data[:, -1]

            model = self.train_model(X_train,y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_metric_artifact = get_regression_score(y_train,y_train_pred)
            test_metric_artifact = get_regression_score(y_test,y_test_pred)


            if train_metric_artifact.accuracy_score == self.model_trainer_config.expected_accuracy:
                raise Exception("The model is a perfect fit.")

            logging.info(train_metric_artifact.accuracy_score)
            logging.info(test_metric_artifact.accuracy_score)

            diff =  abs(train_metric_artifact.accuracy_score - test_metric_artifact.accuracy_score)

            if diff > 0.05:
                raise Exception("The model is potentially overfitting.")
            else:
                print("The model is likely a good fit.")


            preprocessor = load_object(file_path=self.data_tranformation_artifact.transformed_data_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            diamond_model = diamond(preprocessor=preprocessor,model=model)

            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=diamond_model)


            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_metric_artifact,
                test_metric_artifact=test_metric_artifact)
            
            return model_trainer_artifact
            


        except Exception as e: 
            raise CustomException(e, sys)
