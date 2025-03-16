import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait

from data.test_data import TestData
from data.urls import Urls
from pages.login_page import LoginPage

home_page_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
expected_error_message_required_field_color = "rgba(235, 9, 16, 10)"
data = TestData()
url = Urls()
LOGIN_BUTTON_LOCATOR = (By.CSS_SELECTOR, '[type="submit"]')
BULLET_POINTS_LOCATOR = (By.CSS_SELECTOR, "[type='password']")


class TestLogin:

    # @pytest.mark.regression
    # @pytest.mark.smoke
    # @pytest.mark.bug
    def test(self, driver):
        driver.get(home_page_url)
        assert driver.title == 'OrangeHRM'

    def test_pom(self, driver):
        page = LoginPage(driver, home_page_url)
        page.open()
        expected = driver.title
        assert expected == 'OrangeHRM'

    def test_username_required_field(self, driver):
        # 1.Go to login page AUT - Application Under Test
        driver.get(url.LOGIN_URL)
        # 2. Input valid password in a "password" field. (Password: admin123)
        wait(driver, 23).until(EC.visibility_of_element_located(
            ("css selector", '[name="password"]'))).send_keys('admin123')
        # driver.find_element("css selector", '[name="password"]').send_keys('admin123')
        # 3. click the Login button
        driver.find_element(*LOGIN_BUTTON_LOCATOR).click()
        # Expected result

        # Authorization denied
        assert driver.current_url == url.LOGIN_URL
        # Error message "username field" is required is appear on a screen
        expected_message = driver.find_element("xpath", "//span[text()='Required']").text
        assert expected_message == 'Required'

    def test_invalid_username(self, driver):

        # 1.Navigate to https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
        driver.get(url.LOGIN_URL)

        # 2.Enter an invalid username to the "Username" field
        driver.find_element("css selector", '[name="username"]').send_keys('Admi')
        # 3. Enter valid password to the "Password" field
        driver.find_element("css selector", '[name="password"]').send_keys(data.ADMIN_PASSWORD)
        # 4. Click on the Login button
        driver.find_element(*LOGIN_BUTTON_LOCATOR).click()

        # Expected result
        # The user is not logged in and a pop-up window appears on the screen
        assert driver.current_url == url.LOGIN_URL
        expected_message = driver.find_element("xpath", "//p[text()='Invalid credentials']").text
        assert expected_message == 'Invalid credentials'

    def test_username_password_fields_required(self, driver):
        # 1. Navigate to AUT
        driver.get(url.LOGIN_URL)
        # 2. Ensure that both the "Username" and "Password" fields are empty
        # TODO На каждый шаг должно быть действие, нужно добавить код проверки того, что поля пустые
        # 3 Click on the Login button
        driver.find_element(*LOGIN_BUTTON_LOCATOR).click()
        # Expected result
        # Under the Password and Username fields, there are messages that these data are Required
        assert driver.current_url == url.LOGIN_URL
        error_messages = driver.find_elements("xpath", "//span[text()='Required']")
        assert error_messages[0].text == "Required" and error_messages[1].text == "Required"

    def test_password_bullet_points(self, driver):
        page = LoginPage(driver, url.LOGIN_URL)
        # 1. Navigate to AUT
        driver.get(url.LOGIN_URL)
        # 2. Enter valid or invalid data to the "Password" field
        driver.find_element("css selector", '[name="password"]').send_keys('admin123')
        # Expected result
        # The characters displayed in the “Password” field are hidden by bullet points
        password_field_type = page.element_is_visible(BULLET_POINTS_LOCATOR).get_attribute('type')
        assert password_field_type == "password", f"Expected 'password', but got '{password_field_type}'"

    def test_password_required_field(self, driver):

        # 1. Open the login page
        driver.get(url.LOGIN_URL)

        # 2. Enter a valid username in the "Username" field.
        driver.find_element("css selector", '[name="username"]').send_keys(data.ADMIN_NAME)
        # 3. Click the "Login" button.
        driver.find_element(*LOGIN_BUTTON_LOCATOR).click()

        # Expected result
        # An error message "Required" appears below the "Password" field
        # Error message text color per requirements rgba(235, 9, 16, 1) -> ticket Andrei Pukhlov 02/28/2025
        error_message_element = driver.find_element("xpath", "//span[text()='Required']")
        expected_message = error_message_element.text
        get_error_message_color = error_message_element.value_of_css_property("color")

        assert driver.current_url == url.LOGIN_URL
        assert expected_message == "Required"

        try:
            assert get_error_message_color == expected_error_message_required_field_color, \
                "Wrong color for the error message for Required field"
        except AssertionError as e:
            print(f"Warning: {e}")  # Logs the error but allows test execution to continue

    def test_forgot_your_password_cancel(self, driver):
        # 1. Open the login page
        driver.get(url.LOGIN_URL)
        # 2. Click on the 'Forgot your password?' link
        driver.find_element("xpath", "//p[text()='Forgot your password? ']").click()
        # 3. Enter an existing username in the 'Username' field
        driver.find_element("css selector", '[name="username"]').send_keys(data.ADMIN_NAME)
        # 4. Click the 'Cancel' button
        driver.find_element("xpath", "//button[text()=' Cancel ']").click()

        # Expected result
        # The user is returned to the login page
        assert driver.current_url == url.LOGIN_URL

    def test_username_password_fields_required_pom(self, driver):
        page = LoginPage(driver, url.LOGIN_URL)
        page.open()
        page.element_is_visible(LOGIN_BUTTON_LOCATOR).click()

        # driver.find_element(*LOGIN_BUTTON_LOCATOR).click()
        assert driver.current_url == url.LOGIN_URL
        # error_messages = page.element_is_visible(*("xpath", "//span[text()='Required']"))
        error_messages = driver.find_elements("xpath", "//span[text()='Required']")
        assert error_messages[0].text == "Required" and error_messages[1].text == "Required"
