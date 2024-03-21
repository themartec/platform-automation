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
from common_src.pages.login import LoginPage
from common_src.pages.content_recipes import ContentRecipesPage
from common_src.actions.common_action import click_on_button_name

host_lists = {
    "Linkedin": {
        "url": "https://www.linkedin.com/pulse/what-my-life-changing-accident-has-shown-me-telstras-amazing-hoare/"
    },
    "Medium": {
        "url": "https://medium.com/@niteshdancharan2022/how-to-learn-ai-from-scratch-in-2024-a-complete-guide"
               "-08a7a25b8f23"
    },
    "Forbes": {
        "url": "https://www.forbes.com/sites/cmo/2024/03/20/how-googles-ai-search-will-change-marketing-strategy/"
    }
}


@allure.title("")
@allure.description(f"")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}")
@pytest.mark.parametrize("host_list", host_lists.keys())
def test_upload_template(set_up_tear_down_without_state, host_list):
    page = set_up_tear_down_without_state
    print(f"    - host_list: {host_list}")
    with allure.step("Log in"):
        LoginPage(page).enter_username_password("auto.employer03@themartec.com",
                                                os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        time.sleep(10)
    with allure.step("Access 'Content Recipes' tab"):
        main_page = MainEmployerPage(page)
        main_page.access_content_recipes()
        time.sleep(5)
        main_page.access_content_recipes()
        content_recipes_page = ContentRecipesPage(page)
        content_recipes_page.check_page_title_is_correct()
    with allure.step("Open one template & Upload A Example"):
        content_recipes_page.click_on_one_present_template()
        click_on_button_name(page, "My Uploads")
        before_list_size = content_recipes_page.get_number_example_in_my_upload_list()
        print(f"host_lists[host_list]['url']: {host_lists[host_list]['url']}")
        content_recipes_page.click_on_close_upload()
        click_on_button_name(page, "Upload your example")
        content_recipes_page.check_ui_upload_dialog()
        content_recipes_page.enter_example_link_to_upload(host_lists[host_list]['url'])
    with allure.step("Validate Upload Example Is Successful"):
        content_recipes_page.check_upload_successfully(before_list_size)
