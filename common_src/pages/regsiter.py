import re
import time

from playwright.sync_api import expect

from common_src.utils.Screenshot import Screenshot
from common_src.pages.main_employer import MainEmployerPage


class RegisterPage:
    def __init__(self, page):
        self.page = page

    def enter_register_data(self, email: str, password: str):
        self.page.get_by_placeholder("Your Email").click()
        self.page.get_by_placeholder("Your Email").fill(email)
        self.page.locator("#password").click()
        self.page.locator("#password").fill(password)
        self.page.locator("#repeatPassword").click()
        self.page.locator("#repeatPassword").fill(password)

    def check_on_agreement_checkbox(self):
        self.page.locator("div").filter(
            has_text=re.compile(r"^I have read and agreed with the Terms of Use and Privacy Policy\.$")).locator(
            "div span").click()
        Screenshot(self.page).take_screenshot()

    def click_on_sign_up_button(self):
        self.page.get_by_role("button", name="Sign Up").click()

    def enter_profile_data(self, first_name, last_name, role, department, language):
        self.page.locator("#firstName").click()
        self.page.locator("#firstName").fill(first_name)
        self.page.locator("#lastName").fill(last_name)
        self.page.locator("//div[.='Department']/following-sibling::div").click()
        self.page.get_by_text(department, exact=True).click()
        self.page.locator("#role").fill(role)
        self.page.locator("div").filter(has_text=re.compile(r"^Select$")).nth(3).click()
        self.page.get_by_text(language, exact=True).click()
        Screenshot(self.page).take_screenshot()

    def upload_profile_image(self, file_name):
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("img").nth(2).click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_name)

    def click_on_create_profile_button(self):
        self.page.get_by_role("button", name="create profile").click()

    def click_on_skip_button_at_welcome_page(self):
        xpath = "//p[contains(.,'Skip')]/following-sibling::button"
        self.page.locator(xpath).click()
        time.sleep(3)

    # Assert
    def check_warning_texts(self):
        Screenshot(self.page).take_screenshot()
        expect(self.page.get_by_text("First name is required")).to_be_visible()
        expect(self.page.get_by_text("Last name is required")).to_be_visible()
        expect(self.page.get_by_text("Role name is required")).to_be_visible()

    def check_welcome_after_register_successfully(self):
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator("//p[contains(.,'Welcome')]")).to_be_visible()

    # def check_my_stories_is_shown_as_default(self):
    #     Screenshot(self.page).take_screenshot()
    #     expect(self.page.locator("//div[@type='adv']//p[contains(.,'My Stories')]")).to_be_visible()

    def check_sign_up_button_is_disable(self):
        expect(self.page.locator("//p[contains(.,'Sign Up')]/parent::*")).to_be_disabled()

    def check_upload_profile_image_is_successful(self):
        expect(self.page.get_by_role("img", name="Photo Preview")).to_be_visible()
        expect(self.page.get_by_role("button").first).to_be_visible()

    def check_register_page_shown(self):
        xpath = "//p[.='EMAIL']"
        expect(self.page.locator(xpath)).to_be_visible()
        register_url = self.page.evaluate('() => document.URL')
        assert 'advocate/register' in register_url

