import mysql.connector


def get_db_connection_classic_model():
    config = {
        'user': 'root',
        'password': 'Andy1722',
        'host': 'localhost',
        'database': 'classicmodels',
        'raise_on_warnings': True
    }
    return mysql.connector.connect(**config)


def get_db_connection_film2():
    config = {
        'user': 'root',
        'password': 'Andy1722',
        'host': 'localhost',
        'database': 'film2',
        'raise_on_warnings': True
    }
    return mysql.connector.connect(**config)
