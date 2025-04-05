import logging
from selenium.webdriver.common.by import By
from pathlib import Path
from data.generators.sample_form_generator import generate_sample_person_male, generate_sample_person_female, \
    random_country_generator, valid_password_five_chars, dob_generator_select, random_car_generator
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
SELECT_CAR_MAKER = (By.CSS_SELECTOR, '[name="carMake"]')
RELATED_DOCUMENTS = (By.XPATH, "//button[text()='Related documents (click)']")
DOCUMENTS_LIST = (By.XPATH, "//h4")
ATTACHMENT_NAME = (By.CSS_SELECTOR, '#attachment')

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
ASTERISK = '"*"'
IMAGE_FILE_NAME = "se.jpg"

logger = logging.getLogger(__name__)  # logger initialization for this file


class TestSampleForm:
    man = next(person)  # read info from person man inside the class
    year, month, day = dob_generator_select()  # assign result of dob_gen to variables
    car_maker_generator = random_car_generator()

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
        country = random_country_generator()
        page_sp.select_by_text(SELECT_COUNTRY, country)
        logger.info("Select country")

        car_maker = self.car_maker_generator
        page_sp.select_by_value(SELECT_CAR_MAKER, car_maker)
        logger.info('Car maker selected')

        page_sp.element_is_visible((By.XPATH, f"//input[@value='{self.man.gender}']")).click()
        logger.info("Enter user gender")
        page_sp.element_is_visible(ALLOW_TO_CONTACT_CHECK_BOX).click()
        logger.info("Allow to check")

        page_sp.element_is_visible(THIRD_PARTY_AGREEMENT_BUTTON).click()
        logger.info("Third party agreement clicked")

        page_sp.alert()
        alert_text = page_sp.get_alert_text()
        print(alert_text)
        logger.info('Switched to alert and got alert text')

        page_sp.alert_accept()
        logger.info("Alert accepted")

        page_sp.element_is_visible(CHOOSE_FILE_BUTTON).send_keys(str(image_path))
        logger.info("Image uploaded")

        uploaded_file_path = page_sp.get_element_attribute(ATTACHMENT_NAME, 10, 'value')
        actual_uploaded_file_name = uploaded_file_path.split("\\")[-1]
        # print(actual_uploaded_file_name)
        logger.info("Got uploaded image file name")

        page_sp.switch_to_iframe(ADDITIONAL_INFO_IFRAME)
        page_sp.element_is_visible(CONTACT_PERSON_NAME_IFRAME).send_keys(self.man.contact_person_name)
        page_sp.element_is_visible(CONTACT_PERSON_PHONE_IFRAME).send_keys(self.man.contact_person_phone_number)
        page_sp.switch_out_of_iframe()
        logger.info("Contact person information added")

        page_sp.element_is_visible(FORM_SUBMIT_BUTTON).click()
        logger.info("The form submitted")

        elements = page_sp.elements_are_present(RESULT_PAGE_TEXT)
        text_list = [i.text for i in elements]
        # print(text_list)
        logger.info("Got list of text from result data")

        full_result_page_data_with_titles = page_sp.element_is_visible(RESULT_PAGE_CONTAINER).text
        # print(full_result_page_data_with_titles)
        logger.info("Got full result from submitted form with titles")

        # option #1
        corrected_month = str(int(self.month) + 1)
        month = '0' + corrected_month if len(str(int(self.month) + 1)) < 2 else corrected_month
        day = self.day if len(str(self.day)) > 1 else int('0' + str(self.day))
        expected_dob_1 = f"{month}/{day}/{self.year}"

        # option #2 with zfill()
        corrected_month = str(int(self.month) + 1)
        expected_dob_2 = f"{corrected_month.zfill(2)}/{str(self.day).zfill(2)}/{self.year}"

        expected_dob_final = f"{int(self.month) + 1:02}/{self.day:02}/{self.year}"
        logger.info("User DOB reformatted")

        submitted_data = [
            self.man.first_name, self.man.last_name, expected_dob_final,
            self.man.gender, str(self.man.phone_number), self.man.address.replace("\n", " "), self.man.email,
            self.man.contact_person_name, self.man.contact_person_phone_number,
            self.car_maker_generator, country
        ]
        logger.info("List of data for assertion created")

        for i in submitted_data:
            assert i in text_list
        logger.info("Asserted actual submitted data equals to the data were sent ✅")

        asterisk_color = page_sp.get_element_color(USER_NAME_LABEL)
        asterisk_content = page_sp.get_element_after(USER_NAME_LABEL)
        logger.info('Got "*" css element content and color')

        assert asterisk_color == ASTERISK_COLOR
        logger.info('Asserted "*" css element color, result as expected ✅')

        assert asterisk_content == ASTERISK
        logger.info('Asserted "*" css element content, result as expected ✅')

        assert actual_uploaded_file_name == IMAGE_FILE_NAME
        logger.info('Asserted uploaded image file name, result as expected ✅')

    def test_windows(self, driver):
        page_sp = SampleFormPage(driver, url)
        page_sp.open()
        logger.info("Open sample form page")

        page_sp.element_is_visible(RELATED_DOCUMENTS).click()
        logger.info("Open new window(tab)")
        page_sp.element_is_visible(RELATED_DOCUMENTS).click()
        logger.info("Open new window(tab)")

        windows = page_sp.get_window_handles()
        logger.info("Got all opened windows list")

        page_sp.switch_to_window(windows[-1])
        page_sp.close_window()
        logger.info("Switched to last opened window and closed it")

        windows = page_sp.get_window_handles()
        logger.info("Got new list of all opened windows")

        page_sp.switch_to_window(windows[-1])
        logger.info("Switched to the last opened window")

        documents_list_label = page_sp.element_is_visible(DOCUMENTS_LIST).text
        assert documents_list_label == "Documents List:"
        logger.info("Label 'Documents List:' asserted, result as expected ✅")

        page_sp.close_window()
        logger.info("Switched to last window in the list and closed it")

        windows = page_sp.get_window_handles()
        logger.info("Got new list of all opened windows")
        page_sp.switch_to_window(windows[-1])
        page_sp.close_window()
        logger.info("Switched to the last opened window(original) and closed it")


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
