import pytest
from selenium.webdriver.common.by import By

from data.generators.sample_form_generator import generate_sample_person_male, generate_sample_person_female
from pages.sample_form_page import SampleFormPage

person = generate_sample_person_male()
person2 = generate_sample_person_female()

url = "https://skryabin.com/webdriver/html/sample.html"
NAME_FIELD = (By.CSS_SELECTOR, '#name')


class TestSampleForm:
    man = next(person)

    def test_minimum_required_fields(self, driver):
        page_sp = SampleFormPage(driver, url)

        page_sp.open()
        page_sp.element_is_visible(NAME_FIELD).click()
        page_sp.element_is_visible((By.ID, 'firstName')).send_keys(self.man.first_name)
        page_sp.element_is_visible((By.ID, 'lastName')).send_keys(self.man.last_name)
        page_sp.element_is_visible((By.XPATH, "//*[text()='Save']")).click()
        page_sp.element_is_visible((By.CSS_SELECTOR, "[name='username']")).send_keys(
            self.man.first_name + self.man.last_name)
        page_sp.element_is_visible((By.CSS_SELECTOR, "[name='email']")).send_keys(self.man.email)
        page_sp.element_is_visible((By.ID, "password")).send_keys('Pass123!')
        page_sp.element_is_visible((By.ID, "confirmPassword")).send_keys('Pass123!')
        page_sp.element_is_visible((By.CSS_SELECTOR, '[name="agreedToPrivacyPolicy"]')).click()
        page_sp.element_is_visible((By.ID, 'formSubmit')).click()

        actual_text = page_sp.element_is_visible((By.CSS_SELECTOR, '.applicationResult')).text
        expected_text = "Submitted sample form data"
        actual_f_name = page_sp.element_is_visible((By.CSS_SELECTOR, '[name="firstName"]')).text

        assert actual_text == expected_text
        assert actual_f_name == self.man.first_name

    def test_name(self):
        pass
        # fjgkdfghdkfgh
        # kdfglsdfgjdsl


