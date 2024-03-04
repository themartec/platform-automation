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


@allure.title("[C2570] Load assets - Template (Personal, Company) can be loaded successfully with fully contents in "
              "edit mode")
@allure.description("")
@allure.tag("C2570")
def test_studio_load_assets(set_up_tear_down_without_state) -> None:
    page = set_up_tear_down_without_state
    with allure.step("Log in"):
        LoginPage(page).enter_username_password(os.getenv("USER_NAME_OF_NON_ISOLATED_ACC"),
                                                os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))

        MainEmployerPage(page).access_content_recipes()
    with allure.step("Access to template"):
        MainEmployerPage(page).access_creative_studio_tab()
        time.sleep(15)
    with allure.step("Validate template of company template is shown"):
        template_image_dir_company = ("https://cdndev.themartec.com/assets/a693aafd-0313-4089-8e48-2bfecdb093e3"
                                     "/logo_auto-30bbafb5-673b-46c3-8969-b3d2e044af65.jpeg")
        template_name_company = "Automation Company Template"
        template_tag_company = "Career Stories"
        CreativeStudioPage(page).check_template_is_shown_on_Templates_tab(template_image_dir_company,
                                                                          template_name_company,
                                                                          template_tag_company)
    #
    with allure.step("Validate template of personal template is shown"):
        template_image_dir_personal = ("https://cdndev.themartec.com/assets/a693aafd-0313-4089-8e48-2bfecdb093e3"
                                       "/shrimp_auto-b02776bb-4647-4d32-b37f-360bb54b6ea9.png")
        template_name_personal = "Automation Personal Template"
        template_tag_personal = "Career Stories"
        CreativeStudioPage(page).check_template_is_shown_on_Templates_tab(template_image_dir_personal,
                                                                          template_name_personal,
                                                                          template_tag_personal)
    with allure.step("Click on Brand tab"):
        CreativeStudioPage(page).click_on_Brand_tab()
    with allure.step("Validate only company template is shown in Brand tab"):
        template_image_dir_personal = ("https://cdndev.themartec.com/assets/a693aafd-0313-4089-8e48-2bfecdb093e3"
                                     "/logo_auto-30bbafb5-673b-46c3-8969-b3d2e044af65.jpeg")
        template_name_personal = "Automation Company Template"
        template_tag_personal = "Career Stories"
        CreativeStudioPage(page).check_template_is_shown_on_Templates_tab(template_image_dir_personal,
                                                                          template_name_personal,
                                                                          template_tag_personal)
    with allure.step("Click on Edit template"):
        template_image_dir = ("https://cdndev.themartec.com/assets/a693aafd-0313-4089-8e48-2bfecdb093e3/logo_auto"
                              "-30bbafb5-673b-46c3-8969-b3d2e044af65.jpeg")
        CreativeStudioPage(page).click_on_edit_template(template_image_dir)
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


@allure.title("[C2573] Load assets - Text & Cards tab - Load font uploaded in creative menu successfully")
@allure.description("")
@allure.tag("C2573")
def test_studio_load_assets_text_card(set_up_tear_down_without_state) -> None:
    page = set_up_tear_down_without_state
    with allure.step("Log in"):
        LoginPage(page).enter_username_password(os.getenv("USER_NAME_OF_NON_ISOLATED_ACC"),
                                                os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))

        MainEmployerPage(page).access_content_recipes()
    with allure.step("Access to template"):
        MainEmployerPage(page).access_creative_studio_tab()
        time.sleep(15)