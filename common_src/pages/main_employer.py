import time


class MainEmployerPage:
    def __init__(self, page):
        self.page = page

    def access_story_builder_tab(self):
        self.page.get_by_role("link", name="Story Builder").click()

    def access_story_hub_tab(self):
        self.page.get_by_role("link", name="Story Hub").click()

    def access_creative_studio_tab(self):
        self.page.get_by_role("link", name="Creative Studio").click()

    def access_content_recipes(self):
        self.page.get_by_role("link", name="Content Recipes", exact=True).click()

    def access_url(self, url):
        self.page.goto(url)
