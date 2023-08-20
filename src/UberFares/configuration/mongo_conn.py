import pymongo
import certifi

# Import database_name and collection_name form constant package
from src.UberFares.constants.database_name import DATABASE_NAME,COLLECTION_NAME

# Creating a class for mongodb connection 
class MongodbClient:
    client = None
    def __init__(self,database_name=DATABASE_NAME) -> None:
        try:
            if MongodbClient.client is None:
                mongo_url = "mongodb+srv://harsh:harsh@cluster0.aeotez0.mongodb.net/?retryWrites=true&w=majority"
                MongodbClient.client = pymongo.MongoClient(mongo_url,tlsCAFile=certifi.where())
            self.client = MongodbClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e :
            raise e