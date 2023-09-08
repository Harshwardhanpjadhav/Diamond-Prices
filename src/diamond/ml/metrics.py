from src.diamond.entity.artifact import ClassificationMetricArtifact
from src.diamond.exception import CustomException
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os
import sys


def get_regression_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        model_accuracy_score = r2_score(y_true, y_pred)
        model_mean_absolute_error = mean_absolute_error(y_true, y_pred)
        model_mean_squared_error = mean_squared_error(y_true, y_pred)

        classsification_metric = ClassificationMetricArtifact(accuracy_score=model_accuracy_score,
                                                              mean_squared_error=model_mean_absolute_error,
                                                              mean_absolute_error=model_mean_squared_error)
        return classsification_metric
    except Exception as e:
        raise CustomException(e, sys)
