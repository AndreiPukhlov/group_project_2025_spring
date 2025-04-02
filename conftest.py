import datetime
import logging
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pytest
import mysql.connector
from mysql.connector import Error
from _pytest.reports import TestReport
from _pytest.runner import CallInfo


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


@pytest.fixture()  # about scope in 'about_scope_for_pytest_fixture' file
def driver():
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    options = Options()
    if headless:
        options.add_argument("--headless")
    # options.add_argument("--headless")
    # chrome_options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-cache")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("test_logs.log"),  # Store logs in a file
            logging.StreamHandler()  # Show logs in the console
        ]
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.log_cli = True
    config.option.log_cli_level = "INFO"
    config.option.log_file = "test_logs.log"
    config.option.log_file_level = "INFO"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()


    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver and hasattr(driver, "save_screenshot"):
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)


            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(
                screenshot_dir,
                f"failed_{item.name}_{timestamp}.png"
            )

            try:
                driver.save_screenshot(screenshot_path)

                # add screenshot to HTML report if pytest-html is available
                if hasattr(report, "extra"):
                    from pytest_html import extras
                    report.extra.append(extras.image(screenshot_path))
            except Exception as e:
                print(f"Failed to take screenshot: {e}")

    return report


