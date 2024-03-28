import time
from datetime import date, timedelta

import allure
import os

import pytest

from common_src.actions.common_action import click_on_button_name, refresh_page
from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.employee_hub import EmployeeHubPage
from common_src.pages.settings import SettingsPage
from common_src.pages.login import LoginPage
from common_src.pages.regsiter import RegisterPage
from common_src.database.database import MartecDatabase
from common_src.utils.dummy_data import get_dummy_string_for_email_address, get_random_string
from tests.test_nanl_upload_video import cwd
from utils.init_env import init_url


@allure.title("[C2589] Non-SSO - Direct invite Admin is worked as expected")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2589")
@allure.tag("profile_02", "network_listener", "user_invitation")
def test_admin_direct_invite(init_page_with_full_configure_profile_02, init_context):
    page = init_page_with_full_configure_profile_02
    with allure.step("Access Team in Settings"):
        main_page = MainEmployerPage(page)
        main_page.access_settings()
        setting_page = SettingsPage(page)
        setting_page.click_on_team_option()
    with allure.step("Invite Admin By Email"):
        click_on_button_name(page, 'Invite')
        setting_page.select_role_to_invite('Admin')
        random = get_random_string()
        email_address = f"dummy_auto_{random}@dummy.com"
        setting_page.enter_email_address_to_invite(email_address)
        token = setting_page.get_invitation_token()

    with allure.step(f"Validate email address as '{email_address}' and status as 'INVITE SENT' is shown"):
        setting_page.check_invited_tab_with_status_and_email_in_team(email_address, 'INVITE SENT')
    with allure.step("Open Invite Link in new incognito tab"):
        base_register_url = init_url('REGISTER_EMPLOYER_URL')

        invitation_link = f"{base_register_url}{token}"
        print(f" - invitation_link link for admin: {invitation_link}")
        page02 = init_context.new_page()
        page02.goto(invitation_link)
        time.sleep(5)
        company_name = "Dummy Auto 01"
    with allure.step(f"Validate Registration page is shown with {email_address} and {company_name}"):
        register_page = RegisterPage(page02)
        register_page.check_register_page_shown('employer')
        register_page.check_email_and_company_name(email_address, company_name)
    with allure.step("Complete Registration step"):
        register_page.enter_password(os.getenv('PASSWORD_OF_NON_ISOLATED_ACC'))
        register_page.click_on_sign_up_button()
        time.sleep(3)
        file_name_dir = f"{cwd}/test_data/media/shrimp_auto.png"
        register_page.upload_profile_image(file_name_dir)
        register_page.enter_profile_data_for_team_invite_flow("Dummy",
                                                              f"Auto {random}")
        register_page.click_on_complete_registration()
    with allure.step("Refresh Setting page and Validate new admin is added to Admin tab"):
        refresh_page(page)
        time.sleep(5)
        setting_page.click_on_team_option()
        setting_page.click_on_option('Admin')
        admin_name = f"Dummy Auto {random}"
        setting_page.check_admin_tab_show_added_admin_info(email_address, admin_name)
    with allure.step("Open Employee Hub & Search for admin name"):
        main_page.access_employee_hub()
        employee_hub = EmployeeHubPage(page)
        employee_hub.search_by_name(admin_name)
    with allure.step(f"Validate new admin name '{admin_name}' is available in Employee Hub with status as active"):
        employee_hub.check_adv_name_with_status_visible_in_list('active', admin_name)


@allure.title("[C2591] Non-SSO - Direct invite Recruiter is worked as expected")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2591")
@allure.tag("profile_02", "network_listener", "user_invitation")
def test_recruiter_direct_invite(init_page_with_full_configure_profile_02, init_context):
    page = init_page_with_full_configure_profile_02
    with allure.step("Access Team in Settings"):
        main_page = MainEmployerPage(page)
        main_page.access_settings()
        setting_page = SettingsPage(page)
        setting_page.click_on_team_option()
    with allure.step("Invite Recruiter By Email"):
        click_on_button_name(page, 'Invite')
        setting_page.select_role_to_invite('Recruiter')
        random = get_random_string()
        email_address = f"dummy_auto_recruiter_{random}@dummy.com"
        setting_page.enter_email_address_to_invite(email_address)
        token = setting_page.get_invitation_token()

    with allure.step(f"Validate email address as '{email_address}' and status as 'INVITE SENT' is shown"):
        setting_page.check_invited_tab_with_status_and_email_in_team(email_address, 'INVITE SENT')
    with allure.step("Open Invite Link in new incognito tab"):
        base_register_url = init_url('REGISTER_EMPLOYER_URL')

        invitation_link = f"{base_register_url}{token}"
        print(f" - invitation_link link for recruiter: {invitation_link}")
        page02 = init_context.new_page()
        page02.goto(invitation_link)
        time.sleep(5)
        company_name = "Dummy Auto 01"
    with allure.step(f"Validate Registration page is shown with {email_address} and {company_name}"):
        register_page = RegisterPage(page02)
        register_page.check_register_page_shown('recruiter')
        register_page.check_email_and_company_name(email_address, company_name)
    with allure.step("Complete Registration step"):
        register_page.enter_password(os.getenv('PASSWORD_OF_NON_ISOLATED_ACC'))
        register_page.click_on_sign_up_button()
        time.sleep(3)
        file_name_dir = f"{cwd}/test_data/media/shrimp_auto.png"
        register_page.upload_profile_image(file_name_dir)
        register_page.enter_profile_data_for_team_invite_flow("Dummy",
                                                              f"Recruiter {random}")
        register_page.click_on_complete_registration()
    with allure.step("Refresh Setting page and Validate new recruiter is added to Recruiter tab"):
        refresh_page(page)
        time.sleep(5)
        setting_page.click_on_team_option()
        setting_page.click_on_option('Recruiter')
        recruiter_name = f"Dummy Recruiter {random}"
        setting_page.check_admin_tab_show_added_admin_info(email_address, recruiter_name)
    with allure.step("Open Employee Hub & Search for recruiter name"):
        main_page.access_employee_hub()
        employee_hub = EmployeeHubPage(page)
        employee_hub.search_by_name(recruiter_name)
    with allure.step(f"Validate new recruiter name '{recruiter_name}' is available in Employee Hub with status as active"):
        employee_hub.check_adv_name_with_status_visible_in_list('active', recruiter_name)
