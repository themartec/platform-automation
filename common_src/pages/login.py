class LoginPage:
    def __init__(self, page):
        self.page = page

    def enter_username_password(self, username: str, password: str):
        self.page.locator("#email").click()
        self.page.locator("#email").fill(username)
        self.page.locator("#password").click()
        self.page.locator("#password").fill(password)
        self.page.get_by_role("button", name="Log in").click()
