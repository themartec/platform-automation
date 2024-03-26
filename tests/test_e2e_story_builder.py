import time
from datetime import date
import allure
import os

from utils.init_env import init_url
from common_src.pages.story_builder import StoryBuilderPage
from common_src.pages.main_employer import MainEmployerPage
from common_src.actions.common_action import get_clipboard_data, refresh_page, enter_text, click_on_button_name
from common_src.pages.regsiter import RegisterPage
from common_src.pages.story_hub import StoryHubPage
from common_src.pages.login import LoginPage
from common_src.pages.my_adv_stories import MyStoriesPage
from common_src.utils.dummy_data import get_random_string


@allure.title("End To End Test > Employer branding > Individual Written - Submit a new custom topic with generated "
              "questions and invite advocate via a share link of story")
@allure.description(f"Employer branding > Individual Written > Create Custom Story,"
                    f" Update Generated Question, Search Story, Delete Story")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2598")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2575")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2675")
def test_2e2_flow_01(set_up_tear_down, init_context):
    page = set_up_tear_down
    random_num = get_random_string()
    with allure.step("C2598 - Employer branding > Individual Written - Validate submitting a custom topic"):
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
            story_builder_page.check_summary_page_branding_flow("Summary - Create Story",
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
            my_story_page = MyStoriesPage(page02)
            my_story_page.check_my_stories_is_shown_as_default()
            my_story_page.check_story_title_is_shown(tested_topic)
        with allure.step("Validate story status will be ACCEPTED IN Story Hub"):
            story_hub = StoryHubPage(page)
            refresh_page(page)
            with allure.step("Search topic name in Story Hub"):
                story_hub.search_by_content(tested_topic)
                adv_name = f"Story Dummy {random_num}"
            with allure.step(
                    f"Validate topic name as '{tested_topic}', status as 'ACCEPTED' and assigned adv name '{adv_name}'"):
                story_info_02 = f"{tested_topic}Accepted{adv_name}"
                story_hub.check_story_info_is_shown_in_list(story_info_02)
    with allure.step("C2675 - Story Hub - Be able to delete a story by employer"):
        story_hub.delete_story()
        story_hub.check_story_is_deleted_from_search_view()


@allure.title("End To End Test > Talent Acquisition > Company Written - Publish A New Story & Share Content To Linked "
              "Social "
              "Account")
@allure.description(f"Employer should able to submit and publish to LinkedIn a topic with company written type, "
                    f"category as Talent Acquisition, in that process, the employer can add custom question and "
                    f"re-update the default topic with new title content. The story will be assigned to an advocate "
                    f"to submit his/her answer that is"
                    f"included a comment and doesn't have photo attachment even it is required. With expectation, "
                    f"all data about topic name, question, answer is consistent "
                    f"among account, steps. And the employer can also skip 'Approval Pipeline' step during process")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2649")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2611")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2533")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2608")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2677")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2678")
def test_2e2_flow_02(set_up_tear_down, init_a_page_with_base_url):
    page = set_up_tear_down
    random_num = get_random_string()
    tested_topic = 'Our Tech Stack'
    with allure.step("C2649 - EB Portal - Validate publish a new story with a custom question from Talent Acquisition "
                     "category"):
        with allure.step(
                f"Access Story Builder tab > Talent Acquisition > Pick a available topic, example '{tested_topic}'"):
            main_page = MainEmployerPage(page)
            main_page.access_story_builder_tab()
            story_builder_page = StoryBuilderPage(page)
            story_builder_page.click_on_talent_acquisition_category_tab()
            story_builder_page.click_on_option_name(tested_topic)
        with allure.step(f"Validate heading '{tested_topic}' is shown"):
            story_builder_page.check_heading_with_content(tested_topic)
        with allure.step("Choose Company Written option"):
            story_builder_page.click_on_company_written()
        with allure.step(f"Validate heading '{tested_topic}' are shown"):
            story_builder_page.check_chosen_topic_shown_in_heading_and_topic_field(tested_topic)
        with allure.step("At 'Match a Topic & Select Questions' page"):
            custom_question = "What is main tech stack that is applied to develop the Martec automation framework ?"
            with allure.step(f"Add custom question '{custom_question}'"):
                story_builder_page.enter_custom_question_and_add(custom_question)
            with allure.step(f"Validate custom question is shown in 'MY QUESTIONS' field"):
                story_builder_page.check_my_question(custom_question)
                new_topic_content = f"{random_num} - {tested_topic} As An Automation Engineer At The Martec"
            with allure.step(f"Update topic title with new title as '{new_topic_content}"):
                story_builder_page.update_topic_with_new_content(tested_topic, new_topic_content)
            with allure.step("Check on custom question box and move to next step"):
                story_builder_page.check_on_box_box_of_my_question_at_order(1)
                click_on_button_name(page, "Next")
        with allure.step("Assign to Advocates - Search for an advocate and assign story to that advocate"):
            adv_name = 'Test ADV 01'
            adv_name_role = f'{adv_name}Accountant'
            story_builder_page.search_for_adv_name(adv_name)
            story_builder_page.assign_to_adv(adv_name)
            story_builder_page.check_search_result_of_adv(adv_name_role.lower())
            click_on_button_name(page, "Next")
        with allure.step("At 'Summary - Create Story' page"):
            with allure.step(f"Validate information is shown correctly (heading, topic, tag, questions)"):
                story_builder_page.check_summary_page_talent_flow(heading=tested_topic,
                                                                  topic_name=new_topic_content,
                                                                  tag=tested_topic,
                                                                  questions_list=[custom_question]
                                                                  )

                story_builder_page.check_adv_info_is_shown(adv_name)
            with allure.step("Enter a note"):
                note_content = "this is automation note"
                enter_text(page, "Enter Note", note_content)
            with allure.step("Submit story & Close dialog"):
                click_on_button_name(page, "Submit")
                story_builder_page.check_dialog_is_shown_after_submitting_01()
                story_builder_page.click_on_x_button_of_dialog()
            with allure.step(
                    f"Validate Story Hub page is present with assigned status to '{adv_name}' for tested topic "
                    f"as '{new_topic_content}'"):
                story_hub = StoryHubPage(page)
                story_hub.check_story_hub_is_shown()
                story_hub.check_story_info_is_shown_in_list(f"{new_topic_content}Assigned{adv_name}")
    with allure.step("C2533 - BA Portal > My Stories - Assigned stories are listed with consistent info to EB portal"):
        with allure.step("Access advocate's story page"):
            page02 = init_a_page_with_base_url
            LoginPage(page02).enter_username_password(os.getenv("USER_NAME_OF_ADV_01"),
                                                      os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        with allure.step("From 'My stories' page, validate assigned topic is available"):
            my_story_page = MyStoriesPage(page02)
            my_story_page.check_my_stories_is_shown_as_default()
            my_story_page.check_story_title_is_shown(new_topic_content)
        with allure.step("Open story"):
            my_story_page.click_on_topic_name(new_topic_content)
        with allure.step("Validate topic, question, notes are consistent to employer"):
            my_story_page.check_story_info_is_matching(story=new_topic_content,
                                                       question_lists=[custom_question],
                                                       note=note_content)
    with allure.step("C2611 - BA Portal > My Stories - Responses/Answer can be created with AI"):
        with allure.step("Click on Next"):
            click_on_button_name(page02, "Next")
        with allure.step("Question content is shown correctly and AI ASSISTANT button is disable"):
            my_story_page.check_ui_before_answering(custom_question)
        with allure.step("Answer the question"):
            answer = "Playwright as web automation framework\nAllure as report plugin"
            my_story_page.enter_answer_to_one_question(answer)
        with allure.step("Validate AI READY button is ACTIVE, and can provide the suggestion"):
            my_story_page.get_ai_suggestion()
            ai_answer = my_story_page.check_ai_suggestion_content(answer)
        with allure.step("Click on REVIEW button"):
            click_on_button_name(page02, "Review")
        with allure.step("Validate topic, question & answer is consistent"):
            my_story_page.check_data_is_consistent_at_summary(topic=new_topic_content,
                                                              question_lists=[custom_question],
                                                              ai_answer=ai_answer)
        with allure.step("Add comments, Click on Submit and Submit without photo upload"):
            adv_comment = "this is comment from advocate adv 01"
            enter_text(page02, "Your comment", adv_comment)
            click_on_button_name(page02, "Submit")
            my_story_page.click_on_submit_button_in_dialog()
        with allure.step("Click on DONE button & Close Rating popup"):
            click_on_button_name(page02, "Done")
            my_story_page.click_on_x_button_in_rating_modal()
    with allure.step("C2608 - EB Portal > Review Response - Information is shown correctly for review"):
        refresh_page(page)
        with allure.step(f"Story Hub - Search topic name '{new_topic_content}"):
            story_hub.search_by_content(new_topic_content)
        with allure.step(
                f"Story Hub List - Validate topic name, status as 'READY' and assigned adv name '{adv_name}'"):
            story_info_02 = f"{new_topic_content}Ready{adv_name}"
            story_hub.check_story_info_is_shown_in_list(story_info_02)
        with allure.step("Story Hub List - Open topic name"):
            story_hub.click_on_story_title(new_topic_content)
        with allure.step("Story Details > Review Response - Validate data is consistent"):
            story_hub.check_story_details_consistency(topic=new_topic_content,
                                                      question_lists=[custom_question],
                                                      ai_answer=ai_answer,
                                                      adv_comment=adv_comment,
                                                      adv_name=adv_name,
                                                      responded="Responded (1/1)",
                                                      awaiting_response="Awaiting Responses (0/1)")
    with allure.step("C2649 - EB Portal > Story Details - Skip 'Approval Pipeline' step, then publish story "
                     "successfully"):
        click_on_button_name(page, "Next")
        click_on_button_name(page, "Next")
        click_on_button_name(page, "Ok")
        story_hub.check_story_title_shown_in_publish_screen(new_topic_content)
    with allure.step("C2677 - EB Portal > Publish - Create tracking link before publishing"):
        with allure.step("Create a tracking link"):
            story_hub.create_tracking_link('https://automation.com/martec')
        with allure.step("Validate generated tracking link successfully"):
            story_hub.check_generated_tracking_link()
            story_hub.close_tracking_link_modal()
    with allure.step("C2649 - EB Portal > Publish - Publish story with a tracking link"):
        with allure.step("Enter copied tracking link to 'PUBLISH LINK' field & Update Publish Date"):
            formatted_date = date.today()
            story_hub.update_publish_date(formatted_date)
            publish_link = "https://www.themartec.com/"
            story_hub.enter_publish_link(publish_link)
        with allure.step("Click on 'Mark as Published' button"):
            click_on_button_name(page, 'Mark as Published')
            time.sleep(5)
        with allure.step("Validate story status is 'PUBLISHED' and story is located in 'Published' tab"):
            main_page.access_story_hub_tab()
            story_hub.click_on_published_tab()
            story_hub.search_by_content(new_topic_content)
            story_hub.check_story_info_is_shown_in_list(f"{new_topic_content}Published{adv_name}")
    with allure.step("C2678 - EB Portal > Share Content - Share Now with Linked Social Account Applying AI to "
                     "generate content "):
        with allure.step("Click on 'Share Story' button"):
            story_hub.click_on_share_link_option(new_topic_content)
            # click_on_button_name(page, "Share Story")
        with allure.step("Use 'AI SUGGEST' to generate social copy content"):
            click_on_button_name(page, "AI SUGGEST")
        with allure.step("Validate AI suggest generates un-empty content"):
            sample_ai_social_output = story_hub.check_social_copy_ai_suggest()
            print(f"- sample_ai_social_output: {sample_ai_social_output}")
        with allure.step("Choose the 1st example from 'AI SUGGEST' output list"):
            story_hub.choose_example_of_ai_social_copy(0)
        with allure.step("Choose 'Share Now' option"):
            story_hub.click_on_share_content_option("Share Now")
        with allure.step("Share the content (Linked To LinkedIn)"):
            click_on_button_name(page, "Share Content")
        with allure.step("Access LinkedIn and Validate the shared content"):
            story_hub.access_to_linkedin()
            story_hub.check_content_is_shared_correctly(new_topic_content)
            story_hub.check_content_is_shared_with_short_link(init_url('SHORT_TRACKING_URL'))
