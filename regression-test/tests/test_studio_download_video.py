import time
import allure

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.creative_studio import CreativeStudioPage
from common_src.pages.story_hub import StoryHubPage
from common_src.database.database import MartecDatabase
from common_src.actions.click_on_button import click_on_button_name

COMMON_STEP_NAME_01 = "Access Tested Story From Story Hub"


def get_data_of_media(env_id: str, media_url: str):
    video_dev = "sample_video_02_511ea68e-b980-4e54-8dec-7effe2dc07b7.mp4"
    video_stg = "sample_video_02_9f6d2930-5ec9-44ed-be4a-26b255807f0d.mp4"
    if env_id == '2':  # dev
        return f"{media_url}videos/5b1e93f8-7277-450f-b69b-2fa341a757d4/{video_dev}"
    else:
        return f"{media_url}videos/42574232-5b71-4f52-aa05-df912fb5dcb1/{video_stg}"


@allure.title("[C2538, C2638] Creative Studio - Edit media mode - Export Video Quality 720P & Load video in Stories "
              "tab and Preview panel")
@allure.description("[C2564] Download Video - Export Video Successfully as 720P\n"
                    "[C2638] Edit media mode - Load assets - Story tab - Load all related videos from edit video of a story and video is also viewable in preview window\n"
                    "Uploaded Video Size: 720KB")
@allure.tag("C2564", "C2638")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2564\n{os.getenv('TESTRAIL_URL')}2638")
def test_studio_export_video_720(set_up_tear_down,
                                 get_env_id,
                                 get_media_url,
                                 get_base_studio_url,
                                 get_content_id,
                                 remove_and_get_tested_download_files) -> None:
    page = set_up_tear_down
    tested_story_url = f"{get_base_studio_url}home?contentId={get_content_id}&contentType=STORY"
    test_file_name = remove_and_get_tested_download_files
    with allure.step(COMMON_STEP_NAME_01):
        MainEmployerPage(page).access_url(tested_story_url)
        time.sleep(10)
    with allure.step("Click on Stories tab"):
        studio_page = CreativeStudioPage(page)
        studio_page.click_on_stories_tab()
        time.sleep(5)
    with allure.step("Validate video asset is loaded"):
        media_url = get_data_of_media(get_env_id, get_media_url)
        studio_page.check_video_is_displayed_in_stories_tab(media_url)
    with allure.step("Validate video asset is loaded in preview panel"):
        studio_page.check_video_is_displayed_in_preview(media_url)
    with allure.step("Download Video As 720P"):
        studio_page.export_video_with_resolution("720")
    with allure.step("Validate Download Is Successful"):
        # expected_file_size = round(float(8.9), 1)
        expected_file_dimension = "1280x720"
        is_download_ok = CreativeStudioPage(page).check_file_is_downloaded_successfully(test_file_name,
                                                                                        expected_file_dimension)
        assert is_download_ok is True


@allure.title("[C2565, C2639] Download Video - Export Video Successfully as 1080P & Edit video is loaded as "
              "default "
              "in Timeline")
@allure.description("Uploaded Video Size: 720KB")
@allure.tag("C2565", "C2639")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2564\n{os.getenv('TESTRAIL_URL')}2639")
def test_studio_export_video_1080(set_up_tear_down, get_base_studio_url,
                                  get_content_id,
                                  remove_and_get_tested_download_files) -> None:
    page = set_up_tear_down
    tested_story_url = f"{get_base_studio_url}home?contentId={get_content_id}&contentType=STORY"
    test_file_name = remove_and_get_tested_download_files
    with allure.step(COMMON_STEP_NAME_01):
        MainEmployerPage(page).access_url(tested_story_url)
        time.sleep(10)
    with allure.step("Validate story video is loaded by default in timeline"):
        studio_page = CreativeStudioPage(page)
        studio_page.check_video_is_displayed_in_timeline()
    with allure.step("Download Video As 1080P"):
        studio_page.export_video_with_resolution("1080")
    with (allure.step("Validate Download Is Successful")):
        # expected_file_size = round(float(15.6), 1)
        expected_file_dimension = "1920x1080"
        is_download_ok = CreativeStudioPage(page
                                            ).check_file_is_downloaded_successfully(test_file_name,
                                                                                    expected_file_dimension)
        assert is_download_ok is True


@allure.title("[C2566] Save to Story - Save video to story as 720P")
@allure.description("")
@allure.tag("C2566")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2566")
def test_studio_save_to_story_video_720(set_up_tear_down, get_base_studio_url,
                                        get_base_url,
                                        get_content_id,
                                        get_env_id) -> None:
    page = set_up_tear_down
    base_url = get_base_studio_url
    tested_story_url = f"{base_url}home?contentId={get_content_id}&contentType=STORY"
    print(f"get_env_id: {get_env_id}")
    story_details_url = f"{get_base_url}employer/dashboard/{get_content_id}"
    with allure.step(COMMON_STEP_NAME_01):
        main_page = MainEmployerPage(page)
        main_page.access_url(story_details_url)
        click_on_button_name(page, "Next")
        story_page = StoryHubPage(page)
        before_videos = story_page.count_number_of_video()
        print(f"Number Of Video Before Testing: {before_videos}")

        main_page.access_url(tested_story_url)
        time.sleep(5)
    with allure.step("Save to Story"):
        CreativeStudioPage(page).save_to_story_video_with_resolution("720")
    with (allure.step("Validate Save Video To Story Is Successful")):
        main_page.access_url(story_details_url)
        click_on_button_name(page, "Next")
        after_videos = story_page.count_number_of_video()
        print(f"Number Of Video After Testing: {after_videos}")
        assert after_videos == (before_videos + 1)
        media_links = story_page.get_video_links()
        database_connection = MartecDatabase(get_env_id)
        database_connection.remove_videos_of_save_to_story(media_links)


@allure.title("[C2567] Save to Story - Save video to story as 1080P")
@allure.description("")
@allure.tag("C2567")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2567")
def test_studio_save_to_story_video_1080(set_up_tear_down,
                                         get_base_studio_url,
                                         get_base_url,
                                         get_content_id,
                                         get_env_id) -> None:
    page = set_up_tear_down
    base_url = get_base_studio_url
    tested_story_url = f"{base_url}home?contentId={get_content_id}&contentType=STORY"
    print(f"get_env_id: {get_env_id}")
    story_details_url = f"{get_base_url}employer/dashboard/{get_content_id}"
    with allure.step(COMMON_STEP_NAME_01):
        main_page = MainEmployerPage(page)
        main_page.access_url(story_details_url)
        click_on_button_name(page, "Next")
        story_page = StoryHubPage(page)
        before_videos = story_page.count_number_of_video()
        print(f"Number Of Video Before Testing: {before_videos}")

        main_page.access_url(tested_story_url)
        time.sleep(5)
    with allure.step("Save to Story"):
        CreativeStudioPage(page).save_to_story_video_with_resolution("1080")
    with (allure.step("Validate Save Video To Story Is Successful")):
        main_page.access_url(story_details_url)
        click_on_button_name(page, "Next")
        after_videos = story_page.count_number_of_video()
        print(f"Number Of Video After Testing: {after_videos}")
        assert after_videos == (before_videos + 1)
        media_links = story_page.get_video_links()
        database_connection = MartecDatabase(get_env_id)
        database_connection.remove_videos_of_save_to_story(media_links)
