import os
import time

import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from utilities.decorators import time_count

load_dotenv()

# Database and file details
db_name = "English"
csv_file_name = "English_dictionary_master.csv"

# Get the current script's directory (absolute path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Move up to the root directory (go up two levels)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir, os.pardir))

# Database connection details
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

file_path = os.path.join(ROOT_DIR, 'data', 'csv_files', csv_file_name)


def get_execution_time(func):
    start_time = time.time()
    func()
    end_time = time.time()
    importing_time = (end_time - start_time) / 60
    print(f"It took {importing_time} minutes to import this csv file")


def create_database():
    """Create the database if it does not exist."""
    try:
        # Connect to MySQL without specifying a database
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


# Ensure database exists
create_database()

# Create a database connection using SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{db_name}")


@time_count
def import_csv(table_name=None, chunk_size=5000):  # Table name could be added here
    """Dynamically import CSV data into a MySQL table"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Read CSV
    df = pd.read_csv(file_path)

    # Check if the DataFrame is empty
    if df.empty:
        print("No data found in CSV.")
        return

    print(f"Dataframe has {len(df)} rows.")
    print(df.head())  # Check the first few rows of data

    # Use filename as table name if not provided
    if table_name is None:
        table_name = os.path.splitext(os.path.basename(file_path))[0]

    print(f"Importing {file_path} into `{table_name}`")

    # Get column types and create table if not exists
    metadata = MetaData()
    metadata.reflect(bind=engine)

    if table_name not in metadata.tables:
        df.head(0).to_sql(table_name, engine, if_exists="fail", index=False)
        print(f"Table `{table_name}` created.")

    # Insert data in chunks - for big files
    try:
        print(f"Inserting data into `{table_name}`...")
        df.to_sql(table_name, engine, if_exists="append", index=False, chunksize=chunk_size, method="multi")
        print(f"Data successfully inserted into `{table_name}`.")
    except OperationalError as e:
        print(f"Error inserting data: {e}")
        print(df.head())  # Print the first few rows of the DataFrame to inspect what's being inserted


import_csv()
