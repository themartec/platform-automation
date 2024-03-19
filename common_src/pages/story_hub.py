from playwright.sync_api import expect
import re

from common_src.utils.Screenshot import Screenshot


class StoryHubPage:
    def __init__(self, page):
        self.page = page

    def click_on_next_button(self):
        self.page.get_by_role("button", name="Next").click()

    def click_on_story_title(self, title):
        self.page.get_by_role("cell", name=title).get_by_role("paragraph").click()

    def search_by_content(self, content):
        self.page.get_by_placeholder("Search for stories or").fill(content)
        self.page.get_by_placeholder("Search for stories or").press("Enter")

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

    def delete_story(self):
        xpath = "//button[contains(@class,'ellipsis-button')]"
        xpath_01 = "//div[contains(@class,'infinite-scroll-component')]//div[@role='row']"
        self.page.locator(xpath_01).hover()
        self.page.locator(xpath).hover()
        self.page.get_by_role("button", name="Delete").click()
        self.page.get_by_role("button", name="OK").click()

    def count_number_of_video(self) -> int:
        xpath = "//div[.='Studio Videos']/following-sibling::div//video"
        return self.page.locator(xpath).count()

    def check_story_is_deleted_from_search_view(self):
        expect(self.page.get_by_text("Click here to create a new")).to_be_visible()

    # Assert
    def check_story_title_shown_in_story_details(self, title):
        expect(self.page.locator("#root")).to_contain_text(title)

    def check_adv_is_shown_in_story_details(self, adv_name):
        expect(self.page.get_by_text(adv_name).first).to_be_visible()

    def check_question_is_shown_in_story_details(self, question):
        expect(self.page.get_by_text(question)).to_be_visible()

    def get_video_links(self):
        xpath = "//div[.='Studio Videos']/following-sibling::div//video"
        list_elements = self.page.locator(xpath)
        media_link = []
        for i in range(list_elements.count()):
            link = list_elements.nth(i).get_attribute('src')
            media_link.append(link)
        print(f"media_link: {media_link}")
        return media_link

    def check_story_info_is_shown_in_list(self, story_info):
        Screenshot(self.page).take_screenshot()
        elements = self.page.locator("//div[@role='row']")
        is_shown = False
        print(f"story_info: {story_info}")
        for i in range(elements.count()):
            text_row = elements.nth(i).text_content()
            print(f"text_row: {text_row}")
            if story_info.lower() in text_row.lower():
                is_shown = True
                assert is_shown is True
                return
        assert is_shown is True

    def check_story_hub_is_shown(self):
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_text("Story Hub")).to_have_count(2)
