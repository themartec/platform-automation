import random
import string
import time

import allure
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))
from common_src.pages.story_builder import StoryBuilderPage
from common_src.pages.main_employer import MainEmployerPage
from common_src.actions.click_on_button import click_on_button_name
from common_src.actions.common_action import get_clipboard_data, refresh_page
from common_src.pages.regsiter import RegisterPage
from common_src.pages.story_hub import StoryHubPage


def generate_random_string():
    # Generate the 3-digit number
    number_part = random.randint(100, 999)  # Ensures 3 digits (inclusive)

    # Generate 3 random lowercase letters
    letters_part = ''.join(random.choices(string.ascii_lowercase, k=3))

    # Combine the number and letters
    random_string = str(number_part) + letters_part
    return random_string


@allure.title("[C2598,C2575,C2675] Individual Written - Submit a new custom topic with generated questions without "
              "assigning advocate and access share link of story")
@allure.description(f"Employer branding > Individual Written > Create Custom Story,"
                    f" Update Generated Question,"
                    f" Skip assigning advocate. Search Story, Delete Story")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2598")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2575")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2675")
def test_category(set_up_tear_down, init_context):
    page = set_up_tear_down
    random_num = generate_random_string()
    with allure.step("C2598 - Validate submitting a custom topic"):
        with allure.step("Access Story Builder tab"):
            MainEmployerPage(page).access_story_builder_tab()
            story_builder_page = StoryBuilderPage(page)
        with allure.step("Click on 'Create Custom Story' in 'Employer branding' tab"):
            story_builder_page.click_on_create_custom_story()
        with allure.step("Click on 'Individual Written' option"):
            story_builder_page.click_on_individual_written()
        with allure.step("Validate heading with content as 'Create Custom Story'"):
            story_builder_page.check_heading_with_content("Create Custom Story")
        with allure.step("Enter custom topic and Click on Create new button"):
            tested_topic = f"[by Automation {random_num}] Development of engineer in explosion era of AI"
            story_builder_page.enter_brief_topic_to_text_box(tested_topic)
            story_builder_page.click_on_create_new_button()
        with allure.step("Validate heading still correct and entered topic shows correctly"):
            story_builder_page.check_heading_with_content("Create Custom Story")
            story_builder_page.check_topic_with_content(tested_topic)
        with allure.step("Check on first and third question in generated question list"):
            story_builder_page.check_on_box_of_question_at_order(1)
            story_builder_page.check_on_box_of_question_at_order(3)
        with allure.step("Update third question with new content"):
            new_ques_content = ("Can you explain the concept of machine learning and its applications in engineering "
                                "for Automation Engineer ?")
            story_builder_page.update_question_with_new_content_at_order(3, new_ques_content)
        with allure.step("Validate updated question is correct and be highlighted with yellow and origin one is in "
                         "green color"):
            story_builder_page.check_updated_question_is_correct(3, new_ques_content)
            story_builder_page.check_border_color(3, "rgb(255, 201, 55)")
            story_builder_page.check_border_color(1, "rgb(145, 219, 182)")
            question_01 = story_builder_page.get_question_content_at_order(1)
        with allure.step("Click on NEXT button, then click on SKIP button at 'Assign to Advocates' page"):
            story_builder_page.click_on_next_button()
            click_on_button_name(page, "Skip")
        with allure.step("Validate heading content, questions and topic name is correct at 'Summary - Create Story' "
                         "page"):
            story_builder_page.check_summary_page("Summary - Create Story",
                                                  tested_topic,
                                                  "Create Custom Story",
                                                  [question_01, new_ques_content]
                                                  )
        with allure.step("Click on Submit button & Check a dialog is shown"):
            click_on_button_name(page, "Submit")
            story_builder_page.check_dialog_is_shown_after_submitting()
        with allure.step("Click on SHARE STORY LINK button in the opened dialog"):
            click_on_button_name(page, "Share story link")
        with allure.step("Validate Dialog is closed and user will be in STORY HUB page"):
            story_builder_page.check_dialog_is_not_shown()
            story_hub = StoryHubPage(page)
            story_hub.check_story_hub_is_shown()
            story_hub.check_story_info_is_shown_in_list(f"{tested_topic}AssignedNo Advocate")
            time.sleep(30)
        with allure.step("Open Share Link in New Incognito tab"):
            clipboard_text = get_clipboard_data(page)
            print(f"    - clipboard_text: {clipboard_text}")
            context_02 = init_context
            page02 = context_02.new_page()
            page02.goto(clipboard_text)

        with allure.step("Validate user is able to view 'Register' page"):
            register_page = RegisterPage(page02)
            register_page.check_register_page_shown()
    with allure.step("C2575 - Non-SSO - Copy Story magic link is worked as expected"):
        email = f"test.dummy{random_num}@themartec.com"

        with allure.step("Enter Register Info & Sign Up"):
            register_page.enter_register_data(email,
                                              os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
            register_page.check_on_agreement_checkbox()
            register_page.click_on_sign_up_button()
        with allure.step("Enter Profile Info & Create It"):
            register_page.enter_profile_data(first_name="Story",
                                             last_name=f"Dummy {random_num}",
                                             role="Advocacy",
                                             department="Accounting",
                                             language="English")
            register_page.click_on_create_profile_button()
        with allure.step("Validate Register is successful and advocate can view story in his/her story list"):
            register_page.check_welcome_after_register_successfully()
            register_page.click_on_skip_button_at_welcome_page()
            register_page.check_my_stories_is_shown_as_default()
            register_page.check_story_title_is_shown(tested_topic)
        with allure.step("Validate story status will be ACCEPTED IN Story Hub"):
            story_hub = StoryHubPage(page)
            refresh_page(page)
            with allure.step("Search topic name in Story Hub"):
                story_hub.search_by_content(tested_topic)
                adv_name = f"Story Dummy {random_num}"
            with allure.step(f"Validate topic name as '{tested_topic}', status as 'ACCEPTED' and assigned adv name '{adv_name}'"):
                story_info_02 = f"{tested_topic}Accepted{adv_name}"
                story_hub.check_story_info_is_shown_in_list(story_info_02)
    with allure.step("C2675 - Story Hub - Be Able to Delete A Story by employer"):
        story_hub.delete_story()
        story_hub.check_story_is_deleted_from_search_view()