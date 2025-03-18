from selenium.webdriver.common.by import By


class LoginPageLocators:
    FORGOT_PASSWORD_LOCATOR = (By.XPATH, "//p[text()='Forgot your password? ']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, '[name="password"]')
    REQUIRED_ERROR_MESSAGE_LOCATOR = (By.XPATH, "//span[text()='Required']")
    LOGIN_BUTTON_LOCATOR = (By.CSS_SELECTOR, '[type="submit"]')
    BULLET_POINTS_LOCATOR = (By.CSS_SELECTOR, "[type='password']")
