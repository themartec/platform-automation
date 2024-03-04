import time

import allure
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.creative_studio import CreativeStudioPage
from common_src.pages.edit_mode_studio import EditModeStudioPage


@allure.title(
    "[C2568] Brand Kit - Typography (fonts) must be loaded correctly and syn in Text Effect & able to "
    "delete by admin")
@allure.description("Typography (fonts) can be newly loaded in Brand Kit "
                    "and be syned into Text Effect/Font Style "
                    "in 'Text & Cards' tab of Studio Edit Mode for user to select successfully")
@allure.tag("C2568")
def test_load_typography(set_up_tear_down) -> None:
    page = set_up_tear_down
    font_style = "fontawesome-webfont"
    font_file_name = f"test_data/font/{font_style}.ttf"
    with allure.step("Access Brand Kit Tab"):
        MainEmployerPage(page).access_creative_studio_tab()
        creative_studio = CreativeStudioPage(page)
        creative_studio.access_brand_kit_tab()

    with allure.step("Check typography before loading new one"):
        creative_studio.setup_non_typography_is_existed()
    with allure.step(f"Load new typography named {font_file_name}"):
        creative_studio.click_to_add_typography(font_file_name)
    with allure.step(f"Validate typography is loaded"):
        creative_studio.check_typography_is_loaded()
    with allure.step(f"Access Studio edit mode"):
        creative_studio.access_video_library_tab()
        page02 = creative_studio.click_on_web_and_blogs()
    with allure.step(f"Access to update Headline Text"):
        edit_mode_page = EditModeStudioPage(page02)
        edit_mode_page.click_on_text_effects_and_cards()
        edit_mode_page.click_on_text_effects_tab()
        edit_mode_page.click_on_text_effects_headline_text_option()
        edit_mode_page.move_slider_to_active_headline_update()
        edit_mode_page.click_on_headline_text_in_preview()
        edit_mode_page.select_font_style()
    with allure.step(f"Validate Font Style is available & able to selected"):
        edit_mode_page.check_font_style_is_selected(font_style)
        edit_mode_page.back_to_creative_studio()
    with allure.step(f"Validate typography can be deleted"):
        creative_studio_02 = CreativeStudioPage(page02)
        creative_studio_02.access_brand_kit_tab()
        creative_studio_02.close_to_remove_typography()
        creative_studio_02.check_non_typography_is_existed()


@allure.title(
    "[C2569] Brand Kit - Color palette (brand colors) must be loaded correctly, syn in Text Effect and able to "
    "delete by admin ")
@allure.description("Color palette can be newly loaded in Brand Kit "
                    "and be syned into Text Effect/Colour & Background Colour"
                    "in 'Text & Cards' tab of Studio Edit Mode for user to select successfully")
@allure.tag("C2569")
def test_load_color(set_up_tear_down) -> None:
    page = set_up_tear_down
    color_code = "#0d256a"
    with allure.step("Access Brand Kit Tab"):
        MainEmployerPage(page).access_creative_studio_tab()
        creative_studio = CreativeStudioPage(page)
        creative_studio.access_brand_kit_tab()
        time.sleep(10)
    with allure.step("Check color palette before loading new one"):
        creative_studio.setup_non_color_is_existed()
    with allure.step(f"Load new color palette with code {color_code}"):
        creative_studio.click_to_add_color(color_code)
    with allure.step(f"Validate color palette is loaded"):
        creative_studio.check_color_is_loaded()
    with allure.step(f"Access Studio edit mode"):
        creative_studio.access_video_library_tab()
        page02 = creative_studio.click_on_web_and_blogs()
    with allure.step(f"Access to update Headline Text"):
        edit_mode_page = EditModeStudioPage(page02)
        edit_mode_page.click_on_text_effects_and_cards()
        edit_mode_page.click_on_text_effects_tab()
        edit_mode_page.click_on_text_effects_headline_text_option()
        edit_mode_page.move_slider_to_active_headline_update()
        edit_mode_page.click_on_headline_text_in_preview()
        edit_mode_page.set_loaded_color_for_text()
    with allure.step(f"Validate color is available & able to set to Text"):
        edit_mode_page.check_color_is_set(color_code)
    with allure.step(f"Change color to White"):
        edit_mode_page.set_color_for_text(previous_color_code=color_code, new_color_code='#FFFFFF')
    with allure.step(f"Validate color is available & able to set to Background"):
        edit_mode_page.set_loaded_color_for_background()
    with allure.step(f"Validate color can be deleted"):
        edit_mode_page.back_to_creative_studio()
        creative_studio_02 = CreativeStudioPage(page02)
        creative_studio_02.access_brand_kit_tab()
        creative_studio_02.click_close_to_remove_color()
        creative_studio_02.check_non_color_is_existed()
