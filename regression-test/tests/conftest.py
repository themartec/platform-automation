import os
import time

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, BrowserContext

load_dotenv()


def match_env_for_studio(test_env: str):
    if test_env == "1":
        print(f"[Pre-Condition] TEST_ENV=STAGING")
        base_url = "https://studiostaging.themartec.com/"
    elif test_env == "2":
        print(f"[Pre-Condition] TEST_ENV=DEV")
        base_url = "https://studiodev.themartec.com/"
    else:
        print(f"[Pre-Condition] TEST_ENV=PROD")
        base_url = "https://studio.themartec.com/"
    return base_url


def match_env(test_env: str):
    if test_env == "1":
        print(f"TEST_ENV=STAGING")
        base_url = "https://appstaging.themartec.com/"
    elif test_env == "2":
        print(f"TEST_ENV=DEV")
        base_url = "https://appdev.themartec.com/"
    else:
        print(f"TEST_ENV=PROD")
        base_url = "https://app.themartec.com/"
    return base_url


def pytest_addoption(parser):
    parser.addoption("--env_id", action="store")


def get_env_from_command(request):
    name_value = request.config.option.env_id
    if name_value is None:
        pytest.skip()
    return name_value


@pytest.fixture(scope="function")
def get_env_id(request) -> str:
    test_env_id = get_env_from_command(request)
    return test_env_id


@pytest.fixture(scope="function")
def set_up_tear_down(playwright: Playwright, request) -> None:
    test_env_id = get_env_from_command(request)
    print("Set up is called !")
    # load_dotenv()
    # test_env_id = os.getenv('TEST_ENV')
    url = match_env(test_env_id)
    print(f"TEST ENV: {url}")
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    # huong.trinh@themartec.com
    if test_env_id == "1":
        context = browser.new_context(storage_state="auth_regression_staging.json")
    elif test_env_id == "2":
        context = browser.new_context(storage_state="auth_regression_dev.json")
    else:
        context = browser.new_context()
    context.grant_permissions(['clipboard-read', 'clipboard-write'])
    page = context.new_page()
    page.goto(url)
    time.sleep(5)
    yield page

    def teardown():
        print("Tear down is called !")
        browser.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def set_up_tear_down_without_state(playwright: Playwright, request) -> None:
    test_env_id = get_env_from_command(request)
    print("Set up is called !")
    # load_dotenv()
    # test_env_id = os.getenv('TEST_ENV')
    url = match_env(test_env_id)
    print(f"TEST ENV: {url}")
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    time.sleep(5)
    yield page

    def teardown():
        print("Tear down is called !")
        browser.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="package")
def get_base_url(request) -> None:
    test_env_id = get_env_from_command(request)
    url = match_env(test_env_id)
    yield url


@pytest.fixture(scope="package")
def get_base_studio_url(request) -> None:
    test_env_id = get_env_from_command(request)
    url = match_env_for_studio(test_env_id)
    yield url


@pytest.fixture(scope="function")
def get_content_id(request) -> None:
    test_env_id = get_env_from_command(request)
    if test_env_id == "1":
        content_id = "7efad3d4-6e24-4bf7-9c13-d7072a27019a"
    elif test_env_id == "2":
        content_id = "ac79287c-b0d6-4018-b902-57e575983428"
    else:
        content_id = ""
    yield content_id


@pytest.fixture(scope="function")
def remove_and_get_tested_download_files(request) -> str:
    file_name = "How do you stay motivated and productive while working remotely.mp4"
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"[PRE-CONDITION] The {file_name} file is removed")
    else:
        print(f"[PRE-CONDITION] The {file_name} file does not exist")
    return file_name


@pytest.fixture(scope="function")
def get_media_url(request) -> str:
    test_env_id = get_env_from_command(request)
    if test_env_id == "1":
        base_media_url = os.getenv("BASE_MEDIA_URL_STG")
    elif test_env_id == "2":
        base_media_url = os.getenv("BASE_MEDIA_URL_DEV")
    else:
        base_media_url = ""
    yield base_media_url


@pytest.fixture(scope="function")
def set_up_tear_down_with_network_profile(playwright: Playwright, request) -> BrowserContext:
    test_env_id = get_env_from_command(request)
    print("Set up is called !")
    url = match_env(test_env_id)
    print(f"TEST ENV: {url}")
    browser = playwright.chromium.launch(headless=False, slow_mo=500, channel="chrome")
    context = browser.new_context()

    yield context

    def teardown():
        print("Tear down is called !")
        browser.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def init_context(playwright: Playwright, request) -> BrowserContext:
    test_env_id = get_env_from_command(request)
    print("Set up is called !")
    # load_dotenv()
    # test_env_id = os.getenv('TEST_ENV')
    url = match_env(test_env_id)
    print(f"TEST ENV: {url}")
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    yield context

    def teardown():
        print("Tear down is called !")
        context.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def init_context_with_base_url(playwright: Playwright, request) -> BrowserContext:
    test_env_id = get_env_from_command(request)
    print("Set up is called !")
    # load_dotenv()
    # test_env_id = os.getenv('TEST_ENV')
    url = match_env(test_env_id)
    print(f"TEST ENV: {url}")
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    yield page

    def teardown():
        print("Tear down is called !")
        context.close()

    request.addfinalizer(teardown)
