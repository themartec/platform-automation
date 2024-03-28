import json
import logging
import re
import time

from playwright.sync_api import expect
from common_src.utils.Screenshot import Screenshot

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
        expect(self.page.locator(f"//div[@class='tr rdt_TableRow' and contains(.,'{expected_account_info[0]}')]/div["
                                 f"7]//button[@type "
                                 "= 'button']")).to_be_visible()
        # Check avatar
        expect(self.page.get_by_role("cell", name=expected_account_info[0]).get_by_role("img")).to_be_visible()

    # MAIN PAGE
    def click_on_filter_button(self):
        self.page.get_by_text("Filter").click()

    def click_on_apply_button(self):
        self.page.locator("//button[contains(.,'Apply')]").click()

    def click_on_clear_all_button(self):
        self.page.get_by_role("button", name="Clear All").click()

    def click_on_active_people_button(self):
        self.page.get_by_role("button", name="activate people").click()

    def click_on_direct_invite_option(self):
        self.page.get_by_text("Direct InviteOutreach people").click()

    def click_on_activate_people_option(self, option_name):
        self.page.get_by_text(option_name).click()

    def click_on_adv_name_in_list(self, adv_name):
        self.page.get_by_text(adv_name).click()

    def perform_action_adv_with_info_and_return_name(self, button_type, prefix_name, status: str, order: int):
        base_xpath = (f"(//div[contains(@class,'infinite-scroll-component')]/div[@role='row']"
                      f"//p[.='{status}'])[{order}]/parent::div/parent::div")
        logger.info(f"[Debug] base_xpath: {base_xpath}")
        if self.page.locator(base_xpath).count() > 0:
            adv_name_xpath = f"{base_xpath}//div[contains(.,'{prefix_name}')]"
            three_dot_xpath = f"{base_xpath}/div[last()]//button[contains(@class,'ellipsis-button')]"
            button_xpath = f"{base_xpath}/div[last()]//button[.='{button_type}']"
            adv_full_name = self.page.locator(adv_name_xpath).nth(1).text_content()
            logger.info(f"[Debug] button_xpath: {button_xpath}")
            logger.info(f"[Debug] three_dot_xpath: {three_dot_xpath}")
            self.page.locator(three_dot_xpath).hover()
            self.page.locator(button_xpath).click()
            if 'delete' in button_type.lower():
                self.page.get_by_role("button", name="OK").click()
            return adv_full_name
        else:
            raise Exception(f"Advocate with status {status} is not exist")

    def click_on_adv_details_tab(self):
        self.page.get_by_text("Advocate Details").nth(1).click()

    def search_by_name(self, search_name):
        self.page.get_by_placeholder("Search for an advocate, a").fill(search_name)
        self.page.get_by_placeholder("Search for an advocate, a").press("Enter")
        time.sleep(3)

    def remove_filter(self):
        self.click_on_filter_button()
        self.click_on_clear_all_button()
        self.click_on_apply_button()
        time.sleep(3)

    def set_filter_by_list_employee_hub(self, filter_stype: str, info_list: list):
        self.page.locator(f"//p[.='Employee Hub']/following-sibling::div/p[.='{filter_stype}']").click()
        for info in info_list:
            self.page.locator(f"//div[.='{info}']/span").click()
            expect(self.page.locator(f"//div[.='{info}']/input")).to_be_checked()
        if 'Select All' not in info_list:
            expect(self.page.locator("form")).to_contain_text(str(len(info_list)))

    def set_filter_by_list_custom_field(self, filter_stype: str, info_list: list):
        self.page.locator(f"//p[.='Custom Fields']/following-sibling::div/p[.='{filter_stype}']").click()
        for info in info_list:
            self.page.locator(f"//div[.='{info}']/span").click()
            expect(self.page.locator(f"//div[.='{info}']/input")).to_be_checked()
        if 'Select All' not in info_list:
            expect(self.page.locator("form")).to_contain_text(str(len(info_list)))

    def set_communities_with_element_in_order(self, order: int):
        # This feature has not be stable yet

        xpath = "//*[.='Community']/following-sibling::div[.='Select']"
        self.page.locator(xpath).click()
        time.sleep(1)
        self.page.locator(f"#react-select-33-option-{order}").click()
        Screenshot(self.page).take_screenshot()

    def click_on_back_button_from_adv_details(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Advocate Details$")).get_by_role("button").click()

    def hover_on_three_dot_button_and_delete(self):
        self.page.locator("//button[@type='button']").hover()
        self.page.get_by_role("button", name="Delete").click()

    # ACTIVE PEOPLE
    def click_on_copy_invite_link_button(self):
        # need to grant permission of clipboard
        time.sleep(5)
        self.page.locator("//div[.='copy invite link']").click()
        Screenshot(self.page).take_screenshot()

    def click_on_back_button_from_active_people_page(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Activate People$")).get_by_role("button").click()
        expect(self.page.locator("#root")).to_contain_text("Employee Hub")

    def get_clipboard_data(self):
        # Context must be granted for permission
        clipboard_text = self.page.evaluate('() => navigator.clipboard.readText()')
        return clipboard_text

    # --------------------------------------------------------------
    def check_filter_is_correct(self, filtered_content: list):
        Screenshot(self.page).take_screenshot()
        xpath = f"//div[@class='tr rdt_TableRow']"
        time.sleep(5)
        row_info = self.page.locator(xpath)
        logger.info(f" - filtered_content: {filtered_content}")
        for i in range(0, row_info.count()):
            logger.info(f"    - row_info.nth({i}): {row_info.nth(i).text_content()}")
            is_correct = False
            current_row_content = row_info.nth(i).text_content().lower()
            for tx in filtered_content:
                tx = tx.lower()
                logger.info(F"    - check row to contains '{tx}': {tx in current_row_content}'")
                if tx in current_row_content:
                    is_correct = True
            assert is_correct is True

    def check_content_is_existed_in_list(self, filter_content: str):
        Screenshot(self.page).take_screenshot()
        xpath = f"//div[@class='tr rdt_TableRow']"
        time.sleep(5)
        row_info = self.page.locator(xpath)
        is_correct = False

        for i in range(0, row_info.count()):
            current_row_content = row_info.nth(i).text_content().lower()
            if filter_content.lower() in current_row_content:
                # logger.info(f"    - row_info.nth({i}): {row_info.nth(i).text_content()}")
                # logger.info(F"    - check for '{content.lower()}: {content.lower() in current_row_content}'")
                is_correct = True
                logger.info(f"Found content '{filter_content}' at row {i}")
                break
        assert is_correct is True

    def check_star_is_shown(self, advocate_name):
        expect(self.page.get_by_role("cell", name=advocate_name).locator("path")).to_be_visible()

    def check_options_are_reset(self, status_name):
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator(f"//div[.='{status_name}']/input")).not_to_be_checked()

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

    def update_template_with_content(self, new_content):
        self.page.get_by_label("Rich Text Editor, main").fill(
            f"{new_content}")
        Screenshot(self.page).take_screenshot()

    def check_new_template_is_shown_in_direct_invite(self, name):
        expect(self.page.get_by_text(name)).to_be_visible()

    def check_adv_name_with_status_visible_in_list(self, status, adv_full_name):
        Screenshot(self.page).take_screenshot()
        expect(self.page.locator(f"//p[.='{status}']")).to_be_visible(timeout=60000)
        expect(self.page.get_by_text(adv_full_name)).to_be_visible()

    def filter_single_by_status(self, status):
        self.click_on_filter_button()
        (self.page.locator("div").filter(has_text=re.compile(r"^Advocate Status$"))
         .get_by_role("paragraph").click())
        self.page.get_by_text(status).click()
        self.page.get_by_role("button", name="Apply 1 Filters").click()

    def enter_email_address_direct_invite(self, email_address):
        self.page.get_by_placeholder("Email").fill(email_address)
        Screenshot(self.page).take_screenshot()
        self.page.get_by_placeholder("Email").press("Enter")

    def click_on_send_invite_in_direct_invite(self):
        with self.page.expect_response("**/people-invitation/send-email") as response_info:
            self.page.get_by_role("button", name="Send invite").click()
        response = json.loads(response_info.value.body())
        advocateInviteLink = response['data']['advocateInviteLink'][0]
        logger.info(f" - response: {response}")
        logger.info(f" - response advocateInviteLink: {advocateInviteLink}")
        return advocateInviteLink

    def resend_invite(self):
        self.page.locator("//button[@type='button']").hover()
        self.page.get_by_role("button", name="Resend Invite").click()
        time.sleep(5)

    def check_filter_with_selecting_all(self):
        Screenshot(self.page).take_screenshot()
        xpath = "//div[.='Select All']/following-sibling::div//input"
        element_list = self.page.locator(xpath)
        # logger.info(f"element_list: {element_list.count()}")
        for i in range(1, element_list.count()):
            txt = self.page.locator(f"(//div[.='Select All']/following-sibling::div//div)[{i}]").text_content()
            # logger.info(f"text: {txt}")
            expect(self.page.locator(f"({xpath})[{i}]")).to_be_checked()

    def search_in_filter(self, search_content):
        self.page.get_by_placeholder("Search Filter…").fill(search_content)

    def check_search_in_filter(self, filter_section, search_content):
        expect(self.page.locator("div").filter(has_text=re.compile(fr"^{search_content}$"))).to_be_visible()
        expect(self.page.locator("#modal").get_by_text(filter_section)).to_be_visible()
        expect(self.page.get_by_text(search_content).nth(1)).to_be_visible()

    def check_template_is_saved(self, template_name):
        expect(self.page.get_by_text("Your template has been")).to_be_visible()
        expect(self.page.get_by_text(template_name)).to_be_visible()

    def create_own_template(self):
        self.page.locator("div").filter(has_text=re.compile(r"^Create Own Template$")).get_by_role(
            "img").nth(1).click()

    def check_copy_message_work(self, clipboard_content, marked_text):
        current_content = self.page.get_by_label("Rich Text Editor, main").text_content()
        intersection = current_content.replace(clipboard_content, "")
        assert marked_text in intersection

    def download_template_from_bulk_upload(self, file_name):
        with self.page.expect_download(timeout=0) as download_info:
            self.page.get_by_role("button", name="Download Template").click()
        download = download_info.value
        download.save_as(file_name)
        time.sleep(5)
        return file_name

    def upload_a_template_file_for_bulk_upload(self, file_name):
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator("div").filter(has_text=re.compile(r"^Drag or Click to upload a file$")).nth(2).click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_name)
        time.sleep(5)

    def check_bulk_upload(self):
        expect(self.page.locator("div").filter(has_text=re.compile(r"^email$"))).to_be_visible()
        expect(self.page.locator("div").filter(has_text=re.compile(r"^first_name$"))).to_be_visible()
        expect(self.page.locator("div").filter(has_text=re.compile(r"^last_name$"))).to_be_visible()
        expect(self.page.locator("div").filter(has_text=re.compile(r"^department$"))).to_be_visible()

    def select_email_column_in_bulk_upload(self):
        self.page.locator("div").filter(has_text=re.compile(r"^email$")).locator("span").click()

    def select_all_email_address_in_bulk_upload(self):
        self.page.locator("//p[.='Select All']/preceding-sibling::span").click()

    def checkbox_email_address_as_action(self, email_address, action_type):
        self.page.locator(f"//p[.='{email_address}']/preceding-sibling::span").click()
        self.page.get_by_role("button", name=action_type).click()
        Screenshot(self.page).take_screenshot()
        time.sleep(5)

    def uncheck_email_address(self, email_address):
        if self.page.locator(f"//p[.='{email_address}']/preceding-sibling::input").is_checked():
            self.page.locator(f"//p[.='{email_address}']/preceding-sibling::span").click()

    def click_on_back_button_from_screen_name(self, screen_name):
        (self.page.locator("div").filter(has_text=re.compile(fr"^{screen_name}$"))
         .get_by_role("button").click())
