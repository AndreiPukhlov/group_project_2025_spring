import time
from selenium import webdriver


def get_driver():   # function returns webdriver and can be used from anywhere
    driver = webdriver.Chrome()
    return driver


driver_ = webdriver.Chrome()         # global variable
url = "https://www.saucedemo.com/"   # global variable


class TestSmth:

    def test_url_status(self):
        driver = webdriver.Chrome()               # local variable - not seen from outside the method
        driver.get("https://www.apple.com")
        expected_url = "https://www.apple.com/"   # local variable - not seen from outside the method
        assert driver.current_url == expected_url

    def test_apple(self):

        driver_.get("https://www.apple.com")   # global variable used
        time.sleep(3)
        expected_title = "Apple"
        assert driver_.title == expected_title

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
