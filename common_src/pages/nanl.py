import datetime
import os
import sys
import time
import allure

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.utils.Screenshot import Screenshot


class NoAppNoLoginPage:

    def __init__(self, page):
        self.page = page

    def tick_on_check_box_of_term(self):
        self.page.locator("span").click()

    def click_on_start_button(self):
        self.page.get_by_role("button", name="Get Started").click()

    def click_on_next_button(self):
        self.page.get_by_role("button", name="Next").click()

    def click_on_upload_button(self):
        self.page.get_by_text("Upload Video").click()

    def set_file_name_to_upload(self, file_name) -> int:
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_text("Upload Video").click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_name)
        now = datetime.datetime.now()
        start_time = now.strftime("%H:%M:%S")
        print(f"[Upload Process] start_time: {start_time}")
        # Wait for maximum 3 minutes
        time_break = -1
        for i in range(1, 240):  # test with 2 minutes
            break_event_element = self.page.locator("//p[contains(.,' MB')]").count()
            if break_event_element == 1:
                time_break = i * 0.5
                print(f"[Upload Process] Upload is completed. Time break: {time_break} (second)")
                Screenshot(self.page).take_screenshot()
                break
            time.sleep(0.5)
        print(f"[Upload Process] time_break: {time_break}")
        return time_break
