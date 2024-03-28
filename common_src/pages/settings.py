import json
import logging
import time

from playwright.sync_api import expect
from common_src.utils.Screenshot import Screenshot
from utils.init_env import init_url

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SettingsPage:
    def __init__(self, page):
        self.page = page

    # Click Actions
    def click_on_option(self, option_name: str):
        self.page.get_by_text(option_name, exact=True).click()

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

    def click_on_team_option(self):
        self.page.locator("//p[.='Team']").click()

    def select_role_to_invite(self, role):
        self.page.get_by_text('Role').click()
        self.page.locator(f"//div[.='{role}']").click()

    def click_on_invite_link_button(self):
        self.page.get_by_text("Copy Invite Link").click()

    def click_on_close_invite_team_member_popup(self):
        time.sleep(2)
        self.page.locator("//button[contains(@class,'close')]").click()

    def enter_email_address_to_invite(self, email_address):
        (self.page.get_by_placeholder("Please enter your email")
         .fill(email_address))
        Screenshot(self.page).take_screenshot()

    def click_on_invite_button_in_popup(self):
        self.page.get_by_role("button", name="invite", exact=True).click()

    def get_invitation_token(self) -> str:
        with self.page.expect_response("**/team/getInvitedTeam") as response_info:
            self.click_on_invite_button_in_popup()
        response = json.loads(response_info.value.body())
        invite_link = response['data']['result'][0]['invite_link']
        logger.info(f" - response: {response}")
        logger.info(f" - response advocateInviteLink: {invite_link}")
        return invite_link

    def check_invited_tab_with_status_and_email_in_team(self, email_address, status):
        expect(self.page.locator("#root")).to_contain_text(status)
        expect(self.page.locator("#root")).to_contain_text(email_address)

    def check_admin_tab_show_added_admin_info(self, email_address, admin_name):
        expect(self.page.locator("#root")).to_contain_text(admin_name)
        expect(self.page.locator("#root")).to_contain_text(email_address)
        assert f"{init_url('MEDIA_URL')}" in self.page.locator('(//img)[2]').element_handle().get_attribute('src')
