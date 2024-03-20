def get_clipboard_data(page):
    # Content must be granted for permission
    clipboard_text = page.evaluate('() => navigator.clipboard.readText()')
    return clipboard_text


def refresh_page(page):
    page.keyboard.press('F5', delay=3000)


def enter_text(page, field_name, content):
    page.get_by_placeholder(field_name).fill(content)


def click_on_button_name(page, button_name):
    page.get_by_role("button", name=button_name).click()