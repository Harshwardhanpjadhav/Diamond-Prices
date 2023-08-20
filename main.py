from src.UberFares.configuration.mongo_conn import MongodbClient



if __name__ == '__main__':

    mongo = MongodbClient()
    print(mongo.database)