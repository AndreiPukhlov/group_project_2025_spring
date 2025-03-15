from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.webkitgtk.webdriver import WebDriver


class BasePage(object):

    def __init__(self, driver: WebDriver, url: str, timeout: int = 23):  # lesson 7
        self.driver = driver
        self.url = url
        self.timeout = timeout

    def open(self):
        self.driver.get(self.url)

    def element_is_visible(self, locator, timeout=None):
        return wait(self.driver, timeout or self.timeout).until(EC.visibility_of_element_located(locator))
