import os
import re
import time
import cv2
from playwright.sync_api import expect

from common_src.utils.Screenshot import Screenshot
from common_src.patterns.studio_sub_tab_name import StudioSubTab

MEDIA_URL = "https://cdndev.themartec.com/videos"
xpath_first_add_button = "//div[contains(@class,'btn-remove')]/following-sibling::div[1]"


class CreativeStudioPage:
    def __init__(self, page):
        self.page = page

    # BRAND KIT -------------------------------------------------------------------
    def access_brand_kit_tab(self):
        self.page.get_by_text("Brand Kit").click()
        time.sleep(5)

    def click_to_add_typography(self, font_file):
        xpath = "//input[contains(@accept,'font')]/following-sibling::div"
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(xpath).click()
        file_chooser = fc_info.value
        file_chooser.set_files(font_file)
        time.sleep(5)

    def check_typography_is_loaded(self):
        xpath = "//div[.='Typography']/following-sibling::div//p[.='A']"
        expect(self.page.locator(xpath)).to_be_visible()

    def close_to_remove_typography(self):
        self.page.locator("(//div[contains(@class,'container-xs')])[1]").hover()
        self.page.locator("(//div[contains(@class,'close-bock-icon')])[1]").click()

    def setup_non_typography_is_existed(self):
        xpath = "div:nth-child(4) > .css-1jevaiu > div:nth-child(12)"
        is_existed = self.page.locator(xpath).count() == 0
        if is_existed:
            self.close_to_remove_typography()
        expect(self.page.locator(xpath)).to_be_visible()

    def check_non_typography_is_existed(self):
        xpath = "div:nth-child(4) > .css-1jevaiu > div:nth-child(12)"
        expect(self.page.locator(xpath)).to_be_visible()

    def check_non_color_is_existed(self):
        self.page.mouse.wheel(0, 500)
        xpath = "div:nth-child(6) > .css-1jevaiu > div:nth-child(12)"
        expect(self.page.locator(xpath)).to_be_visible()

    def setup_non_color_is_existed(self):
        self.page.mouse.wheel(0, 500)
        xpath = "div:nth-child(6) > .css-1jevaiu > div:nth-child(12)"
        is_existed = self.page.locator(xpath).count() == 0
        if is_existed:
            self.click_close_to_remove_color()
        expect(self.page.locator(xpath)).to_be_visible()

    def click_to_add_color(self, color_code):
        self.page.locator(".plus-dashed > svg").click()
        self.page.get_by_label("hex").fill(color_code)
        self.page.get_by_role("button", name="Confirm").click()

    def check_color_is_loaded(self):
        expect(self.page.locator("//div[contains(@color,'rgba')]")).to_be_visible()

    def click_close_to_remove_color(self):
        self.page.mouse.wheel(0, 500)
        time.sleep(3)
        self.page.locator("//div[@class='plus-dashed']/following-sibling::div[contains(@class,"
                          "'container-xs')]").hover()
        close_ele = self.page.locator("(//div[contains(@class,'close-bock-icon')])[2]")
        if close_ele.count() > 1:
            self.page.locator("(//div[contains(@class,'close-bock-icon')])[2]").click()
        else:
            self.page.locator("(//div[contains(@class,'close-bock-icon')])").click()

    # Stories tab -------------------------------------------------------------------
    def click_on_stories_tab(self):
        self.page.get_by_text("Stories").click()

    def check_video_is_displayed_in_stories_tab(self, media_url):
        xpath = (f"//div[contains(@class,'asset-upload')]//video["
                 f"@src='{media_url}']")
        expect(self.page.locator(xpath)).to_be_visible()

    def check_video_is_displayed_in_preview(self, media_url):
        xpath = (f"//div[contains(@class,'video-react-controls')]//video["
                 f"@src='{media_url}']")
        expect(self.page.locator(xpath)).to_be_visible()

    def check_video_is_displayed_in_timeline(self):
        xpath = f"//div[@id='control-frame-editing']//div[contains(@id,'thumbnail-box')]"
        expect(self.page.locator(xpath)).to_be_visible()

    # -------------------------------------------------------------------
    def export_video_with_resolution(self, resolution_type):
        # Start waiting for the download
        with self.page.expect_download(timeout=0) as download_info:
            # Perform the action that initiates download
            self.page.get_by_role("button", name="Export").click()
            self.page.get_by_text("Download").click()
            self.page.get_by_text(resolution_type).click()
            self.page.locator("#modal").get_by_role("button", name="Export").click()
        download = download_info.value
        print(f"download: {download}")
        # Wait for the download process to complete and save the downloaded file somewhere
        download.save_as(download.suggested_filename)
        return download.suggested_filename

    def get_file_dimension(self, file_path):
        vid = cv2.VideoCapture(file_path)
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        return f"{width}x{height}"

    def check_file_is_downloaded_successfully(self, file_name_path, expected_file_dimension):
        if os.path.isfile(file_name_path):
            file_size = round(float(os.path.getsize(file_name_path) / 1000000), 1)
            file_dimension = self.get_file_dimension(file_name_path)
            print(f"    - file_name_path: {file_name_path}")
            print(f"    - file_size: {file_size}")
            print(f"    - file_dimensions: {file_dimension}")

            # if file_size == round(float(expected_file_size), 1) and expected_file_dimension == file_dimension:
            if expected_file_dimension == file_dimension:
                return True
            else:
                print(f"File is existed, but format is not correct, please check stdout for more info")
                return False
        else:
            print(f"File is NOT existed.")
            return False

    def check_if_save_to_story_is_completed(self, timeout: int):
        xpath = "//button[@loading='true']"
        for x in range(timeout):
            time.sleep(1)
            if self.page.locator(xpath).count() == 0:
                print(f" Waiting for export, break at {x}x1 (s)")
                break

    def save_to_story_video_with_resolution(self, resolution_type):
        self.page.get_by_role("button", name="Export").click()
        self.page.get_by_text("Save to Story").click()
        self.page.get_by_text(resolution_type).click()
        self.page.locator("#modal").get_by_role("button", name="Export").click()
        time.sleep(2)
        self.check_if_save_to_story_is_completed(90)

    # Template
    def check_template_is_shown_on_Templates_tab(self, image_dir, name, tag):
        expect(self.page.get_by_text(name)).to_be_visible()
        xpath = f"//p[.='Templates']/following-sibling::div[2]//div[@src='{image_dir}']"
        print(f"    - xpath: {xpath}, {self.page.locator(xpath).count()}")
        expect(self.page.locator(xpath)).to_have_count(1)
        # assert self.page.locator(xpath).count() == 1
        xpath_01 = f"//div[@src='{image_dir}']/following-sibling::div[.='{tag}']"
        expect(self.page.locator(xpath_01)).to_have_count(1)
        # assert self.page.locator(xpath_01).count() == 1

    def click_on_Brand_tab(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Brand$")).click(timeout=30)

    def click_on_edit_template(self, image_dir, position):
        # self.page.mouse.down()
        xpath = f"//p[.='Templates']/following-sibling::div[2]//div[@src='{image_dir}']"
        self.page.locator(xpath).hover()
        self.page.locator(f"(//div[contains(@class,'pencil-wrapper')])[{position}]").click()

    # Video Library ------------------------------------
    def access_video_library_tab(self):
        self.page.get_by_text("Video Library").click()

    def click_on_web_and_blogs(self):
        with self.page.expect_popup() as page2_info:
            self.page.get_by_text(":9Web & BlogsWebsite, Embed").click()
        return page2_info.value

    def check_all_media_types_shown_in_all_tab_name(self, number_of_media: int):
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_text("ALL", exact=True)).to_be_visible()
        expect(self.page.locator("//div[contains(@class,'asset-upload')]/div")).to_have_count(number_of_media)

    def click_on_upload_button_and_set_file(self, file_name):
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator("//span[.='Upload']").click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_name)
        time.sleep(5)

    # main tab
    def click_on_media_tab(self):
        self.page.locator("p").filter(has_text="Media").click()

    def click_on_Brand_tab_of_media(self):
        self.page.get_by_label("Media").get_by_text("Brand").click()

    # ----------------------
    #  sub-tab list header
    def click_on_tab_name(self, tab_name: str):
        self.page.get_by_text(tab_name, exact=True).click()

    def click_on_remove_button_on_media(self):
        self.page.locator("//div[contains(@class,'asset-upload')]/div").hover()
        self.page.get_by_label("Media").get_by_role("img").nth(1).click()

    def click_to_add_button_of_first_media(self):
        self.page.locator(xpath_first_add_button).click()

    # ------------------------------------------
    #  timeline box
    def click_to_remove_media_in_timeline(self, media_name):
        self.page.get_by_text(media_name).hover()
        self.page.locator("#menu-vertical-lite path").nth(1).click()
        self.page.get_by_text("Remove").click()

    def check_media_can_be_added_and_remove_in_timeline(self, media_name):
        time.sleep(3)
        self.click_to_add_button_of_first_media()
        expect(self.page.get_by_text(media_name)).to_be_visible()
        Screenshot(self.page).take_screenshot_with_custom("After Add To Timeline")
        self.click_to_remove_media_in_timeline(media_name)
        expect(self.page.get_by_text(media_name)).not_to_be_visible()
        Screenshot(self.page).take_screenshot_with_custom("After Remove To Timeline")

    # ------------------------------------------
    # check media in sub-tab
    def check_logo_is_not_shown_image(self):
        # this step can not be shared !
        expect(self.page.locator("//div[contains(@class,'asset-upload')]/div")).to_have_count(1)

    def check_image_is_not_shown_logo(self):
        # this step can not be shared !
        expect(self.page.locator("//div[contains(@class,'asset-upload')]/div")).to_have_count(1)

    # ------------------------------------------
    def click_on_web_and_blog_option(self):
        with self.page.expect_popup() as page2_info:
            self.page.get_by_text("Web & Blogs").click()
            time.sleep(10)
        return page2_info.value

    def check_video_is_displayed_in_tab_name(self, tab_name: StudioSubTab, duration_video: str):
        # this step can not be shared
        self.click_on_tab_name(tab_name.value)
        expect(self.page.get_by_label("Media").locator("div")
               .filter(has_text=re.compile(fr"^{duration_video}$")).nth(2)).to_be_visible()
        Screenshot(self.page).take_screenshot()

    def check_video_is_not_displayed_in_tab_name(self, tab_name: StudioSubTab, duration_video: str):
        self.click_on_tab_name(tab_name.value)
        expect(self.page.get_by_label("Media").locator("div")
               .filter(has_text=re.compile(fr"^{duration_video}$")).nth(2)).not_to_be_visible()
        Screenshot(self.page).take_screenshot()

    def check_remove_video_from_tab_name(self, tab_name: StudioSubTab, duration_video: str):
        self.click_on_tab_name(tab_name.value)
        time.sleep(5)
        self.click_on_remove_button_on_media()
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_label("Media").locator("div")
               .filter(has_text=re.compile(fr"^{duration_video}$")).nth(2)).not_to_be_visible()

    def remove_video_from_tab_name_if_any(self, tab_name: StudioSubTab, duration_video: str):
        self.click_on_tab_name(tab_name.value)
        if self.page.locator("//p[contains(.,'Drag & drop or')]").count() == 0:
            print("Remove Existing Video")
            self.click_on_remove_button_on_media()
            expect(
                self.page.get_by_label("Media").locator("div").filter(has_text=re.compile(fr"^{duration_video}$")).nth(
                    2)).not_to_be_visible()

    def check_video_is_removed_from_tab(self, tab_name: StudioSubTab, duration_video: str):
        self.click_on_tab_name(tab_name.value)
        time.sleep(3)
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_label("Media").locator("div").filter(has_text=re.compile(fr"^{duration_video}$")).nth(
                2)).not_to_be_visible()

    def remove_image_from_tab_name_if_any(self, tab_name: StudioSubTab):
        xpath = "//div[contains(@class,'asset-upload')]/div"
        self.click_on_tab_name(tab_name.value)
        if self.page.locator(xpath).count() == 1:
            self.click_on_remove_button_on_media()
            expect(self.page.locator(xpath)).to_have_count(0)

    def check_image_is_displayed_in_tab_name(self, tab_name: StudioSubTab):
        xpath = "//div[contains(@class,'asset-upload')]/div"
        self.click_on_tab_name(tab_name.value)
        time.sleep(5)
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator(xpath)).to_have_count(1)

    def check_image_is_not_displayed_in_tab_name(self, tab_name: StudioSubTab):
        xpath = "//div[contains(@class,'asset-upload')]/div"
        self.click_on_tab_name(tab_name.value)
        time.sleep(5)
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator(xpath)).to_have_count(0)

    def check_remove_image_from_tab_name(self, tab_name: StudioSubTab):
        xpath = "//div[contains(@class,'asset-upload')]/div"
        self.click_on_tab_name(tab_name.value)
        time.sleep(5)
        self.click_on_remove_button_on_media()
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator(xpath)).to_have_count(0)

    def check_image_is_removed_from_tab(self, tab_name: StudioSubTab):
        self.click_on_tab_name(tab_name.value)
        xpath = "//div[contains(@class,'asset-upload')]/div"
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator(xpath)).to_have_count(0)
