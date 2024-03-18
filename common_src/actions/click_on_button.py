
def click_on_button_name(page, button_name):
    page.get_by_role("button", name=button_name).click()