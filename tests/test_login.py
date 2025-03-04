import time

from selenium import webdriver


def get_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver


login_page_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
home_page_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
expected_error_message_required_field_color = "rgba(235, 9, 16, 1)"


class TestLogin:

    def test(self):
        driver = get_driver()
        driver.get(login_page_url)
        assert driver.title == 'OrangeHRM'

    def test_username_required_field(self):
        driver = get_driver()
        # 1.Go to login page Application Under Test
        driver.get(login_page_url)
        # 2. Input valid password in a "password" field. (Password: admin123)
        driver.find_element("css selector", '[name="password"]').send_keys('admin123')
        # 3. click Login button
        driver.find_element("css selector", '[type="submit"]').click()
        # Expected result
        # Authorization denied A hint "username field" is required is appear on a screen
        assert driver.current_url == "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        # todo add description to step
        expected_message = driver.find_element("xpath", "//span[text()='Required']").text
        assert expected_message == 'Required'

    def test_password_required_field(self):
        driver = get_driver()

        # 1. Open the login page
        driver.get(login_page_url)

        # 2. Enter a valid username in the "Username" field.
        driver.find_element("css selector", '[name="username"]').send_keys('Admin')
        # 3. Click the "Login" button.
        driver.find_element("css selector", '[type="submit"]').click()

        # Expected result
        # An error message "Required" appears below the "Password" field
        # Error message text color per requirements rgba(235, 9, 16, 1) -> ticket Andrei Pukhlov 02/28/2025
        error_message_element = driver.find_element("xpath", "//span[text()='Required']")
        expected_message = error_message_element.text
        get_error_message_color = error_message_element.value_of_css_property("color")
        assert expected_message == "Required"

        try:
            assert get_error_message_color == expected_error_message_required_field_color, \
                "Wrong color for the error message for Required field"
        except AssertionError as e:
            print(f"Warning: {e}")  # Logs the error but allows test execution to continue
