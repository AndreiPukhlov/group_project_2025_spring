
from selenium import webdriver


def get_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver


login_page_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
home_page_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"


class TestLogin:

    def test(self):
        driver = get_driver()
        driver.get(login_page_url)
        assert driver.title == 'OrangeHRM'

    def test_username_required_field(self):
        driver = get_driver()
        # 1.Go to login page AUT - Application Under Test
        driver.get(login_page_url)
        # 2. Input valid password in a "password" field. (Password: admin123)
        driver.find_element("css selector", '[name="password"]').send_keys('admin123')
        # 3. click Login button
        driver.find_element("css selector", '[type="submit"]').click()
        # Expected result
        # Authorization denied A hint "username field" is required is appear on a screen
        assert driver.current_url == login_page_url
        # todo add description to step
        expected_message = driver.find_element("xpath", "//span[text()='Required']").text
        assert expected_message == 'Required'


    def test_invalid_username(self):
        driver = get_driver()
        #1.Navigate to https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
        driver.get(login_page_url)
        # 2.Enter an invalid username to the "Username" field
        driver.find_element("css selector", '[name="username"]').send_keys('Admi')
        # 3. Enter valid password to the "Password" field
        driver.find_element("css selector", '[name="password"]').send_keys('admin123')
       # 4. Click on the Login button
        driver.find_element("css selector", '[type="submit"]').click()
        # Expexted result
        # The user is not logged in and a pop-up window appears on the screen
        assert driver.current_url == login_page_url
        expected_message = driver.find_element("xpath", "//p[text()='Invalid credentials']").text
        assert expected_message == 'Invalid credentials'





