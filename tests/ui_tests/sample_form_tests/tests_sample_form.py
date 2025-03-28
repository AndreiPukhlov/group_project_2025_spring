import pytest
from selenium.webdriver.common.by import By
from pathlib import Path
from data.generators.sample_form_generator import generate_sample_person_male, generate_sample_person_female, \
    random_country_generator, valid_password_five_chars
from pages.sample_form_page import SampleFormPage

person = generate_sample_person_male()
person2 = generate_sample_person_female()

url = "https://skryabin.com/webdriver/html/sample.html"

# locators for the sample form
NAME_FIELD = (By.CSS_SELECTOR, '#name')
FIRST_NAME_FIELD = (By.ID, 'firstName')
LAST_NAME_FIELD = (By.ID, 'lastName')
DOB_FIELD = (By.ID, 'dateOfBirth')
USER_NAME_FIELD = (By.CSS_SELECTOR, "[name='username']")
EMAIL_FIELD = (By.CSS_SELECTOR, "[name='email']")
PASSWORD_FIELD = (By.ID, "password")
CONFIRM_PASSWORD_FIELD = (By.ID, "confirmPassword")
PHONE_FIELD = (By.CSS_SELECTOR, '[name="phone"]')
ADDRESS_FIELD = (By.ID, 'address')
CHOOSE_FILE_BUTTON = (By.ID, 'attachment')
SAVE_BUTTON = (By.XPATH, "//*[text()='Save']")
FORM_SUBMIT_BUTTON = (By.ID, 'formSubmit')
PRIVACY_POLICY_CHECKBOX = (By.CSS_SELECTOR, '[name="agreedToPrivacyPolicy"]')
ALLOW_TO_CONTACT_CHECK_BOX = (By.CSS_SELECTOR, "[name='allowedToContact']")
SELECT_COUNTRY = (By.CSS_SELECTOR, '[name="countryOfOrigin"]')
THIRD_PARTY_AGREEMENT_BUTTON = (By.ID, 'thirdPartyButton')
ADDITIONAL_INFO_IFRAME = (By.CSS_SELECTOR, '[name="additionalInfo"]')
CONTACT_PERSON_NAME_IFRAME = (By.ID, 'contactPersonName')
CONTACT_PERSON_PHONE_IFRAME = (By.ID, 'contactPersonPhone')

# locators for the result page
RESULT_PAGE_TITLE = (By.CSS_SELECTOR, '.applicationResult')
RESULT_PAGE_FIRST_NAME_FIELD = (By.CSS_SELECTOR, '[name="firstName"]')
RESULT_PAGE_CONTAINER = (By.CSS_SELECTOR, '.container-fluid')
RESULT_PAGE_TEXT = (By.CSS_SELECTOR, '.large.ng-binding.ng-scope')

# data
SUBMITTED_FORM_TITLE = "Submitted sample form data"
USER_PASSWORD = valid_password_five_chars()
project_root = Path(__file__).parent.parent.parent.parent
image_path = project_root / "data" / "images" / "se.jpg"

# assertion data locators
ASSERT_THIRD_PARTY_AGREEMENT_TEXT = (By.ID, 'thirdPartyResponseMessage')
USER_NAME_LABEL = (By.XPATH, '//label[@for="username"]')
ASTERISK_COLOR = "rgba(51, 51, 51, 1)"
ASTERISK = "*"


class TestSampleForm:
    man = next(person)

    def test_minimum_required_fields(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()

        self.all_required_fields(page_sp)

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()

        actual_text = page_sp.element_is_visible(RESULT_PAGE_TITLE).text
        expected_text = SUBMITTED_FORM_TITLE
        actual_f_name = page_sp.element_is_visible(RESULT_PAGE_FIRST_NAME_FIELD).text

        assert actual_text == expected_text
        assert actual_f_name == self.man.first_name

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

    def test_name(self):
        project_root = Path(__file__).parent.parent.parent.parent
        print(f"Resolved image path: {project_root}")
        pass
        # fjgkdfghdkfgh
        # kdfglsdfgjdsl

    def all_required_fields(self, page_sp):
        page_sp.element_is_visible(NAME_FIELD).click()
        page_sp.element_is_visible(FIRST_NAME_FIELD).send_keys(self.man.first_name)
        page_sp.element_is_visible(LAST_NAME_FIELD).send_keys(self.man.last_name)
        page_sp.element_is_visible(SAVE_BUTTON).click()
        page_sp.element_is_visible(USER_NAME_FIELD).send_keys(self.man.first_name + self.man.last_name)
        page_sp.element_is_visible(EMAIL_FIELD).send_keys(self.man.email)
        page_sp.element_is_visible(PASSWORD_FIELD).send_keys(USER_PASSWORD)
        page_sp.element_is_visible(CONFIRM_PASSWORD_FIELD).send_keys(USER_PASSWORD)
        page_sp.element_is_visible(PRIVACY_POLICY_CHECKBOX).click()
