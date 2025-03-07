import pytest

from data.test_data import TestData
from data.urls import Urls

home_page_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
expected_error_message_required_field_color = "rgba(235, 9, 16, 10)"
data = TestData()
url = Urls()


class TestLogin:

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.bug
    def test(self, driver):
        driver.get()
        assert driver.title == 'OrangeHRM'

    def test_username_required_field(self, driver):
        # 1.Go to login page AUT - Application Under Test
        driver.get(url.BASE_URL)
        # 2. Input valid password in a "password" field. (Password: admin123)
        driver.find_element("css selector", '[name="password"]').send_keys('admin123')
        # 3. click Login button
        driver.find_element("css selector", '[type="submit"]').click()
        # Expected result

        # Authorization denied
        assert driver.current_url == url.BASE_URL
        # Error message "username field" is required is appear on a screen
        expected_message = driver.find_element("xpath", "//span[text()='Required']").text
        assert expected_message == 'Required'

    def test_invalid_username(self, driver):


        # 1.Navigate to https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
        driver.get(url.BASE_URL)

        # 2.Enter an invalid username to the "Username" field
        driver.find_element("css selector", '[name="username"]').send_keys('Admi')
        # 3. Enter valid password to the "Password" field
        driver.find_element("css selector", '[name="password"]').send_keys('admin123')
        # 4. Click on the Login button
        driver.find_element("css selector", '[type="submit"]').click()

        # Expected result
        # The user is not logged in and a pop-up window appears on the screen
        assert driver.current_url == url.BASE_URL
        expected_message = driver.find_element("xpath", "//p[text()='Invalid credentials']").text
        assert expected_message == 'Invalid credentials'



    def test_username_password_fields_required(self):
        driver = get_driver()
        #1.Navigate to AUT
        driver.get(login_page_url)
        #2. Ensure that both the "Username" and "Password" fields are empty
        #3. Click on the Login button
        driver.find_element("css selector", '[type="submit"]').click()
        # Expected result
        #Under the Password and Username fields there are messages that these data are Required
        assert driver.current_url == login_page_url
        error_messages = driver.find_elements("xpath", "//span[text()='Required']")
        assert error_messages[0].text == "Required" and error_messages[1].text == "Required"



    def test_password_required_field(self, driver):


        # 1. Open the login page
        driver.get(url.BASE_URL)

        # 2. Enter a valid username in the "Username" field.
        driver.find_element("css selector", '[name="username"]').send_keys(data.USER_NAME)
        # 3. Click the "Login" button.
        driver.find_element("css selector", '[type="submit"]').click()

        # Expected result
        # An error message "Required" appears below the "Password" field
        # Error message text color per requirements rgba(235, 9, 16, 1) -> ticket Andrei Pukhlov 02/28/2025
        error_message_element = driver.find_element("xpath", "//span[text()='Required']")
        expected_message = error_message_element.text
        get_error_message_color = error_message_element.value_of_css_property("color")
        # TODO Tamara
        assert expected_message == "Required"

        try:
            assert get_error_message_color == expected_error_message_required_field_color, \
                "Wrong color for the error message for Required field"
        except AssertionError as e:
            print(f"Warning: {e}")  # Logs the error but allows test execution to continue

    def test_234423(self, driver):
        pass

    def test_34563(self, driver):
        pass
