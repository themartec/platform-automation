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
from common_src.patterns.studio_sub_tab_name import StudioSubTab

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
        CreativeStudioPage(page).click_on_edit_template(template_image_dir, 1)
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
        creative_page = CreativeStudioPage(page)
        creative_page.check_template_is_shown_on_Templates_tab(template_image_dir_personal,
                                                               template_name_personal,
                                                               template_tag_personal)

    with allure.step("Validate only personal template is shown in Brand tab"):
        creative_page.check_template_is_shown_on_Templates_tab(template_image_dir_personal,
                                                               template_name_personal,
                                                               template_tag_personal)
    with allure.step("Hover on template & Click on edit template"):
        creative_page.click_on_edit_template(template_image_dir_personal, 2)
        time.sleep(20)
    with allure.step("Validate media as image is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_image()
    with allure.step("Validate text effect Headline is available in timeline"):
        EditModeStudioPage(page).check_timeline_has_text_effects_as("Headline Text")


@allure.title("[C2571] Brand - Load assets in tabs & add asset to timeline and remove")
@allure.description("")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2571")
def test_studio_load_assets_brand_tab_and_timeline_behavior(set_up_tear_down_without_state, get_env_id,
                                                            get_media_url) -> None:
    page = set_up_tear_down_without_state

    with allure.step("Log in"):
        LoginPage(page).enter_username_password(os.getenv("USER_NAME_OF_NON_ISOLATED_ACC"),
                                                os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        MainEmployerPage(page).access_content_recipes()
    with allure.step("Access to Creative Studio Edit page"):
        MainEmployerPage(page).access_creative_studio_tab()
        # time.sleep(15)
        creative_page = CreativeStudioPage(page)
        edit_page = creative_page.click_on_web_and_blog_option()
    with allure.step("Click on Brand sub-tab of Media tab"):
        studio_page = CreativeStudioPage(edit_page)
        studio_page.click_on_Brand_tab_of_media()
    with allure.step("By default, All tab is showing with all media types"):
        studio_page.check_all_media_types_shown_in_all_tab_name(number_of_media=4)
    with allure.step("[Logos] Click on Logos tab and check logo can be added to timeline and remove"):
        studio_page.click_on_tab_name(StudioSubTab.LOGOS.value)
        studio_page.check_media_can_be_added_and_remove_in_timeline("Image 01")
    with allure.step("[Logos] Validate that image won't be shown here"):
        studio_page.check_logo_is_not_shown_image()

    with allure.step("[Videos] Click on Videos tab and check video can be added to timeline and remove"):
        studio_page.click_on_tab_name(StudioSubTab.VIDEOS.value)
        studio_page.check_media_can_be_added_and_remove_in_timeline("Video 01")

    with allure.step("[Music] Click on Music tab and check video can be added to timeline and remove"):
        studio_page.click_on_media_tab()
        studio_page.click_on_tab_name(StudioSubTab.MUSIC.value)
        time.sleep(30)
        studio_page.check_media_can_be_added_and_remove_in_timeline("Music 02")

    with allure.step("[Images] Click on Music tab and check video can be added to timeline and remove"):
        studio_page.click_on_tab_name(StudioSubTab.IMAGES.value)
        studio_page.check_media_can_be_added_and_remove_in_timeline("Image 01")
        studio_page.check_image_is_not_shown_logo()


@allure.title("[C2644] Upload From All tab -Brand - Upload Video in ALL tabs & Remove It")
@allure.description("")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2644")
def test_studio_upload_from_all_tab_for_video(set_up_tear_down_without_state, get_env_id, get_media_url) \
        -> None:
    page = set_up_tear_down_without_state

    with allure.step("Log in"):
        LoginPage(page).enter_username_password(os.getenv("USER_NAME_OF_NON_ISOLATED_ACC_02"),
                                                os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        MainEmployerPage(page).access_content_recipes()
    with allure.step("Access to Creative Studio Edit page"):
        MainEmployerPage(page).access_creative_studio_tab()
        # time.sleep(15)
        creative_page = CreativeStudioPage(page)
        edit_page = creative_page.click_on_web_and_blog_option()
    with allure.step("Click on Brand sub-tab of Media tab"):
        studio_page = CreativeStudioPage(edit_page)
        studio_page.click_on_Brand_tab_of_media()
        video_file_name = f"test_data/media/video_30s_480x270_710kB.mov"
        video_duration_time = "00:30"
        # Remove all video for fresh test
        studio_page.remove_video_from_tab_name_if_any(tab_name=StudioSubTab.VIDEOS, duration_video=video_duration_time)
    with allure.step("From All Tab, upload a video"):
        studio_page.click_on_tab_name(StudioSubTab.ALL.value)
        studio_page.click_on_upload_button_and_set_file(video_file_name)
    with allure.step("Validate Video is displayed in All Tab"):
        studio_page.check_video_is_displayed_in_tab_name(tab_name=StudioSubTab.ALL, duration_video=video_duration_time)
    with allure.step("Validate Video is displayed in Video Tab"):
        studio_page.check_video_is_displayed_in_tab_name(tab_name=StudioSubTab.VIDEOS,
                                                         duration_video=video_duration_time)
    with allure.step("Validate Video is not displayed in Image, Logos, Music Tab"):
        studio_page.check_video_is_not_displayed_in_tab_name(tab_name=StudioSubTab.IMAGES,
                                                             duration_video=video_duration_time)
        studio_page.check_video_is_not_displayed_in_tab_name(tab_name=StudioSubTab.LOGOS,
                                                             duration_video=video_duration_time)
        studio_page.check_video_is_not_displayed_in_tab_name(tab_name=StudioSubTab.MUSIC,
                                                             duration_video=video_duration_time)
    with allure.step("Validate Video can be removed from ALL tab, not displayed in ALL tab & Video tab anymore"):
        studio_page.check_remove_video_from_tab_name(tab_name=StudioSubTab.ALL, duration_video=video_duration_time)
        studio_page.check_video_is_removed_from_tab(tab_name=StudioSubTab.VIDEOS, duration_video=video_duration_time)


@allure.title("[C2648] Upload From All tab - Brand - Upload Image in ALL tabs & Remove It")
@allure.description("")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2648")
def test_studio_upload_from_all_tab_for_image(set_up_tear_down_without_state, get_env_id, get_media_url) \
        -> None:
    page = set_up_tear_down_without_state

    with allure.step("Log in"):
        LoginPage(page).enter_username_password(os.getenv("USER_NAME_OF_NON_ISOLATED_ACC_02"),
                                                os.getenv("PASSWORD_OF_NON_ISOLATED_ACC"))
        MainEmployerPage(page).access_content_recipes()
    with allure.step("Access to Creative Studio Edit page"):
        MainEmployerPage(page).access_creative_studio_tab()
        # time.sleep(15)
        creative_page = CreativeStudioPage(page)
        edit_page = creative_page.click_on_web_and_blog_option()
    with allure.step("Click on Brand sub-tab of Media tab"):
        studio_page = CreativeStudioPage(edit_page)
        studio_page.click_on_Brand_tab_of_media()
        media_file_name = f"test_data/media/shrimp_auto.png"
        # Remove all video for fresh test
        studio_page.remove_image_from_tab_name_if_any(tab_name=StudioSubTab.IMAGES)
    with allure.step("From All Tab, upload a image"):
        studio_page.click_on_upload_button_and_set_file(media_file_name)
    with allure.step("Validate Image is displayed in All Tab"):
        studio_page.check_image_is_displayed_in_tab_name(tab_name=StudioSubTab.ALL)
    with allure.step("Validate Image is displayed in Images Tab"):
        studio_page.check_image_is_displayed_in_tab_name(tab_name=StudioSubTab.IMAGES)
    with allure.step("Validate Image is not displayed in Logos Tab"):
        studio_page.check_image_is_not_displayed_in_tab_name(tab_name=StudioSubTab.LOGOS)
    with allure.step("Validate Image can be removed from ALL tab"):
        studio_page.check_remove_image_from_tab_name(tab_name=StudioSubTab.ALL)
        studio_page.check_image_is_removed_from_tab(tab_name=StudioSubTab.IMAGES)


@allure.title("[C2652] Edit Video - Split Video")
@allure.description("")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2652")
def test_studio_split_video(set_up_tear_down, get_base_studio_url, get_content_id, get_media_url):
    page = set_up_tear_down
    tested_story_url = f"{get_base_studio_url}home?contentId={get_content_id}&contentType=STORY"
    with allure.step("Access tested story from Story Hub"):
        MainEmployerPage(page).access_url(tested_story_url)
        time.sleep(10)
    with allure.step("Click on Stories tab"):
        studio_page = CreativeStudioPage(page)
        studio_page.click_on_stories_tab()
    with allure.step("Split the shown video into 2 parts in timeline box"):
        edit_mode_page = EditModeStudioPage(page)
        edit_mode_page.move_slider_to_half_thumbnail_video()
        edit_mode_page.click_on_video_thumbnail_in_timeline()
        edit_mode_page.click_on_split_video_button()
    with allure.step("Validate splitting video is successful"):
        with allure.step("There is 2 parts of split video"):
            edit_mode_page.check_video_is_split_into(2)
        with allure.step("Split duration is correct as 00:15 each part"):
            edit_mode_page.check_split_video_duration(2, "00:15")
    with allure.step("Now, Click on Undo button"):
        edit_mode_page.click_on_undo_button()
    with allure.step("Validate video is not split after undoing, duration should be 00:30"):
        edit_mode_page.check_video_is_not_split("00:30")
