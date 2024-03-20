import os
import time

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

    def check_story_details_consistency(self, topic, question_lists, ai_answer, adv_comment, adv_name, responded,
                                        awaiting_response):
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_text("Story Details")).to_be_visible()
        expect(self.page.get_by_text(topic)).to_be_visible()
        for question in question_lists:
            expect(self.page.get_by_text(question)).to_be_visible()
        expect(self.page.get_by_text(adv_name).nth(1)).to_be_visible()
        expect(self.page.get_by_text(adv_name).first).to_be_visible()

        expect(self.page.get_by_text(responded)).to_be_visible()
        expect(self.page.get_by_text(awaiting_response)).to_be_visible()

        expect(self.page.get_by_text(adv_comment)).to_be_visible()
        format_answer = ai_answer.replace('\n', ' ')
        print(f"format_answer: {format_answer}")
        expect(self.page.get_by_placeholder("Add an answer")).to_contain_text(format_answer)

    def check_story_title_shown_in_publish_screen(self, topic):
        expect(self.page.get_by_text(topic)).to_be_visible()

    def create_tracking_link(self, track_url):
        self.page.get_by_role("button", name="Create tracking link").click()
        self.page.locator("//p[.='website url']/parent::div/following-sibling::div//input").click()
        self.page.get_by_text(track_url, exact=True).click()
        self.page.get_by_role("button", name="generate tracking link").click()

    def check_generated_tracking_link(self, test_env):
        Screenshot(self.page).take_screenshot()
        # "https://shortstaging.themartec.com/L9EVF"
        xpath = "//div[.='Create Tracking Link']/following-sibling::div//input"
        cur_url = self.page.locator(xpath).input_value()
        print(f"cur_url: {cur_url}")

        assert f"https://short{test_env}.themartec.com/" in cur_url

    def enter_copied_tracking_link(self, clipboard_url):
        self.page.get_by_placeholder("Enter link").fill(clipboard_url)

    def click_on_share_content_option(self, param):
        self.page.get_by_text(param).click()

    def enter_social_copy_text(self, social_content):
        (self.page.get_by_placeholder("Write something about the")
         .fill(social_content))

    def check_social_copy_ai_suggest(self):
        time.sleep(10)
        expect(self.page.locator("//*[@id='example-0']/p[1]")).not_to_be_empty(timeout=10000)
        expect(self.page.locator("//*[@id='example-0']/p[2]")).not_to_be_empty(timeout=10000)
        return self.page.locator("//*[@id='example-0']/p[1]").text_content()

    def access_to_linkedin(self):
        self.page.goto("https://www.linkedin.com/")
        self.page.get_by_label("Email or Phone").fill(os.getenv("LINKED_IN_USER_NAME"))
        self.page.locator("//input[@type='password']").fill(os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        self.page.locator("//div[@data-id='sign-in-form__footer']/button").click()
        time.sleep(10)
        self.page.goto("https://www.linkedin.com/in/huong-trinh-7146612bb/recent-activity/all/")
        time.sleep(5)

    def choose_example_of_ai_social_copy(self, order: int):
        self.page.locator(f"//*[@id='example-{order}']").click()
        Screenshot(self.page).take_screenshot()

    def check_content_is_shared_correctly(self, tested_topic):
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_label(f"Open article: {tested_topic}")).to_be_visible()

    def check_content_is_shared_with_short_link(self, url):
        expect(self.page.locator(f"//a[contains(@href,'{url}')]")).to_have_count(1)

    def update_publish_date(self, today):
        today_year = today.year
        today_month = today.month  # Numeric format (1-12)
        today_day = today.day
        month_name = today.strftime("%b")
        time.sleep(5)
        self.page.locator("#calendar-portal").get_by_role("img").click()
        current_year_month = self.page.locator("//div[@class='react-datepicker__month-container']//p").text_content()
        today_year_month = str(month_name) + ' ' + str(today_year)
        print(f"    - current_year_month: {current_year_month}, today_year_month: {today_year_month}")
        if current_year_month != today_year_month:
            self.page.locator("#calendar-portal button").first.click()
        self.page.locator(f"//div[@class='react-datepicker__week']/div[.='{today_day}']").click()

    # def check_hashtag(self):
    #     before_content = self.page.locator("//textarea").text_content()
    #     print(f"before_content: {before_content}")
    #     self.page.locator("//button[.='Add Hashtag']").click()
    #     time.sleep(120)
    #     after_content = self.page.locator("//textarea").text_content()
    #     print(f"after_content: {after_content}")
    #     assert f"{before_content} #" == after_content
    def click_on_published_tab(self):
        self.page.locator("//p[.='Published']").click()

    def click_on_share_link_option(self, topic_name):
        xpath_01 = f"//p[.='{topic_name}']"
        xpath_02 = "//button[contains(@class,'ellipsis-button')]"
        self.page.locator(xpath_01).hover()
        self.page.locator(xpath_02).hover()
        self.page.get_by_role("button", name="Share Story").click()

