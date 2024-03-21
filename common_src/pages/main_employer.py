import time


class MainEmployerPage:
    def __init__(self, page):
        self.page = page

    def access_story_builder_tab(self):
        self.page.get_by_role("link", name="Story Builder").click()

    def access_story_hub_tab(self):
        self.page.get_by_role("link", name="Story Hub").click()

    def access_creative_studio_tab(self):
        self.page.get_by_role("link", name="Creative Studio").click(timeout=10000)

    def access_content_recipes(self):
        self.page.locator("//a//p[.='Content Recipes']").click()

    def access_library_tab(self):
        self.page.get_by_role("link", name="Library", exact=True).click()

    def access_url(self, url):
        self.page.goto(url)
        time.sleep(3)

    def access_employee_hub(self):
        self.page.get_by_role("link", name="Employee Hub", exact=True).click()

    def access_settings(self):
        self.page.get_by_role("link", name="Settings").click()