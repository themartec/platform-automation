import re
import time

from playwright.sync_api import expect

from common_src.utils.Screenshot import Screenshot
from common_src.pages.main_employer import MainEmployerPage


class MyStoriesPage:
    def __init__(self, page):
        self.page = page

    def check_my_stories_is_shown_as_default(self):
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator("//div[@type='adv']//p[contains(.,'My Stories')]")).to_be_visible()

    def check_story_title_is_shown(self, story_title):
        Screenshot(self.page).take_screenshot()
        xpath = f"//p[.='{story_title}']"
        expect(self.page.locator(xpath)).to_be_visible()

    def check_data_consistency_between_register_and_settings(self, info_list: list):
        # list as [firstname, lastname, role, department, language]
        self.page.get_by_role("link", name="Settings").click()
        MainEmployerPage(self.page).access_settings()
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_role("img", name="Photo Preview")).to_be_visible()
        expect(self.page.get_by_role("button").nth(2)).to_be_visible()

        expect(self.page.locator("#firstName")).to_have_value(info_list[0])
        expect(self.page.locator("#lastName")).to_have_value(info_list[1])
        expect(self.page.locator("#role")).to_have_value(info_list[2])
        expect(self.page.locator("form")).to_contain_text(info_list[3])
        expect(self.page.locator("div").filter(has_text=re.compile(rf"^{info_list[4]}$")).nth(1)).to_be_visible()
        expect(self.page.locator("//input[@id='email']")).to_have_value(info_list[5])

    def click_on_topic_name(self, new_topic_content):
        self.page.get_by_role("link", name=new_topic_content).click()

    def check_story_info_is_matching(self, story, question_lists, note):
        expect(self.page.get_by_text("Write a Story")).to_be_visible()
        expect(self.page.get_by_text(story)).to_be_visible()
        if note:
            expect(self.page.get_by_text(note)).to_be_visible()
        for question in question_lists:
            expect(self.page.get_by_text(question)).to_be_visible()

    def enter_answer_to_one_question(self, answer):
        self.page.get_by_placeholder("Write here").fill(answer)

    def check_ui_before_answering(self, custom_question):
        expect(self.page.get_by_text(custom_question)).to_be_visible()
        expect(self.page.locator("//span[.='AI ASSISTANT']")).to_be_disabled()

    def get_ai_suggestion(self):
        expect(self.page.get_by_role("button", name="AI READY")).to_be_visible()
        self.page.get_by_role("button", name="AI READY").click()
        for i in range(1, 30):
            is_done = self.page.locator("//span[.='AI ASSISTANT']").count() == 1
            if is_done is True:
                break
            time.sleep(1)

    def check_ai_suggestion_content(self, origin_content):
        ai_suggestion = self.page.locator("//textarea").text_content()
        print(f"output of ai suggestion: {ai_suggestion}")
        intersection = ai_suggestion.replace(origin_content, "")
        print(f"intersection: {ai_suggestion}")
        assert intersection != ''
        return ai_suggestion

    def check_data_is_consistent_at_summary(self, topic, question_lists, ai_answer):
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_text(topic)).to_be_visible()
        for question in question_lists:
            expect(self.page.get_by_text(question)).to_be_visible()
        self.page.get_by_text("View The Answer").click()
        expect(self.page.locator("//div[contains(@class,'review-answer')]//textarea")).to_contain_text(ai_answer)

    def click_on_submit_button_in_dialog(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Submit$")).click()

    def click_on_x_button_in_rating_modal(self):
        self.page.locator("#modal").get_by_role("button").click()

    def check_under_review_shown(self):
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_text("Under Review")).to_be_visible()


