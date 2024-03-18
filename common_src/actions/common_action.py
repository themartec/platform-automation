def get_clipboard_data(page):
    # Content must be granted for permission
    clipboard_text = page.evaluate('() => navigator.clipboard.readText()')
    return clipboard_text


def refresh_page(page):
    page.keyboard.press('F5', delay=3000)
