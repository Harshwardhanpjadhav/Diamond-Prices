from src.UberFares.configuration.mongo_conn import MongodbClient
from src.UberFares.exception import CustomException
from src.UberFares.logger import logging

import os,sys


def s():
    try:

        x=1/0
        return x
    except Exception as e:
        raise CustomException(e, sys)


if __name__ == '__main__':
    logging.info("everything is fine")