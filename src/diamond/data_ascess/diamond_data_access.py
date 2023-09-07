import os
import sys
from typing import Optional
from src.diamond.exception import CustomException
from src.diamond.logger import logging
from src.diamond.constants.database_name import DATABASE_NAME
from src.diamond.constants.env_variable import EnvironmentVariable as EV
from src.diamond.configuration.mongo_conn import MongodbClient
import pandas as pd
import numpy as np


class GetDiamondData:
    '''
    This class is used to fetch Data from MongoDB and return Dataframe
    '''

    def __init__(self):
        try:
            self.mongodb_client = MongodbClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise CustomException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:
            """
            export entire collectin as dataframe:
            return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongodb_client.database[collection_name]
            else:
                collection = self.mongodb_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)
            df.replace({0: np.nan}, inplace=True)

            return df

        except Exception as e:
            raise CustomException(e, sys)
