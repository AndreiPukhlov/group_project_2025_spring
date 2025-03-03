from selenium import webdriver


def get_driver():
    driver = webdriver.Chrome()
    return driver


login_page_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


class TestLogin:

    def test(self):
        driver = get_driver()
        driver.get(login_page_url)
        assert driver.title == 'OrangeHRM'
