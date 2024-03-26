import logging
import os
import time

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, BrowserContext
from configobj import ConfigObj
from utils.init_env import init_url

logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_dotenv()


def write_env_var(env_name):
    config = ConfigObj(".env")
    config.filename = ".env"
    config['test_env'] = env_name
    config.write()


def write_browser_var(browser_type):
    config = ConfigObj(".env")
    config.filename = ".env"
    config['browser_type'] = browser_type
    config.write()


def pytest_addoption(parser):
    parser.addoption("--env_name", action="store")
    parser.addoption("--browser_type", action="store")


def get_env_from_command(request):
    name_value = request.config.option.env_name
    browser_value = request.config.option.browser_type
    if name_value is None:
        # pytest.skip()
        raise Exception('test env is not defined !')
    if browser_value is None:
        browser_value = 'chrome'
    write_env_var(name_value.lower())
    write_browser_var(browser_value.lower())
    time.sleep(5)
    load_dotenv()
    return name_value.lower()


@pytest.fixture(scope="function")
def get_env(request) -> None:
    env_name = os.getenv('test_env')
    return env_name


@pytest.fixture(scope="function")
def get_base_url(request) -> None:
    url = init_url('APP_MARTEC_URL')
    yield url


def common_browser_setup(playwright: Playwright):
    logger.info("[SET UP] Set up browser is called !")
    load_dotenv()
    browser_type = os.getenv('browser_type')
    logger.info(f"    - browser_type: {browser_type}")
    if 'chrome' in browser_type or 'chromium' in browser_type:
        browser = playwright.chromium.launch(headless=False, slow_mo=1500, channel=browser_type)
    else:
        raise Exception('browser type is not configured')
    return browser


@pytest.fixture(scope="function")
def set_up_tear_down(playwright: Playwright, request) -> None:
    load_dotenv()
    env_name = get_env_from_command(request)
    browser = common_browser_setup(playwright)
    context = browser.new_context(storage_state=f"auth_regression_{env_name}.json")
    context.grant_permissions(['clipboard-read', 'clipboard-write'])
    page = context.new_page()
    page.goto(init_url('APP_MARTEC_URL'))
    time.sleep(5)
    yield page

    def teardown():
        browser.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def set_up_tear_down_with_full_configure(playwright: Playwright, request) -> None:
    env_name = get_env_from_command(request)
    browser = common_browser_setup(playwright)
    context = browser.new_context(storage_state=f"auth_regression_{env_name}.json")
    context.grant_permissions(['clipboard-read', 'clipboard-write'])
    page = context.new_page()
    # listen for network event
    page.on("request", lambda request: None)
    page.on("response", lambda response: None)
    page.goto(init_url('APP_MARTEC_URL'))
    time.sleep(5)
    yield page

    def teardown():
        print("Tear down is called !")
        browser.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def set_up_tear_down_without_state(playwright: Playwright, request) -> None:
    load_dotenv()
    browser = common_browser_setup(playwright)
    context = browser.new_context()
    page = context.new_page()
    page.goto(init_url('APP_MARTEC_URL'))
    time.sleep(5)
    yield page

    def teardown():
        print("Tear down is called !")
        browser.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def set_up_tear_down_with_network_profile(playwright: Playwright, request) -> BrowserContext:
    logger.info("[SET UP] Set up browser is called !")
    load_dotenv()
    browser_type = os.getenv('browser_type')
    logger.info(f"    - browser_type: {browser_type}")
    browser = playwright.chromium.launch(headless=True, slow_mo=500, channel='chrome')
    context = browser.new_context()

    yield context

    def teardown():
        browser.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def init_context(playwright: Playwright, request) -> BrowserContext:
    browser = common_browser_setup(playwright)
    context = browser.new_context()
    yield context

    def teardown():
        context.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def init_a_page_with_base_url(playwright: Playwright, request) -> BrowserContext:
    browser = common_browser_setup(playwright)
    context = browser.new_context()
    page = context.new_page()
    page.goto(init_url('APP_MARTEC_URL'))
    yield page

    def teardown():
        print("Tear down is called !")
        browser.close()

    request.addfinalizer(teardown)
