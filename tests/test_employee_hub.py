import time
from datetime import date, timedelta

import allure
import os

from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.employee_hub import EmployeeHubPage
from common_src.pages.settings import SettingsPage
from common_src.pages.login import LoginPage
from common_src.pages.regsiter import RegisterPage
from common_src.database.database import MartecDatabase
from common_src.utils.dummy_data import get_dummy_string_for_email_address, get_random_string


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


@allure.title("[C2581, C2582] Direct Invite - Email templates are synced from Settings")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2581")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2582")
def test_add_new_advocate_template(set_up_tear_down, init_a_page_with_base_url):
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
            number_part = get_random_string()
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
    with allure.step("[C2581] Validate A New Template Can Be Created From Direct Invite View"):
        with allure.step("Update Current Template & Check Its Affection To Current View"):
            employee_page.update_template_with_content(body, number_part + " This is new update from Automation - " +
                                                       body)
            employee_page.click_on_save_template_button()
            time.sleep(20)
            new_template_name = adv_template_name + " [New]"
            employee_page.enter_new_template_name(new_template_name)
            employee_page.check_new_template_is_shown_in_direct_invite(new_template_name)
        with allure.step("Validate Newly Update Template In Settings"):
            main_page.access_settings()
            setting_page.click_on_option("Message Templates")
            setting_page.check_template_shown_on_invite_advocate(new_template_name)
    with allure.step("[C2582] Email templates are synced for accounts in the same company"):
        page02 = init_a_page_with_base_url
        LoginPage(page02).enter_username_password(os.getenv("USER_NAME_OF_EMPLOYER_2"),
                                                  os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        with allure.step("Access to Settings > Message Templates > Invite Advocate"):
            MainEmployerPage(page02).access_settings()
            setting_page_02 = SettingsPage(page02)
            setting_page_02.click_on_option("Message Templates")
            setting_page_02.click_on_option("Invite Advocates")
        with allure.step("Validate Email templates are synced"):
            template_list = ['Invite Advocates Origin',
                             'Invite Advocates - Specific Campaign',
                             adv_template_name,
                             new_template_name]
            setting_page_02.check_list_of_invite_adv_templates(template_list)
    with allure.step("Validate Delete An Invite Advocate Template In Settings"):
        setting_page.set_template_as_default("Invite Advocates - Specific Campaign")
        setting_page.delete_invite_adv(new_template_name)
        setting_page.delete_invite_adv(adv_template_name)


# @pytest.mark.skip(reason="Feature is being updated")
@allure.title("[C2580][1] Employee Hub - Filter is worked as expected in case applying adv status")
@allure.description(f"Filter By Status As Active, Deleted, Invitation Sent, Bench & Clear All")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2580")
def test_filter_01(set_up_tear_down):
    page = set_up_tear_down
    employee_page = EmployeeHubPage(page)
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
    with allure.step("[1] Validate Filter By Combined Status As 'Active' And 'Bench'"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list_employee_hub('Advocate Status', ['Active', 'Bench'])
        employee_page.click_on_apply_button()
        employee_page.check_filter_is_correct(['Active', 'Bench'])
        employee_page.check_filter_is_correct(['Active', 'Bench'])
    with allure.step("Clear All Filter"):
        employee_page.remove_filter()
    with allure.step("[2] Validate Filter By Combined Status As 'Delete' and 'Invitation Sent'"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list_employee_hub('Advocate Status', ['Deleted', 'Invitation Sent'])
        employee_page.click_on_apply_button()
        employee_page.check_filter_is_correct(['Deleted', 'Invitation Sent'])
        employee_page.remove_filter()
    with allure.step("[3] Validate filter by 'Select All'"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list_employee_hub('Advocate Status', ['Select All'])
        employee_page.check_filter_with_selecting_all()
        employee_page.click_on_apply_button()
        # check one of status is shown (not cover all for performance)
        employee_page.check_filter_is_correct(['Invitation Sent', 'Bench', 'Active', 'Deleted'])
    with allure.step("[4] Clear All Filter & Validate checked options are reset"):
        employee_page.click_on_filter_button()
        employee_page.click_on_clear_all_button()
        employee_page.check_options_are_reset('Deleted')
        employee_page.check_options_are_reset('Select All')
        employee_page.click_on_apply_button()


# @pytest.mark.skip(reason="Feature is being updated")
@allure.title("[C2580][2] Employee Hub - Filter is worked in case mixed options (adv status & adv type), "
              "filter by custom field")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2580")
def test_filter_02(set_up_tear_down):
    page = set_up_tear_down
    employee_page = EmployeeHubPage(page)
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
    with allure.step("[1] Validate Mixed Filter By Adv Status='Active' And Adv Type='Starred Advocate'"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list_employee_hub('Advocate Status', ['Active'])
        employee_page.set_filter_by_list_employee_hub('Advocate Type', ['Star Advocate'])
        employee_page.click_on_apply_button()
        employee_page.check_filter_is_correct(['Active'])
        employee_page.check_star_is_shown("Test ADV 02")
    with allure.step("Clear All Filter"):
        employee_page.remove_filter()
    with allure.step("[2] Validate Custom Field Filter - Department Field"):
        employee_page.click_on_filter_button()
        employee_page.set_filter_by_list_custom_field('Department', ['Accounting'])
        employee_page.click_on_apply_button()
        employee_page.check_content_is_existed_in_list('Test ADV 01')
        employee_page.check_content_is_existed_in_list('Test ADV 05')
    with allure.step("Clear All Filter"):
        employee_page.remove_filter()
    with allure.step("[3] Validate Searching Field in Filter"):
        employee_page.click_on_filter_button()
        search_content = "Community"
        employee_page.search_in_filter(search_content)
        employee_page.check_search_in_filter("Employee Hub", search_content)


@allure.title("[C2579][1] Delete Advocate & Single Filter By Status (DELETED)")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2579")
def test_account_action_delete(set_up_tear_down):
    page = set_up_tear_down
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
        employee_page = EmployeeHubPage(page)
    with allure.step("Validate Delete option"):
        employee_page.search_by_name('Story Dummy')
        deleted_adv_name = employee_page.perform_action_adv_with_info_and_return_name('Delete',
                                                                                      'Story Dummy',
                                                                                      'active',
                                                                                      2)
        employee_page.search_by_name(deleted_adv_name)
        employee_page.filter_single_by_status("Deleted")
        employee_page.check_adv_name_with_status_visible_in_list('deleted', deleted_adv_name)


@allure.title("[C2579][2] Bench Advocate & Single Filter By Status ")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2579")
def test_account_action_bench(set_up_tear_down, init_a_page_with_base_url):
    page = set_up_tear_down
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
        employee_page = EmployeeHubPage(page)
    with allure.step("Validate Bench option"):
        to_bench_adv_name = 'Test Adv To Bench'
        with allure.step(f"Search {to_bench_adv_name}"):
            employee_page.search_by_name(to_bench_adv_name)

        with allure.step("Click on 'Bench' option to advocate of status active"):
            to_bench_adv_name = employee_page.perform_action_adv_with_info_and_return_name('Bench',
                                                                                           to_bench_adv_name,
                                                                                           'active',
                                                                                           1)

        with allure.step("Validate adv is now in bench status"):
            employee_page.check_adv_name_with_status_visible_in_list('bench', to_bench_adv_name)
        with allure.step("Validate bench adv can not login to portal anymore"):
            page02 = init_a_page_with_base_url
            login_page_02 = LoginPage(page02)
            login_page_02.enter_username_password('test.adv965scw@themartec.com',
                                                  os.getenv('PASSWORD_OF_NON_ISOLATED_ACC'))
            login_page_02.check_login_is_unsuccessful_as_wrong_username()
    with allure.step("Validate be able to 'Un-Bench' for Advocate & Advocate login is successful"):
        with allure.step("Status advocate will change to active after performing unbench action"):
            employee_page.perform_action_adv_with_info_and_return_name('Unbench',
                                                                       to_bench_adv_name,
                                                                       'bench',
                                                                       1)
            employee_page.check_adv_name_with_status_visible_in_list('active', to_bench_adv_name)
        with allure.step("Advocate can log in BA portal again"):
            login_page_02.enter_username_password('test.adv965scw@themartec.com',
                                                  os.getenv('PASSWORD_OF_NON_ISOLATED_ACC'))
            login_page_02.check_login_successfully_for_ba_portal()


@allure.title("[C2680] Direct Invite - Resend Invite & Check For Expired, Renewed Token Event")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2680")
@allure.tag("db_required", "network_listener")
def test_account_direct_invite(set_up_tear_down_with_full_configure, init_context):
    page = set_up_tear_down_with_full_configure
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
        employee_page = EmployeeHubPage(page)
    with allure.step("Access Direct Invite page"):
        employee_page.click_on_active_people_button()
        employee_page.click_on_direct_invite_option()
        email_address = get_dummy_string_for_email_address('eh')
    with allure.step(f"Enter dummy email address '{email_address}'"):
        employee_page.enter_email_address_direct_invite(email_address)
        invitation_link = employee_page.click_on_send_invite_in_direct_invite()
        assert invitation_link != ''
        print(f"invitation_link: {invitation_link}")
    with allure.step(f"Navigate to invitation link in new incognito tab, invitation_link: {invitation_link}"):
        page02 = init_context.new_page()
        page02.goto(invitation_link)
        time.sleep(5)
    with allure.step("Validate invitation link can be opened successfully"):
        with allure.step("Invited email address, company name is auto populated"):
            register_page_02 = RegisterPage(page02)
            register_page_02.check_default_user_info_are_shown(email_address,
                                                               'The Martec')
        with allure.step("UI elements are shown completely"):
            register_page_02.check_register_page_shown()
    with allure.step("Set up for expired event of invitation link"):
        conn = MartecDatabase()
        today_date = date.today()
        expired_date = today_date - timedelta(days=15)
        print(f"expired_date: {expired_date}")
        conn.make_adv_invitation_expire(email_address,
                                        date_tobe_expire=expired_date)
    with allure.step(f"With expired date={expired_date}, validate invitation link will be expired"):
        with allure.step("Navigate to invitation link"):
            page02.goto(invitation_link)
            register_page_02.check_expired_error_message()
    with allure.step("Resend invite to advocate"):
        MainEmployerPage(page).access_employee_hub()
        employee_page.search_by_name(email_address)
        employee_page.resend_invite()
    with allure.step("Try open invitation link again"):
        page02.goto(invitation_link)
        time.sleep(5)
    with allure.step("Validate invitation link is worked"):
        register_page_02 = RegisterPage(page02)
        register_page_02.check_default_user_info_are_shown(email_address,
                                                           'The Martec')