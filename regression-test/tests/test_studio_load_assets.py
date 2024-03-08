import time
import allure
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.pages.login import LoginPage
from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.creative_studio import CreativeStudioPage
from common_src.pages.edit_mode_studio import EditModeStudioPage

content_id_dev = "a693aafd-0313-4089-8e48-2bfecdb093e3"
content_id_stg = "d0075dc7-7aca-40ca-9781-48b25615b363"


def get_data_of_image_in_personal_play_screen(env_id: str, media_url: str):
    image_dev = "shrimp_auto-6bd44835-758d-4a13-a5d2-43e50a6522c8.png"
    image_stg = "shrimp_auto-.png"
    if env_id == '2':  # dev
        return f"{media_url}assets/{content_id_dev}/{image_dev}"
    else:
        return f"{media_url}assets/{content_id_stg}/{image_stg}"


def get_data_of_template_image_dir_personal(env_id: str, media_url: str):
    image_02_dev = "shrimp_auto-b02776bb-4647-4d32-b37f-360bb54b6ea9.png"
    image_02_stg = "shrimp_auto-5d4f39ea-ad6f-4e17-876d-dae3a260706c.png"
    if env_id == '2':  # dev
        return f"{media_url}assets/{content_id_dev}/{image_02_dev}"
    else:
        return f"{media_url}assets/{content_id_stg}/{image_02_stg}"


def get_data_of_template_image_dir_company(env_id: str, media_url: str):
    image_01_dev = "logo_auto-30bbafb5-673b-46c3-8969-b3d2e044af65.jpeg"
    image_01_stg = "logo_auto-8338d2a6-e015-4149-a626-b7963f9bcd3f.jpeg"
    if env_id == '2':  # dev
        return f"{media_url}assets/{content_id_dev}/{image_01_dev}"
    else:
        return f"{media_url}assets/{content_id_stg}/{image_01_stg}"


@allure.title("[C2570] Load assets - Template Company can be loaded successfully with fully contents in "
              "edit mode")
@allure.description("Company/Brand template is shown on Studio tab and its assets are loaded completely in timeline "
                    "in Edit mode")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2570")
def test_studio_load_assets_company_template(set_up_tear_down_without_state, get_env_id, get_media_url) -> None:
    page = set_up_tear_down_without_state

    with allure.step("Log in"):
        LoginPage(page).enter_username_password(os.getenv("USER_NAME_OF_NON_ISOLATED_ACC"),
                                                os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))

        MainEmployerPage(page).access_content_recipes()
    with allure.step("Access to template"):
        MainEmployerPage(page).access_creative_studio_tab()
        time.sleep(15)
    with allure.step("Validate template of company template is shown"):
        template_image_dir_company = get_data_of_template_image_dir_company(get_env_id, get_media_url)
        template_name_company = "Automation Company Template"
        template_tag_company = "Career Stories"
        CreativeStudioPage(page).check_template_is_shown_on_Templates_tab(template_image_dir_company,
                                                                          template_name_company,
                                                                          template_tag_company)
    with allure.step("Click on Brand tab"):
        CreativeStudioPage(page).click_on_Brand_tab()
    with allure.step("Validate only company/brand template is shown in Brand tab"):
        CreativeStudioPage(page).check_template_is_shown_on_Templates_tab(template_image_dir_company,
                                                                          template_name_company,
                                                                          template_tag_company)
    with allure.step("Hover on template & Click on edit template"):
        template_image_dir = get_data_of_template_image_dir_company(get_env_id, get_media_url)
        CreativeStudioPage(page).click_on_edit_template(template_image_dir,1)
        time.sleep(25)
    with allure.step("Validate video is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_video()
    with allure.step("Validate text effect Headline is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_text_effects_as("Headline Text")
    with allure.step("Validate text effect Body is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_text_effects_as("Body Text")
    with allure.step("Validate text effect Caption is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_text_effects_as(":06Caption")
    with allure.step("Validate card is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_card_as("Graphic  01")


@allure.title("[C2640] Load assets - Template Personal can be loaded successfully with fully contents in "
              "edit mode")
@allure.description("Personal template is shown on Studio tab and its assets are loaded completely in timeline")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2640")
def test_studio_load_assets_personal_template(set_up_tear_down_without_state, get_env_id, get_media_url) -> None:
    page = set_up_tear_down_without_state

    with allure.step("Log in"):
        LoginPage(page).enter_username_password(os.getenv("USER_NAME_OF_NON_ISOLATED_ACC"),
                                                os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))

        MainEmployerPage(page).access_content_recipes()
    with allure.step("Access to template"):
        MainEmployerPage(page).access_creative_studio_tab()
        time.sleep(15)

    with allure.step("Validate template of personal template is shown"):
        template_image_dir_personal = get_data_of_template_image_dir_personal(get_env_id, get_media_url)
        template_name_personal = "Automation Personal Template"
        template_tag_personal = "Career Stories"
        CreativeStudioPage(page).check_template_is_shown_on_Templates_tab(template_image_dir_personal,
                                                                          template_name_personal,
                                                                          template_tag_personal)

    with allure.step("Validate only personal template is shown in Brand tab"):
        CreativeStudioPage(page).check_template_is_shown_on_Templates_tab(template_image_dir_personal,
                                                                          template_name_personal,
                                                                          template_tag_personal)
    with allure.step("Hover on template & Click on edit template"):
        CreativeStudioPage(page).click_on_edit_template(template_image_dir_personal, 2)
        time.sleep(20)
    with allure.step("Validate media as image is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_image()
    with allure.step("Validate text effect Headline is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_text_effects_as("Headline Text")

