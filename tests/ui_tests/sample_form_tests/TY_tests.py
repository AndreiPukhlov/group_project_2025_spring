import pytest
from selenium.webdriver.common.by import By

from data.generators.sample_form_generator import generate_sample_person_male, generate_sample_person_female
from pages.sample_form_page import SampleFormPage


person = generate_sample_person_male()
person2 = generate_sample_person_female()


URL = "https://skryabin.com/webdriver/html/sample.html"
NAME_FIELD = (By.CSS_SELECTOR, '#name')
FIRST_NAME_FIELD = (By.NAME, 'firstName')
LAST_NAME_FIELD = (By.NAME, 'lastName')
SAVE_BUTTON = (By.XPATH, "//*[text()='Save']")
USERNAME_FIELD = (By.CSS_SELECTOR, "[name='username']")
EMAIL_FIELD = (By.CSS_SELECTOR, "[name='email']")
PASSWORD_FIELD = (By.ID, "password")
CONFIRM_PASSWORD_FIELD = (By.ID, "confirmPassword")
CHECKBOX_PRIVACY_POLICY = (By.CSS_SELECTOR, '[name="agreedToPrivacyPolicy"]')
SUBMIT_BUTTON = (By.ID, 'formSubmit')
SUBMITTED_SAMPLE_FORM_DATA = (By.CSS_SELECTOR, '.applicationResult')
SUBMITTED_NAME = (By.CSS_SELECTOR, '[name="name"]')

REQUIRED_NAME_ERROR = (By.ID,"name-error")
REQUIRED_FIRST_NAME_ERROR = (By.ID, "username-error")
REQUIRED_LAST_NAME_ERROR = (By.ID, "password-error")
REQUIRED_EMAIL_ERROR = (By.ID, "email-error")


class TestSampleForm:
    man = next(person)


    def test_minimum_required_fields(self, driver):
        page_sp = SampleFormPage(driver, URL)

        page_sp.open()
        page_sp.element_is_visible(NAME_FIELD).click()
        page_sp.element_is_visible(FIRST_NAME_FIELD).send_keys(self.man.first_name)
        page_sp.element_is_visible(LAST_NAME_FIELD).send_keys(self.man.last_name)
        page_sp.element_is_visible(SAVE_BUTTON).click()
        page_sp.element_is_visible(USERNAME_FIELD).send_keys(self.man.first_name + self.man.last_name)
        page_sp.element_is_visible(EMAIL_FIELD).send_keys(self.man.email)
        page_sp.element_is_visible(PASSWORD_FIELD).send_keys('Pass123!')
        page_sp.element_is_visible(CONFIRM_PASSWORD_FIELD).send_keys('Pass123!')
        page_sp.element_is_visible(CHECKBOX_PRIVACY_POLICY).click()
        page_sp.element_is_visible(SUBMIT_BUTTON).click()
        actual_text = page_sp.element_is_visible(SUBMITTED_SAMPLE_FORM_DATA).text
        expected_text = "Submitted sample form data"
        actual_f_name = page_sp.element_is_visible(SUBMITTED_NAME).text


        assert actual_text == expected_text
        assert actual_f_name == self.man.first_name + ' ' + self.man.last_name

    def test_name(self):
        pass

    def test_form_validation(self, driver):
        page_sp = SampleFormPage(driver, URL)

        page_sp.open()
        page_sp.element_is_visible(SUBMIT_BUTTON).click()
        name_error = page_sp.element_is_visible(REQUIRED_NAME_ERROR).text
        first_name_error = page_sp.element_is_visible(REQUIRED_FIRST_NAME_ERROR).text
        last_name_error = page_sp.element_is_visible(REQUIRED_LAST_NAME_ERROR).text
        email_error = page_sp.element_is_visible(REQUIRED_EMAIL_ERROR).text

        assert name_error == "This field is required.", "The error did not appear for Name"
        assert first_name_error == "This field is required.", "The error did not appear for First Name"
        assert last_name_error == "This field is required.", "The error did not appear for Last Name"
        assert email_error == "This field is required.", "The error did not appear for Email"

