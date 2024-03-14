import re
import time

from playwright.sync_api import expect

from common_src.utils.Screenshot import Screenshot


class EmployeeHubPage:

    def __init__(self, page):
        self.page = page

    def check_table_column_name_is_correct(self):
        element = self.page.get_by_role("table")
        expect(element).to_contain_text("Advocate")
        expect(element).to_contain_text("Status")
        expect(element).to_contain_text("Role")
        expect(element).to_contain_text("Communities")
        expect(element).to_contain_text("Email")

    def check_account_name_has_correct_info_field(self, expected_account_info: list):
        # Detail order of expected_account_info
        # Adv name, Status, Role, Communities, Email
        Screenshot(self.page).take_screenshot()
        xpath = f"//div[@class='tr rdt_TableRow' and contains(.,'{expected_account_info[0]}')]/div"
        row_info = self.page.locator(xpath)
        # Checkbox Exist
        expect(self.page.locator(f"//div[@class='tr rdt_TableRow' and contains(.,'{expected_account_info[0]}')]/div["
                                 f"1]//input")).not_to_be_checked()
        # Check Status
        expect(row_info.nth(2)).to_have_text(expected_account_info[1])
        # Check Role
        expect(row_info.nth(3)).to_have_text(expected_account_info[2])
        # Check Communities
        expect(row_info.nth(4)).to_have_text(expected_account_info[3])
        # Check Email
        expect(row_info.nth(5)).to_have_text(expected_account_info[4])
        # Check three dot button
        expect(self.page.locator("//div[@class='tr rdt_TableRow' and contains(.,'Test ADV 01')]/div[7]//button[@type "
                                 "= 'button']")).to_be_visible()
        # Check avatar
        expect(self.page.get_by_role("cell", name=expected_account_info[0]).get_by_role("img")).to_be_visible()

    # MAIN PAGE
    def click_on_filter_button(self):
        self.page.get_by_text("Filter").click()

    def click_on_apply_button(self):
        self.page.get_by_role("button", name="Apply").click()

    def click_on_clear_all_button(self):
        self.page.get_by_role("button", name="Clear All").click()

    def click_on_active_people_button(self):
        self.page.get_by_role("button", name="activate people").click()

    def click_on_direct_invite_option(self):
        self.page.get_by_text("Direct InviteOutreach people").click()

    def click_on_adv_name_in_list(self, adv_name):
        self.page.get_by_text(adv_name).click()

    def click_on_adv_details_tab(self):
        self.page.get_by_text("Advocate Details").nth(1).click()

    def search_by_name(self, search_name):
        self.page.get_by_placeholder("Search for an advocate, a").fill(search_name)

    def remove_filter(self):
        self.click_on_filter_button()
        self.click_on_clear_all_button()
        self.click_on_apply_button()
        time.sleep(3)

    def set_filter_by_list(self, info_list: list):
        for status in info_list:
            self.page.locator(f"//p[.='{status}']/preceding-sibling::span").click()
            expect(self.page.locator(f"//p[.='{status}']/preceding-sibling::input")).to_be_checked()

    def set_communities_with_element_in_order(self, order: int):
        # This feature has not be stable yet

        xpath = "//*[.='Community']/following-sibling::div[.='Select']"
        self.page.locator(xpath).click()
        time.sleep(1)
        self.page.locator(f"#react-select-33-option-{order}").click()
        Screenshot(self.page).take_screenshot()

    def click_on_back_button_from_adv_details(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Advocate Details24$")).get_by_role("button").click()

    def hover_on_three_dot_button_and_delete(self):
        self.page.locator("//button[@type='button']").hover()
        self.page.get_by_role("button", name="Delete").click()

    # ACTIVE PEOPLE
    def click_on_copy_invite_link_button(self):
        # need to grant permission of clipboard
        self.page.locator("//span[.='copy invite link']").click()
        time.sleep(3)
        Screenshot(self.page).take_screenshot()

    def click_on_back_button_from_active_people_page(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Activate People$")).get_by_role("button").click()
        expect(self.page.locator("#root")).to_contain_text("Employee Hub")

    def get_clipboard_data(self):
        # Content must be granted for permission
        clipboard_text = self.page.evaluate('() => navigator.clipboard.readText()')
        return clipboard_text

    # --------------------------------------------------------------
    def check_filter_is_correct(self, expected_tex_list: list):
        Screenshot(self.page).take_screenshot()
        xpath = f"//div[@class='tr rdt_TableRow']"
        time.sleep(5)
        row_info = self.page.locator(xpath)
        for i in range(0, row_info.count()):
            print(f"row_info.nth({i}): {row_info.nth(i).text_content()}")
            is_correct = False
            for tx in expected_tex_list:
                print(F"'{tx.lower()}: {tx.lower() in row_info.nth(i).text_content().lower()}'")
                if tx.lower() in row_info.nth(i).text_content().lower():
                    is_correct = True
            assert is_correct is True

    def check_star_is_shown(self, advocate_name):
        expect(self.page.get_by_role("cell", name=advocate_name).locator("path")).to_be_visible()

    def check_options_are_reset(self, status_name):
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator(f"//p[.='{status_name}']/preceding-sibling::input")).not_to_be_checked()
        expect(self.page.locator(f"//p[.='Star Advocate']/preceding-sibling::input")).not_to_be_checked()
        expect(self.page.locator(f"#react-select-33-option-0")).not_to_be_visible()

    def check_filter_result_as_empty(self):
        expect(self.page.get_by_text("Click here to add an advocate")).to_be_visible()

    def check_adv_overview_info(self, adv_name, adv_role):
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator("#root")).to_contain_text(adv_name)
        expect(self.page.locator("#root")).to_contain_text(adv_role)

    def check_adv_details(self, user_info):
        # ["Test", f"Dummy {random_num}", "Advocacy Dummy", "Engineering", "English"]
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator("#firstName")).to_have_value(user_info[0])
        expect(self.page.locator("#lastName")).to_have_value(user_info[1])
        expect(self.page.locator("#role")).to_have_value(user_info[2])
        expect(self.page.locator("div").filter(has_text=re.compile(fr"^{user_info[3]}$")).nth(3)).to_be_visible()
        expect(self.page.get_by_text(user_info[4])).to_be_visible()
        expect(self.page.locator("//input[@id='email']")).to_have_value(user_info[5])

    # Direct Invite
    def click_on_save_template_button(self):
        self.page.get_by_role("button", name="Save Template").click()

    def enter_new_template_name(self, template_name):
        self.page.get_by_placeholder("Your template name").fill(template_name)
        self.page.get_by_role("button", name="save", exact=True).click()

    def select_email_template_name(self, template_name):
        self.page.get_by_role("option", name=template_name).click()

    def check_body_email_template(self, body):
        (expect(self.page.get_by_label("Rich Text Editor, main"))
         .to_contain_text(body))

    def update_template_with_content(self, old_content, new_content):
        self.page.get_by_label("Rich Text Editor, main").fill(
            f"{new_content}")
        Screenshot(self.page).take_screenshot()

    def check_new_template_is_shown_in_direct_invite(self, name):
        expect(self.page.get_by_text(name)).to_be_visible()

