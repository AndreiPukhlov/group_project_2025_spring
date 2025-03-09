import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def driver():
    options = Options()

    # options.add_argument("--headless")
    # chrome_options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-cache")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


