from dotenv import find_dotenv,load_dotenv
import pymongo
import certifi
import os
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Import database_name and collection_name form constant package
from src.UberFares.constants.database_name import DATABASE_NAME, COLLECTION_NAME



# Creating a class for mongodb connection
class MongodbClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongodbClient.client is None:
                mongo_url = os.getenv('MONGO_DB_URL')
                MongodbClient.client = pymongo.MongoClient(
                    mongo_url, tlsCAFile=certifi.where())
            self.client = MongodbClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e
