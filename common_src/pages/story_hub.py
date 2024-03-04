import json
import time

from playwright.sync_api import Playwright, sync_playwright, expect
import re

from e2e_test.src.ai_evals_logic.similarity_check import check_for_similarity
from e2e_test.src.pages.main_employer import MainEmployerPage
import allure

from e2e_test.src.utils.Screenshot import Screenshot


class StoryHubPage:
    def __init__(self, page):
        self.page = page

    def click_on_next_button(self):
        self.page.get_by_role("button", name="Next").click()

    def click_on_story_title(self, title):
        self.page.get_by_role("cell", name=title).get_by_role("paragraph").click()

    def check_story_title_shown_in_story_details(self, title):
        # expect(self.page.getByText(title)).toBeVisible()
        expect(self.page.locator("#root")).to_contain_text(title)

    def click_on_create_AI_Prompts_button(self):
        self.page.get_by_role("button", name="Create AI Prompts").click()

    def check_options_text_are_shown(self):
        expect(self.page.get_by_text("Headline")).to_be_visible()
        expect(self.page.get_by_text("Key Points", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Tone of Voice")).to_be_visible()
        expect(self.page.get_by_text("Content Language")).to_be_visible()

    def replace_all_tone_of_voice(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Energetic$")).get_by_role("img").click()
        self.page.locator("span").filter(has_text="Innovative Assured Authentic").locator("path").first.click()
        self.page.locator("span").filter(has_text="Assured Authentic Inclusive").get_by_role("img").first.click()
        self.page.locator("span").filter(has_text="Authentic Inclusive").locator("path").first.click()
        self.page.locator("span").filter(has_text="Inclusive").locator("path").click()

    def select_tone_of_voice(self, tone_of_voice):
        self.page.get_by_placeholder("e.g. professional, casual,").fill(tone_of_voice)
        self.page.get_by_placeholder("e.g. professional, casual,").press("Enter")

    def select_content_language(self, language_option):
        self.page.locator("div").filter(has_text=re.compile(r"^" + language_option + "$")).first.click()
        self.page.get_by_role("option", name="British English").click()

    def click_on_draft_with_ai_button(self):
        self.page.get_by_role("button", name="Draft with Ai").click()

    def collect_content(self):
        list_content = []
        list_elements = self.page.locator("form > div > div")
        count = list_elements.count()

        for i in range(1, count):
            content = list_elements.nth(i).text_content()
            print(f"content: {content} at i={i}")
            if 'add section' not in content.lower():
                list_content.append(content)

        return list_content

    def check_adv_is_shown_in_story_details(self, adv_name):
        expect(self.page.get_by_text(adv_name).first).to_be_visible()

    def check_question_is_shown_in_story_details(self, question):
        expect(self.page.get_by_text(question)).to_be_visible()

    def check_studio_video_is_existed(self):
        xpath = "//div[.='Studio Videos']/following-sibling::div//media"
        list_elements = self.page.locator(xpath)
        media_link = []
        for i in range(list_elements.count()):
            link = list_elements.nth(i).get_attribute('src')
            media_link.append(link)
        print(f"media_link: {media_link}")
        assert len(media_link) == 1
        assert '.mp4' in media_link[0]
        # assert 'story/how-do-you-stay-motivated-and-productive-while-working-remotely' in media_link[0]
        return media_link
