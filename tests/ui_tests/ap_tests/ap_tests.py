from selenium.webdriver.common.by import By

from data.generators.sample_form_generator import dob_generator_select
from pages.sample_form_page import SampleFormPage

url = "https://skryabin.com/webdriver/html/sample.html"


class TestSamplePageAP:

    def test_populate_dob(self, driver):
        year, month, day = dob_generator_select()
        sf_page = SampleFormPage(driver, url)
        sf_page.open()
        sf_page.element_is_visible((By.ID, "dateOfBirth")).click()
        sf_page.select_by_value((By.CSS_SELECTOR, '[data-handler="selectYear"]'), year)
        sf_page.select_by_value((By.CSS_SELECTOR, '[data-handler="selectMonth"]'), month)
        sf_page.element_is_visible((By.XPATH, f'//a[text()="{day}"]')).click()


