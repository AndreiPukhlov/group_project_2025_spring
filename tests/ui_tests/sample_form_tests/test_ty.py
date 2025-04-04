import random
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from data.generators.sample_form_generator import generate_sample_person_male, generate_sample_person_female, \
    valid_password_five_chars
from pages.sample_form_page import SampleFormPage


person = generate_sample_person_male()
person2 = generate_sample_person_female()

URL = "https://skryabin.com/webdriver/html/sample.html"

#locators for form
NAME_FIELD = (By.CSS_SELECTOR, '#name')
FIRST_NAME_FIELD = (By.NAME, 'firstName')
LAST_NAME_FIELD = (By.NAME, 'lastName')
USERNAME_FIELD = (By.CSS_SELECTOR, "[name='username']")
EMAIL_FIELD = (By.CSS_SELECTOR, "[name='email']")
PASSWORD_FIELD = (By.ID, "password")
CONFIRM_PASSWORD_FIELD = (By.ID, "confirmPassword")
SUBMITTED_SAMPLE_FORM_DATA = (By.CSS_SELECTOR, '.applicationResult')
SUBMITTED_NAME = (By.CSS_SELECTOR, '[name="name"]')
REQUIRED_ERROR_MESSAGES = (By.XPATH, '//*[text()="This field is required."]')
CAR_MAKE_LOCATOR = (By.NAME, "carMake")

#locators for buttons and checkbox
SAVE_BUTTON = (By.XPATH, "//*[text()='Save']")
SUBMIT_BUTTON = (By.ID, 'formSubmit')
PRIVACY_POLICY_CHECKBOX = (By.NAME, "agreedToPrivacyPolicy")
CHECKBOX_ERROR_LOCATOR = (By.XPATH, '//label[contains(text(), "Must check")]')
CHOOSE_FILE_BUTTON_LOCATOR = (By.ID, 'attachment')

#data
SUBMITTED_FORM_TEXT = "Submitted sample form data"
EMPTY_FIELDS_ERROR_MESSAGE = "This field is required."
CHECKBOX_ERROR_MESSAGE = "- Must check!"
USER_PASSWORD_GENERATOR = valid_password_five_chars()

#generator
cars = ["Ford", "Toyota", "BMW", "Other"]

def random_cars_generator():
    return random.choice(cars)


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
        page_sp.element_is_visible(PASSWORD_FIELD).send_keys(USER_PASSWORD_GENERATOR)
        page_sp.element_is_visible(CONFIRM_PASSWORD_FIELD).send_keys(USER_PASSWORD_GENERATOR)
        page_sp.element_is_visible(PRIVACY_POLICY_CHECKBOX).click()
        page_sp.element_is_visible(SUBMIT_BUTTON).click()
        actual_text = page_sp.element_is_visible(SUBMITTED_SAMPLE_FORM_DATA).text
        actual_f_name = page_sp.element_is_visible(SUBMITTED_NAME).text

        assert actual_text == SUBMITTED_FORM_TEXT
        assert actual_f_name == self.man.first_name + ' ' + self.man.last_name

    def test_name(self):
        pass

    def test_form_validation(self, driver):
        page_sp = SampleFormPage(driver, URL)

        page_sp.open()
        page_sp.element_is_visible(SUBMIT_BUTTON).click()
        error_elements = page_sp.elements_are_visible(REQUIRED_ERROR_MESSAGES)
        error_texts = [element.text for element in error_elements]
        assert error_texts.count(EMPTY_FIELDS_ERROR_MESSAGE) == 4

    def test_privacy_policy_checkbox(self, driver):
        page_sp = SampleFormPage(driver, URL)

        page_sp.open()
        page_sp.element_is_visible(NAME_FIELD).click()
        page_sp.element_is_visible(FIRST_NAME_FIELD).send_keys(self.man.first_name)
        page_sp.element_is_visible(LAST_NAME_FIELD).send_keys(self.man.last_name)
        page_sp.element_is_visible(SAVE_BUTTON).click()
        page_sp.element_is_visible(USERNAME_FIELD).send_keys(self.man.first_name + self.man.last_name)
        page_sp.element_is_visible(EMAIL_FIELD).send_keys(self.man.email)
        page_sp.element_is_visible(PASSWORD_FIELD).send_keys(USER_PASSWORD_GENERATOR)
        page_sp.element_is_visible(CONFIRM_PASSWORD_FIELD).send_keys(USER_PASSWORD_GENERATOR)

        page_sp.element_is_visible(SUBMIT_BUTTON).click()
        actual_text = page_sp.element_is_visible(CHECKBOX_ERROR_LOCATOR).text
        assert actual_text == CHECKBOX_ERROR_MESSAGE

    def test_select_car_make(self, driver):
        page_sp = SampleFormPage(driver, URL)
        page_sp.open()

        car_select = Select(page_sp.element_is_visible(CAR_MAKE_LOCATOR))
        random_car = random_cars_generator()
        car_select.select_by_visible_text(random_car)
        selected_car = car_select.first_selected_option.text
        assert selected_car == random_car

    def test_upload_image(self, driver):
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        image_path = project_root / "data" / "images" / "se.jpg"
        print(f"\nProject root: {project_root}")
        print(f"\nImage path: {image_path}")

        page_sp = SampleFormPage(driver, URL)
        page_sp.open()

        file_input = page_sp.element_is_visible(CHOOSE_FILE_BUTTON_LOCATOR)
        file_input.send_keys(str(image_path))
        assert image_path.name in file_input.get_attribute("value")

