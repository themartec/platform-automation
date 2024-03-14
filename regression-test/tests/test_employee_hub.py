import random
import time

import allure
import os
import sys

import pytest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.employee_hub import EmployeeHubPage
from common_src.pages.settings import SettingsPage


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


@allure.title("[C2581] Direct Invite - Email templates are synced from Settings")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2581")
def test_add_new_advocate_template(set_up_tear_down):
    page = set_up_tear_down
    with allure.step("Access Settings"):
        main_page = MainEmployerPage(page)
        main_page.access_settings()
        setting_page = SettingsPage(page)
    with allure.step("Add New Invite Advocate Template & Set It As Default"):
        setting_page.click_on_option("Message Templates")
        setting_page.click_on_option("Invite Advocates")
        setting_page.click_on_option("Add email template")
        with allure.step("Validate Default Keywords In Template"):
            setting_page.check_default_keywords()
            number_part = random.randint(100, 999)
            adv_template_name = f"Automation Advocate Template {number_part}"
        with allure.step(f"Naming for template As '{adv_template_name}' & Write the template body"):
            setting_page.enter_template_name(adv_template_name)
            body = "Hi [advocateName], I’m excited to invite you to be a brand advocate for [companyName]"
            setting_page.fill_in_template_body(body)
        with allure.step("Click to ADD button to save template"):
            setting_page.click_on_add_button()
        with allure.step("Validate Template Name Is Shown On Invite Advocate"):
            setting_page.check_template_shown_on_invite_advocate(adv_template_name)
        with allure.step("Set New Template As Default"):
            setting_page.set_template_as_default(adv_template_name)
        with allure.step(f"Validate Flag Is Marked for '{adv_template_name}'"):
            setting_page.check_default_is_marked(adv_template_name)
    with allure.step("Access Employee Hub And Check Affected Advocate Template In Direct Invite"):
        with allure.step("Access Employee Hub"):
            main_page.access_employee_hub()
        with allure.step("Access ACTIVE PEOPLE > Direct Invite"):
            employee_page = EmployeeHubPage(page)
            employee_page.click_on_active_people_button()
            employee_page.click_on_direct_invite_option()
        with allure.step(f"Validate Default Template '{adv_template_name}' Is Selected"):
            employee_page.check_new_template_is_shown_in_direct_invite(adv_template_name)
        with allure.step("Validate template body content matching to Settings configure"):
            employee_page.check_body_email_template(body)
    with allure.step("Validate A New Template Can Be Created From Direct Invite View"):
        with allure.step("Update Current Template & Check Its Affection To Current View"):
            employee_page.update_template_with_content(body, "This is new update from Automation - " + body)
            employee_page.click_on_save_template_button()
            new_template_name = adv_template_name + " [New]"
            employee_page.enter_new_template_name(new_template_name)
            employee_page.check_new_template_is_shown_in_direct_invite(new_template_name)
        with allure.step("Validate Newly Update Template In Settings"):
            main_page.access_settings()
            setting_page.click_on_option("Message Templates")
            setting_page.check_template_shown_on_invite_advocate(new_template_name)
    with allure.step("Validate Delete An Invite Advocate Template In Settings"):
        setting_page.set_template_as_default("Invite Advocates - Specific Campaign")
        setting_page.delete_invite_adv(new_template_name)
        setting_page.delete_invite_adv(adv_template_name)


@pytest.mark.skip(reason="Feature is being updated")
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


@pytest.mark.skip(reason="Feature is being updated")
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

# @allure.title("")
# @allure.description(f"")
# @allure.testcase(f"{os.getenv('TESTRAIL_URL')}")
# def test_delete_adv(set_up_tear_down):
#     page = set_up_tear_down
#     with allure.step("Access Employee Hub"):
#         MainEmployerPage(page).access_employee_hub()
#         employee_page = EmployeeHubPage(page)
#     with allure.step("Search For Newly Register Advocate"):
#         adv_fullname = "Test Dummy"
#         employee_page.search_by_name(adv_fullname)
#     with allure.step("Hover on three dot button & Delete"):
#         employee_page.hover_on_three_dot_button_and_delete()
