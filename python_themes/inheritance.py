from selenium.webdriver.common.by import By

# pytest.fixture
def driver():
    # driver = webDriver.Chrome()
    yield driver
    driver.quit()
    pass

class BaseClass:
    def __init__(self, driver, url, timeout=23):
        self.driver = driver
        self.url = url
        self.timeout = timeout

    def find_element_with_condition(self):
        print("element_is_visible")

    def open(self):
        print("url_is_opened")

    def select_element(self):
        print("element_is_selected")


class LocatorsClass:
    BUTTON_LOCATOR = (By.XPATH, "//div[@class='some-class']")
    LOGIN_LOCATOR = (By.XPATH, "//div[@class='some-class']")
    PASSWORD_LOCATOR = (By.XPATH, "//div[@class='some-class']")


class Urls:
    HOME_PAGE_URL = "https://www.homepage.com"
    PROFILE_PAGE_URL = "https://www.homepage.com"
    PRODUCT_PAGE_URL = "https://www.homepage.com"


class LoginP(BaseClass):

    def get_smth(self):
        self.find_element_with_condition()
        element = self.select_element()
        return element


class HeaderMenu(BaseClass):
    def open_header(self):
        self.find_element_with_condition()


class FooterMenu(BaseClass):
    def open_footer(self):
        self.find_element_with_condition()

class HomeP(HeaderMenu, FooterMenu):
    def get_more(self):
        self.find_element_with_condition()
        self.find_element_with_condition()
        element = self.select_element()
        self.open_header()
        self.open_footer()
        self.find_element_with_condition()
        return element



class TestsLogin():
    url = Urls()
    locator = LocatorsClass()
    def test_1(self, driver):
        page = LoginP(driver, self.url, 12)
        page.open()
        page.find_element_with_condition(self.locator.LOGIN_LOCATOR)
        page.get_smth()


class TestsHome():
    url = Urls()
    locator = LocatorsClass()

    def test_1(self, driver):
        page = HomeP(driver, self.url)
        page.open()
        page.open_header()
        page.open_footer()
        page.get_more()