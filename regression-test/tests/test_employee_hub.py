
import allure
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.employee_hub import EmployeeHubPage


@allure.title("[C2578] Employee Hub - Account list displays correct accounts & info")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2578")
def test_account_list(set_up_tear_down):
    page = set_up_tear_down
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
    with allure.step("Validate that advocate info should be reflected correctly"):
        employee_page = EmployeeHubPage(page)
        employee_page.check_table_column_name_is_correct()
        acc_info = ['Test ADV 01', 'active', 'Accountant', 'Banking & Finance', 'test.adv01@themartec.com']
        employee_page.check_account_name_has_correct_info_field(acc_info)


@allure.title("[C2580][1] Employee Hub - Filter is worked as expected in case applying status")
@allure.description(f"Filter By Status As Active, Deleted, Invitation Sent, Bench")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2580")
def test_filter_01(set_up_tear_down):
    page = set_up_tear_down
    employee_page = EmployeeHubPage(page)
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
    with allure.step("[1] Validate Filter By Combined Status As 'Active' And 'Bench'"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list(['Active', 'Bench'])
        employee_page.click_on_apply_button()
        employee_page.check_filter_is_correct(['Active', 'Bench'])
    with allure.step("Clear All Filter"):
        employee_page.remove_filter()
    with allure.step("[2] Validate Filter By Combined Status As 'Delete' and 'Invitation Sent'"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list(['Deleted', 'Invitation Sent'])
        employee_page.click_on_apply_button()
        employee_page.check_filter_is_correct(['Deleted', 'Invitation Sent'])
    with allure.step("[5]Clear All Filter & Validate checked option are reset"):
        employee_page.click_on_filter_button()
        employee_page.click_on_clear_all_button()
        employee_page.check_options_are_reset('Active')
        employee_page.click_on_apply_button()


@allure.title("[C2580][2] Employee Hub - Filter is worked in case mixed options (status & star advocate)")
@allure.description(f"Mix between status & star advocate")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2580")
def test_filter_02(set_up_tear_down):
    page = set_up_tear_down
    employee_page = EmployeeHubPage(page)
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
    with allure.step("[3] Validate Filter By Status='Active' And ADVOCATE TYPE='Starred Advocate'"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list(['Active'])
        employee_page.set_filter_by_list(['Star Advocate'])
        employee_page.click_on_apply_button()
        employee_page.check_filter_is_correct(['Active'])
        employee_page.check_star_is_shown("Test ADV 02")
    with allure.step("Clear All Filter"):
        employee_page.remove_filter()
    with allure.step("[4] Validate Filter By Status='Invitation Pending' And Unchecked ADVOCATE TYPE"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list(['Invitation Pending'])
        employee_page.click_on_apply_button()
        employee_page.check_filter_result_as_empty()