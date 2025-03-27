import pytest
from selenium.webdriver.common.by import By

from data.generators.sample_form_generator import generate_sample_person_male, generate_sample_person_female
from pages.sample_form_page import SampleFormPage

person = generate_sample_person_male()
person2 = generate_sample_person_female()

url = "https://skryabin.com/webdriver/html/sample.html"

# 1 types of locators
# NAME_FIELD = (By.CSS_SELECTOR, '#name')
# FIRST_NAME = (By.ID, 'firstName')
# LAST_NAME = (By.ID, 'lastName')
# SAVE_BUTTON = (By.XPATH, "//*[text()='Save']")
# ADDRESS_FIELD = (By.ID, 'address')
USER_NAME = (By.CSS_SELECTOR, '[name="username"]')
EMAIL_FIELD = (By.CSS_SELECTOR, "[name='email']")
# PASSWORD_FIELD = (By.ID, "password")
# CONFIRM_PASSWORD_FIELD = (By.ID, "confirmPassword")
PHONE_NUMBER = (By.CSS_SELECTOR, '[name="phone"]')
CHECKBOX_POLICY = (By.CSS_SELECTOR, '[name="agreedToPrivacyPolicy"]')
# SUBMIT_BUTTON = (By.ID, 'formSubmit')
LOGIN_RESULT = (By.CSS_SELECTOR, '.applicationResult')


# 2 types of locators
NAME_FIELD = (By.CSS_SELECTOR, '[name="name"]')
FIRST_NAME = (By.CSS_SELECTOR, '[name="firstName"]')
LAST_NAME = (By.CSS_SELECTOR, '[name="lastName"]')
SAVE_BUTTON = (By.XPATH, "//span[contains(text(), 'Save')]")
ADDRESS_FIELD = (By.CSS_SELECTOR, '[name="address"]')
# USER_NAME = (By.CSS_SELECTOR, '[name="username"]')
# EMAIL_FIELD = (By.CSS_SELECTOR, '[name="email"]')
PASSWORD_FIELD = (By.CSS_SELECTOR, '[name="password"]')
CONFIRM_PASSWORD_FIELD = (By.CSS_SELECTOR, '[name="confirmPassword"]')
# PHONE_NUMBER = (By.CSS_SELECTOR, '[name="phone"]')
# CHECKBOX_POLICY = (By.CSS_SELECTOR, '[name="agreedToPrivacyPolicy"]')
SUBMIT_BUTTON = (By.CSS_SELECTOR, '[name="formSubmit"]')
# LOGIN_RESULT = (By.XPATH, "//legend[@class='applicationResult']")


class TestSampleForm:
    man = next(person)

    def test_minimum_required_fields(self, driver):
        page_sp = SampleFormPage(driver, url)

        page_sp.open()
        page_sp.element_is_visible(NAME_FIELD).click()
        page_sp.element_is_visible(FIRST_NAME).send_keys(self.man.first_name)
        page_sp.element_is_visible(LAST_NAME).send_keys(self.man.last_name)
        page_sp.element_is_visible(SAVE_BUTTON).click()
        page_sp.element_is_visible(USER_NAME).send_keys(self.man.first_name + self.man.last_name)
        page_sp.element_is_visible(EMAIL_FIELD).send_keys(self.man.email)
        page_sp.element_is_visible(PASSWORD_FIELD).send_keys('Pass123!')
        page_sp.element_is_visible(CONFIRM_PASSWORD_FIELD).send_keys('Pass123!')
        page_sp.element_is_visible(CHECKBOX_POLICY).click()
        page_sp.element_is_visible(SUBMIT_BUTTON).click()

        actual_text = page_sp.element_is_visible(LOGIN_RESULT).text
        expected_text = "Submitted sample form data"

        assert actual_text == expected_text



    def test_required_other_fields(self, driver):
        page_sp = SampleFormPage(driver, url)

        page_sp.open()
        page_sp.element_is_visible(NAME_FIELD).click()
        page_sp.element_is_visible(FIRST_NAME).send_keys(self.man.first_name)
        page_sp.element_is_visible(LAST_NAME).send_keys(self.man.last_name)
        page_sp.element_is_visible(SAVE_BUTTON).click()
        page_sp.element_is_visible(ADDRESS_FIELD).send_keys(self.man.address)
        page_sp.element_is_visible(USER_NAME).send_keys(self.man.first_name + self.man.last_name)
        page_sp.element_is_visible(EMAIL_FIELD).send_keys(self.man.email)
        page_sp.element_is_visible(PASSWORD_FIELD).send_keys('Pass123!')
        page_sp.element_is_visible(CONFIRM_PASSWORD_FIELD).send_keys('Pass123!')
        page_sp.element_is_visible(PHONE_NUMBER).send_keys(self.man.phone_number)
        page_sp.element_is_visible(CHECKBOX_POLICY).click()
        page_sp.element_is_visible(SUBMIT_BUTTON).click()

        actual_text = page_sp.element_is_visible(LOGIN_RESULT).text
        expected_text = "Submitted sample form data"
        actual_f_name = page_sp.element_is_visible(FIRST_NAME).text
        actual_l_name = page_sp.element_is_visible(LAST_NAME).text
        actual_u_name = page_sp.element_is_visible(USER_NAME).text
        actual_email = page_sp.element_is_visible(EMAIL_FIELD).text
        # actual_address = page_sp.element_is_visible(ADDRESS_FIELD).text
        # actual_phone = page_sp.element_is_visible(PHONE_NUMBER).text


        assert actual_text == expected_text
        assert actual_f_name == self.man.first_name
        assert actual_l_name == self.man.last_name
        assert actual_u_name == self.man.first_name + self.man.last_name
        assert actual_email == self.man.email
        # assert actual_address == self.man.address
        # assert actual_phone == self.man.phone_number



    def test_name(self):
        pass
        #  Check lists:
        #  Enter valid data in all required fields
        #  Select a country
        #  Enter a valid address
        #  Enter a valid phone number
        #  Select a gender
        #  Select Car Make
        #  Select a date of birth
        #  Check the "Agree to Terms" checkbox
        #  Click "Submit" and verify that "SUBMITTED SAMPLE FORM DATA" appears.
        #  Leave "First Name" field empty, attempt to submit, and verify the error message.
        #  Leave "Last Name" field empty, attempt to submit, and verify the error message.
        #  Leave the "Email" field empty, attempt to submit, and verify the error message.
        #  Leave the "Password" or "Confirm Password" field empty, attempt to submit, and verify the error message.
        #  Submit without checking the "Agree to Terms" checkbox and verify the error message.


