import json
import time

from playwright.sync_api import Playwright, sync_playwright, expect
import re

from e2e_test.src.ai_evals_logic.similarity_check import check_for_similarity
from e2e_test.src.pages.main_employer import MainEmployerPage
import allure

from e2e_test.src.utils.Screenshot import Screenshot


def get_common_generated_question_xpath(order):
    return f"//p[.='Generated Questions']/following-sibling::div[{order}]"


class StoryBuilderPage:
    def __init__(self, page):
        self.page = page

    def check_ai_suggest_topic_is_not_empty(self):
        Screenshot(self.page).take_screenshot()
        list_elements = self.page.locator('div:nth-child(2) > div.topic-list > div')
        count = list_elements.count()
        print("count: " + str(count))
        for i in range(count):
            topic = list_elements.nth(i).text_content()
            assert topic, "Check suggested topic is not empty"

    def check_ai_suggested_topic_tobe_similarity(self, input_topic):
        Screenshot(self.page).take_screenshot_with_custom('screenshot-ai_suggested_topic_tobe_similarity')

        # returned_topics = self.page.locator('div:nth-child(2) > div.topic-list').text_content()
        list_elements = self.page.locator('div:nth-child(2) > div.topic-list > div')
        count = list_elements.count()
        print("count: " + str(count))
        for i in range(count):
            topic = list_elements.nth(i).text_content()
            print("topic: " + topic)
            json_result = json.loads(check_for_similarity(input_topic, topic))
            allure.attach("Similarity Score of Topic '" + topic + "' is " + str(json_result["score"]),
                          name="Similarity Score of Topic at position [" + str(i) + "]",
                          attachment_type="text/plain",
                          extension="attach")
            assert json_result["isSimilar"] == True, f"Check for similarity of generated topics at position " + str(i)
        # for element in list_elements:
        #     topic = element.text_content()
        #     print("topic: "+topic)
        #     json_result = json.loads(check_for_similarity(input_topic, topic))
        #     allure.attach("Similarity Score of Topic '" + topic + "' is "+str(json_result["score"]), name="Similarity Score",
        #                   attachment_type="text/plain",
        #               extension="attach")
        #     assert json_result["isSimilar"] == True

    def access_topic_name_of_employer_branding(self, option_name):
        MainEmployerPage(self.page).access_story_builder_tab()
        self.click_on_employer_branding()
        self.click_on_option_name(option_name)
        self.click_on_individual_written()

    def enter_topic_name_and_get_ai_suggested(self, topic_name):
        self.enter_text_to_topic_box(topic_name)
        self.click_on_AI_suggest_button()

    def click_on_employer_branding(self):
        self.page.locator("div").filter(
            has_text=re.compile(r"^Employer BrandingShowcase business impact of employer branding$")).first.click()

    def click_on_option_name(self, option_name):
        self.page.get_by_text(option_name).click()

    def click_on_individual_written(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Individual Written$")).first.click()

    def enter_text_to_topic_box(self, text):
        self.page.get_by_placeholder("Enter a topic, select from").click()
        self.page.get_by_placeholder("Enter a topic, select from").fill(text)

    def click_on_AI_suggest_button(self):
        self.page.get_by_role("button", name="AI Suggest").click()
        time.sleep(5)

    def check_suggested_list_includes_text(self, text):
        expect(self.page.locator('div:nth-child(2) > div.topic-list')).to_contain_text(text)

    def get_first_title_in_suggest_list(self):
        # SUGGESTED FOR YOU
        return self.page.locator('(//*[@class="topic-list"]/div[1])[1]').text_content()

    def click_on_first_title_in_suggest_list(self):
        self.page.hover('(//*[@class="topic-list"]/div[1])[1]')
        time.sleep(3)
        expect(self.page.locator(".css-1obwxrv").first).to_be_visible()
        self.page.locator('(//*[@class="topic-list"]/div[1])[1]//button').click()
        time.sleep(3)
        self.page.locator('(//*[@class="topic-list"]/div[1])[1]//button').click()

    def click_on_create_new(self):
        self.page.get_by_role("button", name="Create New").click()

    def stick_on_first_question(self):
        self.page.locator(".css-io3ihv").first.click()

    def choose_advocate_to_assign(self, adv_name):
        place_holder_name = "Search for an advocate"
        self.page.get_by_placeholder(place_holder_name).click()
        self.page.get_by_placeholder(place_holder_name).fill(adv_name)
        self.page.locator("span").click()

    def create_new_story(self):
        self.click_on_create_new()

    def assign_story_to_adv(self, adv_name):
        self.click_on_next_button()
        self.choose_advocate_to_assign(adv_name)
        self.click_on_next_button()
        self.page.get_by_role("button", name="Submit").click()
        self.page.locator("#modal").get_by_role("button").first.click()

    def get_first_question(self):
        return self.page.locator("//p[contains(.,'Generated Questions')]/following-sibling::div[1]").text_content()

    # Click Action
    def click_on_employer_branding_category_tab(self):
        self.page.locator("//p[.='Employer Branding']").click()

    def click_on_talent_acquisition_category_tab(self):
        self.page.locator("//p[.='Talent Acquisition']").click()

    def click_on_create_custom_story(self):
        self.page.get_by_text("Create Custom Story").click()

    def click_on_company_written(self):
        self.page.get_by_text("Company Written").click()

    def click_on_create_new_button(self):
        self.page.get_by_role("button", name="Create New").click()

    def click_on_next_button(self):
        self.page.get_by_role("button", name="Next").click()

    # Other Actions
    def enter_brief_topic_to_text_box(self, topic_name):
        self.page.get_by_placeholder("Enter a topic, select from").fill(topic_name)

    def get_question_content_at_order(self, order: int):
        xpath = get_common_generated_question_xpath(order)
        return self.page.locator(xpath).text_content()

    def check_on_box_of_question_at_order(self, order: int):
        self.page.locator(get_common_generated_question_xpath(order)).click()

    def update_question_with_new_content_at_order(self, order: int, new_content: str):
        xpath = get_common_generated_question_xpath(order)
        self.page.locator(xpath).hover()
        self.page.locator(xpath + "/button").click()
        self.page.get_by_role("textbox").first.fill(new_content)
        self.page.get_by_role("textbox").first.press("Enter")
        Screenshot(self.page).take_screenshot()

    # Assertion
    def check_categories_topic_list(self, topics_text):
        elements_text = self.page.locator("div.css-1dzy8az > div").text_content()
        print(f"elements_text: {elements_text}")
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator("div.css-1dzy8az > div")).to_have_text(topics_text)

    def check_heading_with_content(self, content):
        expect(self.page.get_by_text(content)).to_be_visible()

    def check_topic_with_content(self, content):
        expect(self.page.get_by_text(content)).to_be_visible()

    def check_border_color(self, order: int, color: str):
        xpath = get_common_generated_question_xpath(order)

        current_color = self.page.locator(xpath).evaluate('(e) => window.getComputedStyle(e).getPropertyValue('
                                                          '"border-top-color")')
        print(f"color: {color}")
        assert current_color == color

    def check_updated_question_is_correct(self, order: int, content):
        expect(self.page.get_by_text(content)).to_be_visible()
        expect(self.page.locator(get_common_generated_question_xpath(order)+"//input")).to_be_checked()

    def check_summary_page(self, heading, topic_name, tag, questions_list):
        expect(self.page.get_by_text(heading)).to_be_visible()
        expect(self.page.get_by_text(topic_name)).to_be_visible()
        expect(self.page.locator(f"//p[.='Tag']/following-sibling::div[.='{tag}']")).to_be_visible()
        for question in questions_list:
            expect(self.page.get_by_role("button", name=question)).to_be_visible()
            print(f"Check for question '{question} is correct !'")

    def check_dialog_is_shown_after_submitting(self):
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_role("img", name="brand cover")).to_be_visible()
        expect(self.page.get_by_text("Your story has been submitted")).to_be_visible()
        self.page.get_by_text("We’ll notify you when the").click()
        expect(self.page.get_by_role("button", name="Share story link")).to_be_visible()

    def check_dialog_is_not_shown(self):
        expect(self.page.get_by_role("img", name="brand cover")).not_to_be_visible()


