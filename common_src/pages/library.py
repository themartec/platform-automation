import os
import time

from playwright.sync_api import expect

from common_src.utils.Screenshot import Screenshot


class LibraryPage:

    def __init__(self, page):
        self.page = page

    def check_header_title_is_correct(self, title_name):
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator("#root")).to_contain_text(title_name)

    def check_question_is_correctly_shown(self, question_content):
        expect(self.page.get_by_role("article")).to_contain_text(question_content)

    def check_type_of_media(self, media_type):
        expect(self.page.get_by_role("article")).to_contain_text(media_type.upper())

    def check_status_of_media(self, status):
        expect(self.page.get_by_role("article")).to_contain_text(status.upper())

    def check_edit_icon_in_thumbnail(self):
        self.page.locator("//div[contains(@class,'left-body')]/div").hover()
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator(".edit-video")).to_be_visible()

    def click_on_edit_button_of_vide_name(self, video_name):
        with (self.page.expect_popup() as page1_info):
            self.page.get_by_role("article").locator("div").filter(has_text=video_name).get_by_role("img").nth(
                3).click()
        return page1_info.value

    def check_edit_page_is_opened_after_clicking_on_edit_button(self):
        expect(self.page.get_by_text("Create Studio")).to_be_visible(timeout=10000)
        Screenshot(self.page).take_screenshot()

    def check_download_icon_in_thumbnail_of_video(self, video_name):
        self.page.locator("//div[contains(@class,'left-body')]/div").hover()
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_role("article").locator("div").filter(has_text=video_name).get_by_role("img").nth(
            1)).to_be_visible()

    def click_on_download_button_in_thumbnail_of_video(self, video_name):
        with self.page.expect_download(timeout=0) as download_info:
            self.page.locator("//div[contains(@class,'left-body')]/div").hover()
            self.page.get_by_role("article").locator("div").filter(has_text=video_name).get_by_role("img").nth(
                1).click()
        download = download_info.value
        print(f"origin download: {download}")
        suggested_filename = "download_from_thumbnail.mp4"
        download.save_as(suggested_filename)
        return suggested_filename

    def check_file_is_downloaded_successfully(self, file_name_path):
        if os.path.isfile(file_name_path):
            return True
        else:
            print(f"File is NOT existed.")
            return False

    def search_for_story(self, story_name):
        self.page.get_by_placeholder("Search for headline or topic").click()
        self.page.get_by_placeholder("Search for headline or topic").fill(story_name)
        self.page.get_by_placeholder("Search for headline or topic").press("Enter")
        time.sleep(3)


