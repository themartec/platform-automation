from playwright.sync_api import expect

from common_src.utils.Screenshot import Screenshot


class LoginPage:
    def __init__(self, page):
        self.page = page

    def check_ui_is_correct(self):
        expect(self.page.get_by_text("Log in").first).to_be_visible()
        expect(self.page.get_by_text("EMAIL")).to_be_visible()
        expect(self.page.get_by_text("PASSWORD", exact=True)).to_be_visible()
        expect(self.page.get_by_role("link", name="Forgot Password?")).to_be_visible()
        expect(self.page.get_by_role("link", name="Or log in with SSO")).to_be_visible()

    def check_login_is_successful(self):
        expect(self.page.get_by_role("link", name="Content Recipes", exact=True)).to_be_visible()

    def check_login_is_unsuccessful_as_wrong_username(self):
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator("div").filter(has_text="errorYour email or password is incorrect").nth(
            1)).to_be_visible()

    def check_login_is_unsuccessful_as_wrong_format(self):
        expect(self.page.get_by_text("Please enter a valid email")).to_be_visible()

    def enter_username_password(self, username: str, password: str):
        self.page.locator("#email").click()
        self.page.locator("#email").fill(username)
        self.page.locator("#password").click()
        self.page.locator("#password").fill(password)
        self.page.get_by_role("button", name="Log in").click()

    def check_login_successfully_for_ba_portal(self):
        expect(self.page.locator("(//p[.='My Stories'])[2]")).to_be_visible(timeout=10000)
