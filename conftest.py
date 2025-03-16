from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pytest
import mysql.connector
from mysql.connector import Error


@pytest.fixture(scope="session")  # module or session
def db_connection():
    """Fixture to establish a database connection and clean up after tests."""
    try:
        config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME', 'classicmodels'),  # Default DB
            'raise_on_warnings': True
        }
        connection = mysql.connector.connect(**config)
        yield connection  # Provide connection to tests

    except Error as e:
        pytest.fail(f"Error connecting to the database: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Database connection closed.")


@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """Fixture to get a fresh database cursor for each test."""
    cursor = db_connection.cursor(dictionary=False)
    yield cursor
    cursor.close()


@pytest.fixture()
def driver():
    options = Options()

    # options.add_argument("--headless")
    # chrome_options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-cache")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
