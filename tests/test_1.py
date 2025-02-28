import time
from selenium import webdriver


def get_driver():
    driver = webdriver.Chrome()
    return driver


url = "https://www.saucedemo.com/"


class TestSmth:

    def test_apple(self):
        driver = get_driver()
        driver.get("https://www.apple.com")
        time.sleep(3)
        assert driver.title == "Apple"

    def test_login(self):
        driver = get_driver()
        # open AUT
        driver.get(url)
        # enter user_name
        driver.find_element("", "")
        driver.find_element("css selector", "#user-name").send_keys("standard_user")
        # enter_password
        driver.find_element("css selector", "#password").send_keys("secret_sauce")
        # click button Login
        driver.find_element("css selector", "#login-button").click()
        # click navigation drawer
        driver.find_element("css selector", "#react-burger-menu-btn").click()
        # Logout button presented
        time.sleep(1)
        expected_result = driver.find_element("css selector", "#logout_sidebar_link").is_displayed()
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert expected_result == True
        assert driver.current_url == expected_url
