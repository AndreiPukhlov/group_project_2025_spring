import pytest

from data.admin_test_data import TestData
from data.locators.forgot_password_locators import ForgotPasswordLocators
from data.locators.login_locators import LoginPageLocators
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
        page_lp = LoginPage(driver, url.LOGIN_URL)
        page_lp.open()
        page_lp.element_is_visible(lp_locators.FORGOT_PASSWORD_LOCATOR).click()


        # создаем представителя класса ForgotPasswordPage
        page_fp = ForgotPasswordPage(driver, "")
        page_fp.element_is_visible(fp_locators.USERNAME_FIELD).send_keys(data.ADMIN_NAME)

        page_fp.element_is_visible(fp_locators.SUBMIT_BUTTON).click()

        message = page_fp.element_is_visible(fp_locators.SUCCESS_MESSAGE).text
        assert message == "Reset Password link sent successfully"

    @pytest.mark.regression
    def test_forgot_your_password_cancel(self, driver):
        # создаем представителя класса LoginPage
        page = LoginPage(driver, url.LOGIN_URL)
        page.open()
        page.element_is_visible(fp_locators.FORGOT_PASSWORT_LINK).click()
        # создаем представителя класса ForgotPasswordPage
        page = ForgotPasswordPage(driver, "")
        page.element_is_visible(fp_locators.USERNAME_FIELD).send_keys(data.ADMIN_NAME)
        page.element_is_visible(fp_locators.CANCEL_BUTTON).click()
        assert driver.current_url == url.LOGIN_URL
