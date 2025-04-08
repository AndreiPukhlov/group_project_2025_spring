import time

import pytest
from selenium.webdriver.common.by import By

from data.generators.sample_form_generator import generate_sample_person_male, generate_sample_person_female, \
    random_country_generator, dob_generator_select
from pages.sample_form_page import SampleFormPage
from tests.ui_tests.sample_form_tests.test_sample_form import image_path

person = generate_sample_person_male()
person2 = generate_sample_person_female()

url = "https://skryabin.com/webdriver/html/sample.html"

# locators for the sample form
NAME_FIELD = (By.CSS_SELECTOR, '[name="name"]')
FIRST_NAME = (By.CSS_SELECTOR, '[name="firstName"]')
LAST_NAME = (By.CSS_SELECTOR, '[name="lastName"]')
SAVE_BUTTON = (By.XPATH, "//span[contains(text(), 'Save')]")
ADDRESS_FIELD = (By.CSS_SELECTOR, '[name="address"]')
USER_NAME = (By.CSS_SELECTOR, '[name="username"]')
EMAIL_FIELD = (By.CSS_SELECTOR, "[name='email']")
PASSWORD_FIELD = (By.CSS_SELECTOR, '[name="password"]')
CONFIRM_PASSWORD_FIELD = (By.CSS_SELECTOR, '[name="confirmPassword"]')
PHONE_FIELD = (By.CSS_SELECTOR, '[name="phone"]')
CHECKBOX_POLICY = (By.CSS_SELECTOR, '[name="agreedToPrivacyPolicy"]')
FORM_SUBMIT_BUTTON = (By.CSS_SELECTOR, '[name="formSubmit"]')

DOB_FIELD = (By.ID, 'dateOfBirth')

SELECTED_GENDER_FEMALE = (
By.XPATH, "//input[@value = 'female' and @class = 'ng-valid ng-dirty ng-touched ng-valid-parse']")
SELECTED_GENDER_MALE = (By.XPATH, "//input[@value = 'male' and @class = 'ng-valid ng-dirty ng-touched ng-valid-parse']")

NAME_FIELD_SAVE = (By.ID, "name")
ALLOW_TO_CONTACT_CHECK_BOX = (By.CSS_SELECTOR, "[name='allowedToContact']")
SELECT_COUNTRY = (By.CSS_SELECTOR, '[name="countryOfOrigin"]')
THIRD_PARTY_AGREEMENT_BUTTON = (By.ID, 'thirdPartyButton')
ADDITIONAL_INFO_IFRAME = (By.CSS_SELECTOR, '[name="additionalInfo"]')
CONTACT_PERSON_NAME_IFRAME = (By.ID, 'contactPersonName')
CONTACT_PERSON_PHONE_IFRAME = (By.ID, 'contactPersonPhone')

SELECT_CAR = (By.CSS_SELECTOR, '[name="carMake"]')

CHOOSE_FILE_BUTTON = (By.ID, 'attachment')

# locators for the result page
LOGIN_RESULT = (By.XPATH, "//legend[@class='applicationResult']")
RESULT_PAGE_PHONE_NUMBER = (By.XPATH, "(//*[@name='phone'])[1]")

REQUIRED_ERROR_MESSAGES = (By.XPATH, '//*[text()="This field is required."]')

# data
USER_PASSWORD = 'Pass123!'
SUBMITTED_FORM_TITLE = "Submitted sample form data"
EMPTY_FIELDS_ERROR_MESSAGE = "This field is required."

# locators for the result page
RESULT_PAGE_TITLE = (By.CSS_SELECTOR, '.applicationResult')
RESULT_PAGE_FIRST_NAME_FIELD = (By.CSS_SELECTOR, '[name="firstName"]')
RESULT_PAGE_CONTAINER = (By.CSS_SELECTOR, '.container-fluid')
RESULT_PAGE_TEXT = (By.CSS_SELECTOR, '.large.ng-binding.ng-scope')

# assertion data locators
ASSERT_THIRD_PARTY_AGREEMENT_TEXT = (By.ID, 'thirdPartyResponseMessage')
USER_NAME_LABEL = (By.XPATH, '//label[@for="username"]')
ASTERISK_COLOR = "rgba(51, 51, 51, 1)"
ASTERISK = "*"

import random

cars = [
    "Ford",
    "Toyota",
    "BMW",
    "Other"
]


def random_car_generator():
    index = random.randint(0, len(cars) - 1)
    return cars[index]


class TestSampleForm:
    man = next(person)
    car_maker = random_car_generator()
    year, month, day = dob_generator_select()
    country = random_country_generator()

    def test_minimum_required_fields(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()

        actual_text = page_sp.element_is_visible(LOGIN_RESULT).text
        expected_text = SUBMITTED_FORM_TITLE

        assert actual_text == expected_text

    def test_required_other_fields(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.element_is_visible(ADDRESS_FIELD).send_keys(self.man.address)
        page_sp.element_is_visible(PHONE_FIELD).send_keys(self.man.phone_number)

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()

        actual_text = page_sp.element_is_visible(LOGIN_RESULT).text
        expected_text = SUBMITTED_FORM_TITLE
        actual_first_name = page_sp.element_is_visible(FIRST_NAME).text
        actual_last_name = page_sp.element_is_visible(LAST_NAME).text
        actual_user_name = page_sp.element_is_visible(USER_NAME).text
        actual_email = page_sp.element_is_visible(EMAIL_FIELD).text
        actual_address = page_sp.element_is_visible(ADDRESS_FIELD).text
        cleaned_address = actual_address.replace("\n", " ")
        actual_phone = int(page_sp.element_is_visible(RESULT_PAGE_PHONE_NUMBER).text)

        assert actual_text == expected_text
        assert actual_first_name == self.man.first_name
        assert actual_last_name == self.man.last_name
        assert actual_user_name == self.man.first_name + self.man.last_name
        assert actual_email == self.man.email
        assert cleaned_address == self.man.address.replace("\n", " ")
        assert actual_phone == self.man.phone_number

    def test_all_fields(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.element_is_visible(PHONE_FIELD).send_keys(self.man.phone_number)
        page_sp.element_is_visible(DOB_FIELD).send_keys('2/23/2000')  # TODO DOB generator
        page_sp.element_is_visible(ADDRESS_FIELD).send_keys(self.man.address)
        # TODO car maker select

        page_sp.element_is_visible((By.XPATH, f"//input[@value='{self.man.gender}']")).click()
        page_sp.element_is_visible(ALLOW_TO_CONTACT_CHECK_BOX).click()
        page_sp.select_by_text(SELECT_COUNTRY, random_country_generator())
        page_sp.element_is_visible(THIRD_PARTY_AGREEMENT_BUTTON).click()

        alert_text = page_sp.get_alert_text()
        print(alert_text)
        page_sp.alert_accept()
        page_sp.element_is_visible(CHOOSE_FILE_BUTTON).send_keys(str(image_path))

        iframe_element = page_sp.element_is_visible(ADDITIONAL_INFO_IFRAME)
        page_sp.switch_to_iframe(iframe_element)
        page_sp.element_is_visible(CONTACT_PERSON_NAME_IFRAME).send_keys(self.man.contact_person_name)
        page_sp.element_is_visible(CONTACT_PERSON_NAME_IFRAME).send_keys(self.man.contact_person_phone_number)
        page_sp.switch_out_of_iframe()

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()
        elements = page_sp.elements_are_present(RESULT_PAGE_TEXT)
        text_list = [i.text for i in elements]
        alert_text = page_sp.element_is_visible(RESULT_PAGE_CONTAINER).text
        print(text_list)
        print(type(alert_text))
        print(alert_text)
        # TODO assertions
        asterisk_color = page_sp.get_element_color(USER_NAME_LABEL)
        asterisk_content = page_sp.get_element_after(USER_NAME_LABEL)
        print(asterisk_color)
        print(asterisk_content)

        # option #1
        corrected_month = str(int(self.month) + 1)
        month = '0' + corrected_month if len(str(int(self.month) + 1)) < 2 else corrected_month
        day = self.day if len(str(self.day)) > 1 else int('0' + str(self.day))
        expected_dob_1 = f"{month}/{day}/{self.year}"

        # option #2 with zfill()
        corrected_month = str(int(self.month) + 1)
        expected_dob_2 = f"{corrected_month.zfill(2)}/{str(self.day).zfill(2)}/{self.year}"

        expected_dob_final = f"{int(self.month) + 1:02}/{self.day:02}/{self.year}"

    def all_required_fields(self, page_sp):
        page_sp.element_is_visible(NAME_FIELD).click()
        page_sp.element_is_visible(FIRST_NAME).send_keys(self.man.first_name)
        page_sp.element_is_visible(LAST_NAME).send_keys(self.man.last_name)
        page_sp.element_is_visible(SAVE_BUTTON).click()
        page_sp.element_is_visible(USER_NAME).send_keys(self.man.first_name + self.man.last_name)
        page_sp.element_is_visible(EMAIL_FIELD).send_keys(self.man.email)
        page_sp.element_is_visible(PASSWORD_FIELD).send_keys(USER_PASSWORD)
        page_sp.element_is_visible(CONFIRM_PASSWORD_FIELD).send_keys(USER_PASSWORD)
        page_sp.element_is_visible(CHECKBOX_POLICY).click()

    def test_car_make(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.select_by_value(SELECT_CAR, self.car_maker)
        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()

        actual_car = page_sp.element_is_visible(SELECT_CAR).text
        expected_car = self.car_maker

        assert actual_car == expected_car

    def test_valid_name_field(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        page_sp.element_is_visible(NAME_FIELD).click()
        page_sp.element_is_visible(FIRST_NAME).send_keys(self.man.first_name)
        page_sp.element_is_visible(LAST_NAME).send_keys(self.man.last_name)
        page_sp.element_is_visible(SAVE_BUTTON).click()

        actual_name = page_sp.get_element_attribute(NAME_FIELD_SAVE, 10, "value")
        expected_name = self.man.first_name + " " + self.man.last_name
        assert actual_name == expected_name

    def test_empty_required_fields(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()
        error_elements = page_sp.elements_are_visible(REQUIRED_ERROR_MESSAGES)
        error_texts = [element.text for element in error_elements]
        assert error_texts.count(EMPTY_FIELDS_ERROR_MESSAGE) == 4

    def test_gender_radio_buttons(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.element_is_visible((By.XPATH, "//input[@name='gender' and @value='female']")).click()

        # actual_gender = page_sp.element_is_visible(SELECTED_GENDER_FEMALE).is_selected()
        # assert page_sp.element_is_visible(SELECTED_GENDER_FEMALE)

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()

        actual_gender = page_sp.element_is_visible((By.XPATH, '//b[@name="gender"]')).text
        assert actual_gender == "female"

    def test_country_of_origin_dropdown(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.select_by_text(SELECT_COUNTRY, self.country)
        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()

        actual_country = page_sp.element_is_visible(SELECT_COUNTRY).text
        assert actual_country == self.country

    def test_date_of_birth_input(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.element_is_visible(DOB_FIELD).send_keys('02/23/2000')
        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()

        actual_DOB = page_sp.element_is_visible((By.XPATH, '//b[@name="dateOfBirth"]')).text
        assert actual_DOB == '02/23/2000'
        print(actual_DOB)

    def test_date_of_birth_generator(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.element_is_visible(DOB_FIELD).click()
        page_sp.select_by_text((By.CSS_SELECTOR, '[data-handler="selectYear"]'), self.year)
        page_sp.select_by_value((By.CSS_SELECTOR, '[data-handler="selectMonth"]'), self.month)
        page_sp.element_is_visible((By.XPATH, f"//a[text()='{self.day}']")).click()

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()

        actual_dob = page_sp.element_is_visible((By.XPATH, '//input[@name="dateOfBirth"]')).get_attribute("value")
        expected_dob = f"{int(self.month) + 1:02}/{self.day:02}/{self.year}"
        assert actual_dob == expected_dob

    # # Verify Reset form functionality
    # # Precondition - some of the fields are filled in
    # def test_reset_button(self, driver):
    #     page_sp = SampleFormPage(driver, url)
    #     page_sp.open()
    #     # Click Reset button
    #     # Expected result - All fields should be cleared in default state
    #     pass
    #
    # # Verify Reset form functionality
    # # Precondition - some of the fields are filled in
    # def test_refresh_button(self, driver):
    #     page_sp = SampleFormPage(driver, url)
    #     page_sp.open()
    #     # Click Refresh button
    #     # Expected result - All fields should be reloaded to reflect updates
    #     pass
    #
    # # verify first_name_field  with invalid data
    # def test_name_field_invalid_first_name(self, driver):
    #     page_sp = SampleFormPage(driver, url)
    #     page_sp.open()
    #     # Input first_name more than maxlength > 100 characters
    #     # Expected result: message - Please enter no more than 100 characters.
    #     pass
    #
    # # verify last_name_field with invalid data
    # def test_name_field_invalid_last_name(self, driver):
    #     page_sp = SampleFormPage(driver, url)
    #     page_sp.open()
    #     # Input last_name more than maxlength > 100 characters
    #     # Expected result: message - Please enter no more than 100 characters.
    #     pass
    #
    # # Verify username_field with more than 40 characters
    # def test_invalid_username_field(self, driver):
    #     page_sp = SampleFormPage(driver, url)
    #     page_sp.open()
    #     # Input name more than maxlength > 40 characters
    #     # Expected result: cannot possible to input more than 40.
    #     pass
    #
    # # Verify password_field more than 40 characters
    # def test_invalid_password(self, driver):
    #     page_sp = SampleFormPage(driver, url)
    #     page_sp.open()
    #     # Input name more than maxlength > 40 characters
    #     # Expected result: cannot possible to input more than 40.
    #     pass

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
