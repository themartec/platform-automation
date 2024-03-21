import time

from playwright.sync_api import expect


class ContentRecipesPage:

    def __init__(self, page):
        self.page = page

    def check_page_title_is_correct(self):
        expect(self.page.get_by_text("Content Recipes").nth(1)).to_be_visible()

    def click_on_one_present_template(self):
        self.page.locator("(//p[.='Hiring'])[1]/parent::div").click()

    def check_ui_upload_dialog(self):
        expect(self.page.get_by_text("Upload your own example")).to_be_visible()
        expect(self.page.get_by_text("LinkedIn, Forbes, Medium URLs")).to_be_visible()
        expect(self.page.locator("#modal").get_by_role("button").first).to_be_visible()
        expect(self.page.get_by_role("button", name="Cancel")).to_be_visible()
        expect(self.page.get_by_role("button", name="Upload", exact=True)).to_be_visible()

    def enter_example_link_to_upload(self, url):
        self.page.locator("//input").fill(url)
        self.page.get_by_role("button", name="Upload", exact=True).click()
        xpath_waiting = "//p[.='Upload']/following-sibling::div/div"
        time.sleep(3)
        expect(self.page.locator(xpath_waiting)).not_to_be_visible(timeout=60000)

    def check_upload_successfully(self, before_size: int):
        warning_xpath = "//label[.='Upload failed, please try again with a different link.']"
        time.sleep(1)
        expect(self.page.locator(warning_xpath)).not_to_be_visible()
        expect(self.page.get_by_text("My Uploads").nth(1)).to_be_visible()
        expect(self.page.locator("//div[.='My Uploads']/following-sibling::div/div")).to_have_count(before_size+1)

    def get_number_example_in_my_upload_list(self):
        return self.page.locator("//div[.='My Uploads']/following-sibling::div/div").count()

    def click_on_close_upload(self):
        self.page.locator("//*[@class='css-1h5x3dy']").click()

