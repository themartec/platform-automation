import os
import sys
import time
import allure
from playwright.async_api import expect
from playwright.sync_api import Playwright

# from common_src.pages.main_employer import MainEmployerPage
# from common_src.pages.story_builder import StoryBuilderPage
# from common_src.pages.story_hub import StoryHubPage
import sys

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.creative_studio import CreativeStudioPage
from common_src.pages.story_hub import StoryHubPage
from common_src.database.database import MartecDatabase


@allure.title("[C2538] Creative Studio - Edit media mode - Export Video Quality 720P")
@allure.description("")
@allure.tag("C2538")
def test_studio_export_video_720(set_up_tear_down, get_base_studio_url,
                                 get_content_id,
                                 remove_and_get_tested_download_files) -> None:
    page = set_up_tear_down
    tested_story_url = f"{get_base_studio_url}home?contentId={get_content_id}&contentType=STORY"
    test_file_name = remove_and_get_tested_download_files
    with allure.step("Access Story"):
        MainEmployerPage(page).access_url(tested_story_url)
        time.sleep(10)
    with allure.step("Download Video As 720P"):
        CreativeStudioPage(page).export_video_with_resolution("720")
    with allure.step("Validate Download Is Successful"):
        expected_file_size = round(float(8.9), 1)
        expected_file_dimension = "1280x720"
        is_download_ok = CreativeStudioPage(page).check_file_is_downloaded_successfully(test_file_name,
                                                                                        expected_file_size,
                                                                                        expected_file_dimension)
        assert is_download_ok is True


@allure.title("[C2539] Creative Studio - Edit media mode - Export Video Quality 1080P")
@allure.description("")
@allure.tag("C2539")
def test_studio_export_video_1080(set_up_tear_down, get_base_studio_url,
                                  get_content_id,
                                  remove_and_get_tested_download_files) -> None:
    page = set_up_tear_down
    tested_story_url = f"{get_base_studio_url}home?contentId={get_content_id}&contentType=STORY"
    test_file_name = remove_and_get_tested_download_files
    with allure.step("Access Story"):
        MainEmployerPage(page).access_url(tested_story_url)
        time.sleep(10)
    with allure.step("Download Video As 1080P"):
        CreativeStudioPage(page).export_video_with_resolution("1080")
    with (allure.step("Validate Download Is Successful")):
        expected_file_size = round(float(15.6), 1)
        expected_file_dimension = "1920x1080"
        is_download_ok = CreativeStudioPage(page
                                            ).check_file_is_downloaded_successfully(test_file_name,
                                                                                    expected_file_size,
                                                                                    expected_file_dimension)
        assert is_download_ok is True


@allure.title("[C2540] Save to Story - Save media to story as 720P ")
@allure.description("")
@allure.tag("C2540")
def test_studio_save_to_story_video_720(set_up_tear_down, get_base_studio_url,
                                        get_base_url,
                                        get_content_id,
                                        get_env_id) -> None:
    page = set_up_tear_down
    base_url = get_base_studio_url
    tested_story_url = f"{base_url}home?contentId={get_content_id}&contentType=STORY"
    with allure.step("Access Story"):
        MainEmployerPage(page).access_url(tested_story_url)
        time.sleep(10)
    with allure.step("Save to Story"):
        CreativeStudioPage(page).save_to_story_video_with_resolution("720")
    with (allure.step("Validate Save Video To Story Is Successful")):
        print(f"get_env_id: {get_env_id}")
        story_details_url = f"{get_base_url}employer/dashboard/{get_content_id}"
        MainEmployerPage(page).access_url(story_details_url)
        StoryHubPage(page).click_on_next_button()
        media_link = StoryHubPage(page).check_studio_video_is_existed()
    with (allure.step("Remove Linked Video From Story")):
        database_connection = MartecDatabase(get_env_id)
        database_connection.remove_video_of_save_to_story(media_link[0])


@allure.title("[C2541] Save to Story - Save media to story as 1080P")
@allure.description("")
@allure.tag("C2541")
def test_studio_save_to_story_video_1080(set_up_tear_down,
                                         get_base_studio_url,
                                         get_base_url,
                                         get_content_id,
                                         get_env_id) -> None:
    page = set_up_tear_down
    base_url = get_base_studio_url
    tested_story_url = f"{base_url}home?contentId={get_content_id}&contentType=STORY"
    with allure.step("Access Story"):
        MainEmployerPage(page).access_url(tested_story_url)
        time.sleep(10)
    with allure.step("Save to Story"):
        CreativeStudioPage(page).save_to_story_video_with_resolution("1080")
    with (allure.step("Validate Save Video To Story Is Successful")):
        print(f"get_env_id: {get_env_id}")
        story_details_url = f"{get_base_url}employer/dashboard/{get_content_id}"
        MainEmployerPage(page).access_url(story_details_url)
        StoryHubPage(page).click_on_next_button()
        media_link = StoryHubPage(page).check_studio_video_is_existed()
    with (allure.step("Remove Linked Video From Story")):
        database_connection = MartecDatabase(get_env_id)
        database_connection.remove_video_of_save_to_story(media_link[0])
