import random
import string
import time

import allure
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))
from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.employee_hub import EmployeeHubPage
from common_src.pages.regsiter import RegisterPage
from common_src.pages.my_adv_stories import MyStoriesPage


def generate_random_string():
    # Generate the 3-digit number
    number_part = random.randint(100, 999)  # Ensures 3 digits (inclusive)

    # Generate 3 random lowercase letters
    letters_part = ''.join(random.choices(string.ascii_lowercase, k=3))

    # Combine the number and letters
    random_string = str(number_part) + letters_part
    return random_string


@allure.title("[C2574][1] Non-SSO - Copy Invite advocate magic link is worked as expected With An Existing Email")
@allure.description(f"An existing email is entered to register phase and user can not register successfully")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2574")
def test_magic_link_01(set_up_tear_down, init_context):
    page = set_up_tear_down
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
    with allure.step("Click on ACTIVE PEOPLE button"):
        employee_page = EmployeeHubPage(page)
        employee_page.click_on_active_people_button()
    with allure.step("Click on COPY INVITE LINK button"):
        employee_page.click_on_copy_invite_link_button()
    with allure.step("Open Copied Link In New Window In Incognito mode"):
        clipboard_text = employee_page.get_clipboard_data()
        print(f"    - clipboard_text: {clipboard_text}")
        context_02 = init_context
        page02 = context_02.new_page()
        page02.goto(clipboard_text)
        time.sleep(5)
    with allure.step("[New window] Fill in an existing email and a correct format password, repeated password "
                     "and check in 'I have read and agreed with the Terms of Use and Privacy Policy.' box"):
        register_page = RegisterPage(page02)
        register_page.enter_register_data("test.adv05@themartec.com",
                                          os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        register_page.check_on_agreement_checkbox()
        register_page.click_on_sign_up_button()
    with allure.step("[New window] At 'Set up your profile' page, click on CREATE PROFILE button"
                     " without entering to any textbox"):
        register_page.click_on_create_profile_button()

    with allure.step("[New window] Validate warning text will show for configured "
                     "required fields (First Name, Last Name, Role)"):
        register_page.check_warning_texts()
    with allure.step("[New window] Now, enter required fields (First Name, Last Name, Role) "
                     "& click on create profile button"):
        register_page.enter_profile_data(first_name="Test",
                                         last_name="Adv 05",
                                         role="Advocacy",
                                         department="Accounting",
                                         language="English")
        register_page.click_on_create_profile_button()
    with allure.step("[New window] Validate error message will shown on screen"):
        # waiting
        pass


@allure.title("[C2574][2] Non-SSO - Copy Invite advocate magic link is worked as expected With A Non-Existing Email")
@allure.description(f"A valid, non-existing email is entered to register phase")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2574")
def test_magic_link_02(set_up_tear_down, init_context):
    page = set_up_tear_down
    with allure.step("Access Employee Hub"):
        MainEmployerPage(page).access_employee_hub()
    with allure.step("Click on ACTIVE PEOPLE button"):
        employee_page = EmployeeHubPage(page)
        employee_page.click_on_active_people_button()
    with allure.step("Click on COPY INVITE LINK button"):
        employee_page.click_on_copy_invite_link_button()
    with allure.step("Open Copied Link In New Window In Incognito mode"):
        clipboard_text = employee_page.get_clipboard_data()
        print(f"    - clipboard_text: {clipboard_text}")
        context_02 = init_context
        page02 = context_02.new_page()
        page02.goto(clipboard_text)
        time.sleep(5)
    with allure.step("[New window] Fill in a valid and non-existing email and a correct format password, repeated "
                     "password"):
        register_page = RegisterPage(page02)
        random_num = generate_random_string()
        email = f"test.adv{random_num}@themartec.com"
        register_page.enter_register_data(email,
                                          os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
    with allure.step("[New window] Validate Sign Up button is disable when uncheck for agreement checkbox"):
        register_page.check_sign_up_button_is_disable()
    with allure.step("[New window] check in 'I have read and agreed with the Terms of Use and Privacy Policy.' box"):
        register_page.check_on_agreement_checkbox()
    with allure.step("[New window] Click on Sign Up"):
        register_page.click_on_sign_up_button()
    with allure.step("[New window] Upload Profile Image & Validate process is successful"):
        cwd = os.getcwd()
        file_name_dir = f"{cwd}/test_data/media/shrimp_auto.png"
        register_page.upload_profile_image(file_name_dir)
        register_page.check_upload_profile_image_is_successful()
    with allure.step("[New window] At 'Set up your profile' page, click on CREATE PROFILE button"
                     " after entering to required fields (First Name, Last Name, Role"):
        user_info = ["Test", f"Dummy {random_num}", "Advocacy Dummy", "Engineering", "English", email]
        print(f"user_info: {user_info}")
        register_page.enter_profile_data(first_name=user_info[0],
                                         last_name=user_info[1],
                                         role=user_info[2],
                                         department=user_info[3],
                                         language=user_info[4])
        register_page.click_on_create_profile_button()
        time.sleep(10)
    with allure.step("[New window] Validate welcome page is showing & can skip this page"):
        register_page.check_welcome_after_register_successfully()
        register_page.click_on_skip_button_at_welcome_page()
    with allure.step("[New window] Validate My Stories Page is shown after skipping"):
        my_story = MyStoriesPage(page02)
        my_story.check_my_stories_is_shown_as_default()
    with allure.step("[New window] Input info are displayed correctly in Settings of Advocate portal when login by "
                     "that advocate"):
        my_story.check_data_consistency_between_register_and_settings(user_info)
    with allure.step("[Origin window] Input info are displayed correctly in Advocate details via Admin portal"):
        with allure.step("Back To Employee Hub"):
            employee_page.click_on_back_button_from_active_people_page()
        with allure.step("Search For Newly Register Advocate"):
            adv_fullname = user_info[0] + ' ' + user_info[1]
            employee_page.search_by_name(adv_fullname)
            employee_page.click_on_adv_name_in_list(adv_fullname)
        with allure.step("Validate Advocate Overview Info"):
            employee_page.check_adv_overview_info(adv_fullname, user_info[2])
        with allure.step("Click on Advocate Details tab"):
            employee_page.click_on_adv_details_tab()
        with allure.step("Validate Advocate Details is matching to Register details"):
            employee_page.check_adv_details(user_info)


