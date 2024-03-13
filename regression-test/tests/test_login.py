import allure
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.pages.login import LoginPage


@allure.title("[C2528] Non-SSO - Verify Login UI & Successful login with valid username and password")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2528")
def test_successful_login(set_up_tear_down_without_state):
    page = set_up_tear_down_without_state
    with allure.step("Check Login UI is correct"):
        login_page = LoginPage(page)
        login_page.check_ui_is_correct()
    with allure.step("Log in With Valid User Name & Password"):
        login_page.enter_username_password(os.getenv("USER_NAME_OF_NON_ISOLATED_ACC_02"),
                                           os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        login_page.check_login_is_successful()


@allure.title("[C2650] Non-SSO - Login UnSuccessfully with invalid username and password")
@allure.description(f"Invalid Username, Incorrect format of Username")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2650")
def test_unsuccessful_login(set_up_tear_down_without_state):
    page = set_up_tear_down_without_state
    login_page = LoginPage(page)
    with allure.step("Log in With InValid User Name & Password"):
        login_page.enter_username_password("invalid_user@ntt.com",
                                           os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        login_page.check_login_is_unsuccessful_as_wrong_username()
    with allure.step("Log in With InValid Format of User Name"):
        login_page.enter_username_password("invalid_user",
                                           os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        login_page.check_login_is_unsuccessful_as_wrong_format()

