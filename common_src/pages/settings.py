
from playwright.sync_api import expect

from common_src.utils.Screenshot import Screenshot


class SettingsPage:
    def __init__(self, page):
        self.page = page

    # Click Actions
    def click_on_option(self, option_name: str):
        self.page.get_by_text(option_name).click()

    def click_on_add_button(self):
        self.page.get_by_role("button", name="Add").click()

    def enter_template_name(self, name):
        self.page.locator("#name").fill(name)

    def fill_in_template_body(self, body):
        self.page.get_by_label("Rich Text Editor, main").fill(body)

    def delete_invite_adv(self, template_name):
        xpath = f"//p[.='{template_name}']"
        self.page.locator(xpath).hover()
        self.page.get_by_role("button").nth(1).hover()
        self.page.get_by_role("button", name="Delete").click()
        self.page.get_by_role("button", name="OK").click()

    def set_template_as_default(self, template_name):
        xpath01 = f"//p[.='{template_name}']"
        self.page.locator(xpath01).hover()
        self.page.get_by_role("button").nth(1).hover()
        self.page.get_by_role("button", name="Mark as default").click()
        Screenshot(self.page).take_screenshot()

    # Assert
    def check_default_keywords(self):
        expect(self.page.get_by_text("[advocateName]")).to_be_visible()
        expect(self.page.get_by_text("[companyName]")).to_be_visible()
        expect(self.page.get_by_text("[ebName]")).to_be_visible()

    def check_template_shown_on_invite_advocate(self, name):
        expect(self.page.get_by_text(name)).to_be_visible()

    def check_default_is_marked(self, name):
        xpath = f"//div/p[.='{name}']/parent::*/parent::*/*[name()='svg']"
        expect(self.page.locator(xpath)).to_be_visible()

    def check_list_of_invite_adv_templates(self, template_list):
        Screenshot(self.page).take_screenshot()
        for template_name in template_list:
            xpath = f"//p[.='{template_name}']"
            expect(self.page.locator(xpath)).to_be_visible()
