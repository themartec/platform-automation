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

    def click_on_filter_button(self):
        self.page.get_by_text("Filter").click()

    def click_on_apply_button(self):
        self.page.get_by_role("button", name="Apply").click()

    def click_on_clear_all_button(self):
        self.page.get_by_role("button", name="Clear All").click()

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