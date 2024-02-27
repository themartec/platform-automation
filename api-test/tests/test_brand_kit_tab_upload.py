import os
import logging
import pytest
import allure
from dotenv import load_dotenv
from src.studio import Studio

cwd = os.getcwd()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
def reset_state_brand_kit_tab(request) -> str:
    print("\nPerforming set up...")
    load_dotenv()
    base_url = match_env(os.getenv('TEST_ENV'))

    Studio(base_url).remove_logo_brand_kit_tab()

    def finalizer():
        print("\nPerforming teardown...")
        Studio(base_url).remove_logo_brand_kit_tab()

    request.addfinalizer(finalizer)

    return base_url


@allure.title("Studio - Upload Logo From Brand Kit Tab")
@allure.description("Logo upload as format JPEG")
def test_brand_kit_upload_for_logo(reset_state_brand_kit_tab):
    file_list_dir = [f"{cwd}/test_data/logo_auto.jpeg"]
    response = Studio(reset_state_brand_kit_tab).upload_logo_brand_kit_tab(file_list_dir)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 200  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Add Logo for Brand Kit successfully"
    assert len(json_data["data"]) == 1
