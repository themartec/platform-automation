import re
import time

from playwright.sync_api import expect

from common_src.utils.Screenshot import Screenshot


class RegisterPage:
    def __init__(self, page):
        self.page = page

    def enter_password(self, password: str):
        self.page.locator("#password").click()
        self.page.locator("#password").fill(password)
        self.page.locator("*:is(#repeatPassword, #confirmPassword)").click()
        self.page.locator("*:is(#repeatPassword, #confirmPassword)").fill(password)

    def enter_register_data(self, email: str, password: str):
        self.page.get_by_placeholder("Your Email").click()
        self.page.get_by_placeholder("Your Email").fill(email)
        self.enter_password(password)

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

    def enter_profile_data_for_team_invite_flow(self, first_name, last_name,):
        self.page.locator("*:is(#firstName, #firstname)").click()
        self.page.locator("*:is(#firstName, #firstname)").fill(first_name)
        self.page.locator("*:is(#lastName, #lastname)").fill(last_name)
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

    def check_register_page_shown(self, role_type):
        Screenshot(self.page).take_screenshot()
        xpath = "//p[.='EMAIL']"
        expect(self.page.locator(xpath)).to_be_visible()
        register_url = self.page.evaluate('() => document.URL')
        if 'advocate' in role_type.lower():
            assert 'advocate/register' in register_url
            expect(self.page.locator("//p[.='CREATE PASSWORD']/following-sibling::div/input")).to_be_visible()
            expect(self.page.locator("//p[contains(.,'I have read and agreed with the')]")).to_be_visible()
        elif 'employer' in role_type.lower() or 'recruiter' in role_type.lower():
            assert 'employer/register' in register_url
            expect(self.page.locator("//p[.='CREATE A PASSWORD']/following-sibling::div/input")).to_be_visible()
        else:
            raise Exception(f"Un-support role type as {role_type}")

        expect(self.page.locator("//p[.='REPEAT PASSWORD']/following-sibling::div/input")).to_be_visible()
        expect(self.page.locator("//p[.='Sign Up']")).to_be_visible()

    def check_error_email_taken(self):
        time.sleep(3)
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator("//p[.='Email already taken']")).to_be_visible(timeout=10000)

    def check_default_user_info_are_shown(self, email_address, company_name):
        expect(self.page.locator(f"//*[@value='{email_address}']")).to_be_visible()
        expect(self.page.locator(f"//*[@value='{company_name}']")).to_be_visible()

    def check_expired_error_message(self):
        expect(self.page.locator("//p[.='Invitation expired']")).to_be_visible(timeout=20000)
        Screenshot(self.page).take_screenshot()

    def check_email_and_company_name(self, email_address, company_name):
        expect(self.page.locator(f"//*[@value='{email_address}']")).to_be_visible()
        expect(self.page.locator(f"//*[@value='{company_name}']")).to_be_visible()

    def click_on_complete_registration(self):
        self.page.locator("//button[.='Complete Registration']").click()
        time.sleep(5)
        Screenshot(self.page).take_screenshot()
