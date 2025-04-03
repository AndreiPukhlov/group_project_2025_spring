import logging
from selenium.webdriver.common.by import By
from pathlib import Path
from data.generators.sample_form_generator import generate_sample_person_male, generate_sample_person_female, \
    random_country_generator, valid_password_five_chars, dob_generator_select
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

logger = logging.getLogger(__name__)  # logger initialization for this file


class TestSampleForm:
    man = next(person)  # read info from person man inside the class
    year, month, day = dob_generator_select()  # assign result of dob_gen to variables

    def test_minimum_required_fields(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()
        logger.info("Open sample form page")

        self.all_required_fields(page_sp)
        logger.info("Populate all the required fields")

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()
        logger.info("Click 'Submit' button")

        actual_text = page_sp.element_is_visible(RESULT_PAGE_TITLE).text
        logger.info("Get all data from the submitted form")
        expected_text = SUBMITTED_FORM_TITLE
        actual_first_name = page_sp.element_is_visible(RESULT_PAGE_FIRST_NAME_FIELD).text
        logger.info("Get first_name from the submitted form")

        assert actual_text == expected_text
        logger.info("Result page data and expected data are equal as expected, test passed ✅")
        assert actual_first_name == self.man.first_name
        logger.info("Result page actual first_name and expected first_name are equal as expected, test passed ✅")

    def test_all_fields(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()
        logger.info("Open sample form page")
        self.all_required_fields(page_sp)

        page_sp.element_is_visible(PHONE_FIELD).send_keys(self.man.phone_number)
        logger.info("Enter user phone number")

        page_sp.element_is_visible(DOB_FIELD).click()
        page_sp.select_by_text((By.CSS_SELECTOR, '[data-handler="selectYear"]'), self.year)
        page_sp.select_by_value((By.CSS_SELECTOR, '[data-handler="selectMonth"]'), self.month)
        page_sp.element_is_visible((By.XPATH, f"//a[text()='{self.day}']")).click()
        logger.info("Enter user DOB")

        page_sp.element_is_visible(ADDRESS_FIELD).send_keys(self.man.address)
        logger.info("Enter user address")
        page_sp.select_by_text(SELECT_COUNTRY, random_country_generator())
        logger.info("Select country")
        # TODO car maker select

        page_sp.element_is_visible((By.XPATH, f"//input[@value='{self.man.gender}']")).click()
        logger.info("Enter user gender")
        page_sp.element_is_visible(ALLOW_TO_CONTACT_CHECK_BOX).click()
        logger.info("Allow to check")

        page_sp.element_is_visible(THIRD_PARTY_AGREEMENT_BUTTON).click()
        logger.info("Third party agreement")

        alert_text = page_sp.get_alert_text()
        print(alert_text)
        page_sp.alert_accept()
        # page_sp.select_by_text(SELECT_COUNTRY, random_country_generator())
        logger.info("Accept alert")

        page_sp.element_is_visible(CHOOSE_FILE_BUTTON).send_keys(str(image_path))
        logger.info("Upload image")

        page_sp.switch_to_iframe(ADDITIONAL_INFO_IFRAME)
        page_sp.element_is_visible(CONTACT_PERSON_NAME_IFRAME).send_keys(self.man.contact_person_name)
        page_sp.element_is_visible(CONTACT_PERSON_PHONE_IFRAME).send_keys(self.man.contact_person_phone_number)
        page_sp.switch_out_of_iframe()
        logger.info("Contact person information added")

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()
        logger.info("The form submitted")

        elements = page_sp.elements_are_present(RESULT_PAGE_TEXT)
        text_list = [i.text for i in elements]
        alert_text = page_sp.element_is_visible(RESULT_PAGE_CONTAINER).text
        print(text_list)
        print(type(alert_text))
        print(alert_text)

        # option #1
        corrected_month = str(int(self.month) + 1)
        month = '0' + corrected_month if len(str(int(self.month) + 1)) < 2 else corrected_month
        day = self.day if len(str(self.day)) > 1 else int('0' + str(self.day))
        expected_dob_1 = f"{month}/{day}/{self.year}"

        # option #2 with zfill()
        corrected_month = str(int(self.month) + 1)
        expected_dob_2 = f"{corrected_month.zfill(2)}/{str(self.day).zfill(2)}/{self.year}"

        expected_dob_final = f"{int(self.month) + 1:02}/{self.day:02}/{self.year}"

        # TODO assertions
        print(expected_dob_final)
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
