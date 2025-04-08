import time

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_driver():   # function returns webdriver and can be used from anywhere
    driver = webdriver.Chrome()
    return driver


browser = webdriver.Chrome()         # global variable
url = "https://www.saucedemo.com/"   # global variable


class TestSmth:

    @pytest.mark.skip
    def test_url_status(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        # local variable - not seen from outside the method
        driver.get("https://www.apple.com")
        expected_url = "https://www.apple.com/"   # local variable - not seen from outside the method
        assert driver.current_url == expected_url
        driver.quit()

    @pytest.mark.skip
    def test_apple(self):

        browser.get("https://www.apple.com")   # global variable used
        time.sleep(3)
        expected_title = "Apple"
        assert browser.title == expected_title
        browser.quit()

    @pytest.mark.skip
    def test_login(self):
        driver = get_driver()              # function used
        # open AUT
        driver.get(url)
        # enter user_name
        # driver.find_element("", "")
        driver.find_element("css selector", "#user-name").send_keys("standard_user")
        # enter_password
        driver.find_element("css selector", "#password").send_keys("secret_sauce")
        # click button Login
        driver.find_element("css selector", "#login-button").click()
        # click navigation drawer
        driver.find_element("css selector", "#react-burger-menu-btn").click()
        # Logout button presented
        time.sleep(2)
        expected_result = driver.find_element("css selector", "#logout_sidebar_link").is_displayed()
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert expected_result
        assert driver.current_url == expected_url
        driver.quit()

