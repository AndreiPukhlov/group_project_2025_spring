from selenium.webdriver.common.by import By


class ForgotPasswordLocators:
    USERNAME_FIELD = (By.CSS_SELECTOR, "[name='username']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".orangehrm-forgot-password-title")
    LOC = None