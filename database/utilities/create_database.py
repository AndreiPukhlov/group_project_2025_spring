import mysql.connector
from mysql.connector import errorcode
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Connect to MySQL Server
try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),  # Replace with your MySQL username
        password=os.getenv('DB_PASSWORD'),  # Replace with your MySQL password
        database=''  # You can leave this blank to create a database
    )

    cursor = conn.cursor()

    # Read SQL file
    with open('mysqlsampledatabase.sql', 'r') as file:
        sql_queries = file.read()

    # Split queries by semicolon to handle multiple queries
    queries = sql_queries.split(';')

    # Execute each query individually
    for query in queries:
        query = query.strip()
        if query:  # If the query is not empty
            try:
                cursor.execute(query)
                conn.commit()  # Commit changes if the query modifies the database
                print(f"Executed query: {query}")
            except mysql.connector.Error as err:
                print(f"Error executing query: {err}")
                conn.rollback()  # Rollback in case of error

finally:
    # Close cursor and connection in the finally block
    cursor.close()
    conn.close()
    print("Connection closed.")
