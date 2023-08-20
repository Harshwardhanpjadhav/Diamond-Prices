from src.UberFares.configuration.mongo_conn import MongodbClient
from src.UberFares.exception import CustomException
from src.UberFares.logger import logging

import os,sys

if __name__ == '__main__':
    a=MongodbClient()
    print(a.database_name)