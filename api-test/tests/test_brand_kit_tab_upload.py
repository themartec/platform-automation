import os
import logging
import allure

from src.brand_kit_tab import BrandKitTab

cwd = os.getcwd()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@allure.title("[C2542] Brand Kit - Logo (JPEG) can be loaded successfully for admin")
@allure.description("Logo upload as format JPEG")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2542")
def test_brand_kit_upload_for_logo_jpeg(reset_state_brand_kit_tab, get_base_studio_api_url):
    with allure.step("Call API"):
        file_list_dir = [f"{cwd}/test_data/logo_auto.jpeg"]
        response = BrandKitTab(reset_state_brand_kit_tab).upload_logo_brand_kit_tab(file_list_dir)
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        assert response.status_code == 200  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Add Logo for Brand Kit successfully"
        assert len(json_data["data"]) == 1


@allure.title("[C2543] Brand Kit - Logo (PNG) can be loaded successfully for all admin")
@allure.description("Logo upload as format PNG")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2543")
def test_brand_kit_upload_for_logo_png(reset_state_brand_kit_tab):
    with allure.step("Call API"):
        file_list_dir = [f"{cwd}/test_data/sample_image_4k_01.png"]
        response = BrandKitTab(reset_state_brand_kit_tab).upload_logo_brand_kit_tab(file_list_dir)
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        assert response.status_code == 200  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Add Logo for Brand Kit successfully"
        assert len(json_data["data"]) == 1
