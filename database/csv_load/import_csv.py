# To run this script in terminal run: - python import_csv.py

import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import os

from dotenv import load_dotenv
load_dotenv()
# Get the current script's directory (absolute path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Move up to the root directory (go up two levels)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir, os.pardir))

# Database connection details

DB_HOST = "localhost"
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = "Film"
TABLE_NAME = "SF_movies"
CSV_FILE = os.path.join(ROOT_DIR, 'data', 'csv_files', 'yitu-d5am_version_111.csv')  # Path to your CSV file

# Step 1: Read CSV to get column names and data types
df = pd.read_csv(CSV_FILE)

# Step 2: Convert Pandas dtypes to MySQL-compatible types
dtype_mapping = {
    "int64": "INT",
    "float64": "FLOAT",
    "object": "VARCHAR(255)",
}

# columns_sql = ", ".join(
#     f"`{col}` {dtype_mapping.get(str(df[col].dtype), 'VARCHAR(255)')}"
#     for col in df.columns
# )

columns_sql = ", ".join(
    f"`{col}` {'TEXT' if col == 'fun_facts' else dtype_mapping.get(str(df[col].dtype), 'VARCHAR(255)')}"
    for col in df.columns
)

# Step 3: Connect to MySQL
conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
cursor = conn.cursor()

# Step 4: Drop table if it exists (optional)
cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")

# Step 5: Create table dynamically
create_table_query = f"CREATE TABLE {TABLE_NAME} ({columns_sql});"
cursor.execute(create_table_query)
print(f"Table `{TABLE_NAME}` created successfully.")

# Step 6: Insert data into the table using Pandas
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False)

print(f"Data imported successfully into `{TABLE_NAME}`.")

# Step 7: Close connections
cursor.close()
conn.close()
