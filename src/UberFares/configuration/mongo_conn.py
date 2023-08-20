import pymongo
import certifi
import os
from src.UberFares.constants.env_variable import EnvironmentVariable

# Import database_name and collection_name form constant package
from src.UberFares.constants.database_name import DATABASE_NAME, COLLECTION_NAME



# Creating a class for mongodb connection
class MongodbClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            mymongo_url = EnvironmentVariable.mongo_url
            if MongodbClient.client is None:
                MongodbClient.client = pymongo.MongoClient(
                    mymongo_url, tlsCAFile=certifi.where())
            self.client = MongodbClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e
