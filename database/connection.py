import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_connection_classic_model():
    config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': 'classicmodels',
        'raise_on_warnings': True
    }
    return mysql.connector.connect(**config)


def get_db_connection_film2():
    config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': 'film2',
        'raise_on_warnings': True
    }
    return mysql.connector.connect(**config)
