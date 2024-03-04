import os
import re
import time
import cv2
from playwright.sync_api import expect


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
        self.page.locator("(//div[contains(@class,'close-bock-icon')])[2]").click()

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

    def check_file_is_downloaded_successfully(self, file_name_path, expected_file_size: float, expected_file_dimension):
        if os.path.isfile(file_name_path):
            file_size = round(float(os.path.getsize(file_name_path) / 1000000), 1)
            file_dimension = self.get_file_dimension(file_name_path)
            print(f"    - file_name_path: {file_name_path}")
            print(f"    - file_size: {file_size}")
            print(f"    - file_dimensions: {file_dimension}")
            if file_size == round(float(expected_file_size), 1) and expected_file_dimension == file_dimension:
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
        self.page.locator("div").filter(has_text=re.compile(r"^Brand$")).click()

    def click_on_edit_template(self, image_dir):
        xpath = f"//p[.='Templates']/following-sibling::div[2]//div[@src='{image_dir}']"
        self.page.locator(xpath).hover()
        self.page.locator(".pencil-wrapper > svg").click()

    # Video Library ------------------------------------
    def access_video_library_tab(self):
        self.page.get_by_text("Video Library").click()

    def click_on_web_and_blogs(self):
        with self.page.expect_popup() as page2_info:
            self.page.get_by_text(":9Web & BlogsWebsite, Embed").click()
        return page2_info.value
