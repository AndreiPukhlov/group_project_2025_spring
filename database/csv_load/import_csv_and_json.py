import os
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from utilities.decorators import time_count

load_dotenv()

db_name = "jeopardy"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir, os.pardir))

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def create_database():
    """Create the database if it does not exist."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database `{db_name}` checked/created.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()
        connection.close()


create_database()

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{db_name}")

@time_count
def import_file(file_name, file_type="csv", chunk_size=5000):
    """
    Dynamically import data from a CSV or JSON file into a MySQL table.

    :param file_name: Name of the file (without path)
    :param file_type: Either "csv" or "json"
    :param chunk_size: Number of rows inserted at a time
    """
    file_path = os.path.join(ROOT_DIR, 'data', 'csv_files', file_name)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    if file_type == "csv":
        df = pd.read_csv(file_path)
    elif file_type == "json":
        df = pd.read_json(file_path)
    else:
        print(f"Unsupported file type: {file_type}")
        return

    df.rename(columns=lambda x: x.strip(), inplace=True)

    if df.empty:
        print(f"No data found in {file_type.upper()}.")
        return

    print(f"Dataframe has {len(df)} rows.")
    print(df.head())

    table_name = os.path.splitext(file_name)[0]

    print(f"Importing {file_path} into `{table_name}`")

    metadata = MetaData()
    metadata.reflect(bind=engine)

    if table_name not in metadata.tables:
        df.head(0).to_sql(table_name, engine, if_exists="fail", index=False)
        print(f"Table `{table_name}` created.")

    try:
        print(f"Inserting data into `{table_name}`...")
        df.to_sql(table_name, engine, if_exists="append", index=False, chunksize=chunk_size, method="multi")
        print(f"Data successfully inserted into `{table_name}`.")
    except OperationalError as e:
        print(f"Error inserting data: {e}")
        print(df.head())


import_file("JEOPARDY_CSV.csv", file_type="csv")  # for CSV
# import_file("JEOPARDY_DATA.json", file_type="json")  # for JSON
