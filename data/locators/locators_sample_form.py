from selenium.webdriver.common.by import By


class LocatorsSampleForm:
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