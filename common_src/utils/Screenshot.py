import time

import allure


class Screenshot:

    def __init__(self, page):
        self.page = page

    def take_screenshot(self):
        png_bytes = self.page.screenshot()
        allure.attach(
            png_bytes,
            name='full page screenshot',
            attachment_type=allure.attachment_type.PNG
        )
        time.sleep(10)

    def take_screenshot_with_custom(self, description):
        png_bytes = self.page.screenshot()
        allure.attach(
            png_bytes,
            name=description,
            attachment_type=allure.attachment_type.PNG
        )
        time.sleep(10)
