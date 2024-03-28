import os
import time

from playwright.sync_api import expect


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


def check_text_is_shown_on_screen(page, text):
    expect(page.get_by_text(text)).to_be_visible()


def check_file_is_downloaded_successfully(file_name_path):
    if os.path.isfile(file_name_path):
        return True
    else:
        print(f"File is NOT existed.")
        return False


def remove_file_name(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"[PRE-CONDITION] The {file_name} file is removed")
    else:
        print(f"[PRE-CONDITION] The {file_name} file does not exist")


def check_button_name_is_disable(page, button_name):
    expect(page.get_by_role("button", name=button_name)).to_be_disabled(timeout=10000)
