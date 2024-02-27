import os
import time

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect

from src.brand_kit import BrandKit


def match_env(test_env: str):
    if test_env == "1":
        print(f"TEST_ENV=STAGING")
        base_url = "https://apistaging.themartec.com/"
    elif test_env == "2":
        print(f"TEST_ENV=DEV")
        base_url = "https://apidev.themartec.com/"
    else:
        print(f"TEST_ENV=PROD")
        base_url = ""
    return base_url


@pytest.fixture(scope="function")
def set_up_tear_down(request) -> str:
    pass


