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
        password=os.getenv('DB_PASSWORD')  # Replace with your MySQL password
    )

    cursor = conn.cursor()

    # Step 1: Create a new database
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS classicmodels")
        print("Database created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

    # Step 2: Use the newly created database
    cursor.execute("USE classicmodels")

    # Step 3: Create a table (if it doesn't exist)
    create_table_query = '''
    CREATE TABLE productlines (
  productLine varchar(50),
  textDescription varchar(4000) DEFAULT NULL,
  htmlDescription mediumtext,
  image mediumblob,
  PRIMARY KEY (productLine)
);
    '''
    cursor.execute(create_table_query)
    print("Table 'users' created or already exists.")

    # Step 4: Insert sample data
    insert_query = '''
    INSERT INTO users (name, age, email)
    VALUES (%s, %s, %s)
    '''
    sample_data = [
        ("Alice", 25, "alice@example.com"),
        ("Bob", 30, "bob@example.com"),
        ("Charlie", 35, "charlie@example.com")
    ]

    cursor.executemany(insert_query, sample_data)
    conn.commit()  # Commit the changes
    print("Data inserted successfully.")

    # Step 5: Query and display data to verify
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Users in database:")
    for row in results:
        print(row)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Access denied, check your username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

finally:
    # Step 6: Close the cursor and connection
    cursor.close()
    conn.close()
