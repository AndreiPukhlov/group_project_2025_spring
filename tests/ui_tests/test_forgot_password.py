import pytest

from data.locators.forgot_password_locators import ForgotPasswordLocators
from data.locators.login_locators import LoginPageLocators
from data.test_data import TestData
from data.urls import Urls
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage

url = Urls()
fp_locators = ForgotPasswordLocators()
lp_locators = LoginPageLocators()
data = TestData()


class TestForgotPassword:

    @pytest.mark.regression
    def test_success_message(self, driver):
        # создаем представителя класса LoginPage
        page = LoginPage(driver, url.LOGIN_URL)
        page.open()
        page.element_is_visible(lp_locators.FORGOT_PASSWORD_LOCATOR).click()

        # создаем представителя класса ForgotPasswordPage
        page = ForgotPasswordPage(driver, "")
        page.element_is_visible(fp_locators.USERNAME_FIELD).send_keys(data.ADMIN_NAME)

        page.element_is_visible(fp_locators.SUBMIT_BUTTON).click()

        message = page.element_is_visible(fp_locators.SUCCESS_MESSAGE).text
        assert message == "Reset Password link sent successfully"

    @pytest.mark.skip(reason="This feature is not ready yet")

    def test_forgot_your_password_cancel(self, driver):
        # 1. Open the login page
        driver.get(url.LOGIN_URL)
        # 2. Click on the 'Forgot your password?' link
        driver.find_element("xpath", "//p[text()='Forgot your password? ']").click()
        # 3. Enter an existing username in the 'Username' field
        driver.find_element("css selector", '[name="username"]').send_keys(data.ADMIN_NAME)
        # 4. Click the 'Cancel' button
        driver.find_element("xpath", "//button[text()=' Cancel ']").click()

        # Expected result
        # The user is returned to the login page
        assert driver.current_url == url.LOGIN_URL
