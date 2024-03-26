import allure
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.pages.main_employer import MainEmployerPage
from common_src.pages.library import LibraryPage


@allure.title("[C2643] Library - Video stories info is matching to story hub and has type as VIDEO along with RAW "
              "status")
@allure.description("")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2643")
def test_video_info(set_up_tear_down) -> None:
    page = set_up_tear_down
    with allure.step("Access Library tab"):
        MainEmployerPage(page).access_library_tab()
    with allure.step("Story Video should have correct title & related question"):
        library_page = LibraryPage(page)
        library_page.check_header_title_is_correct(
            "[DOWNLOAD_VIDEO] Automation Blog To Test Download Video (Don't remove)")
        library_page.check_question_is_correctly_shown(
            "How do you stay motivated and productive while working remotely?")
    with allure.step("Story Video should have RAW status, Video Type"):
        library_page.check_type_of_media("VIDEO")
        library_page.check_status_of_media("RAW")


@allure.title("[C2646] Library - Click on Edit icon on Video Thumbnail will navigate user to Edit page")
@allure.description("")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2646")
def test_video_edit_icon(set_up_tear_down) -> None:
    page = set_up_tear_down
    with allure.step("Access Library tab"):
        MainEmployerPage(page).access_library_tab()
    with allure.step("Story Video should have Edit icon in thumbnail"):
        library_page = LibraryPage(page)
        library_page.check_edit_icon_in_thumbnail()
    with allure.step("Click on Edit button will navigate user to Edit Video page"):
        edit_page = library_page.click_on_edit_button_of_vide_name("How do you stay motivated and")
        edit_page_obj = LibraryPage(edit_page)
        edit_page_obj.check_edit_page_is_opened_after_clicking_on_edit_button()


@allure.title("[C2647] Library - Click on Download on Video Thumbnail will able to download that video")
@allure.description("")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2647")
def test_video_download_icon(set_up_tear_down) -> None:
    page = set_up_tear_down
    file_name = "download_from_thumbnail.mp4"
    with allure.step("[Precondition] Remove Exsiting File If Any"):
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"[PRE-CONDITION] The {file_name} file is removed")
        else:
            print(f"[PRE-CONDITION] The {file_name} file does not exist")

    with allure.step("Access Library tab"):
        MainEmployerPage(page).access_library_tab()
    with allure.step("Story Video should have Download icon in thumbnail"):
        library_page = LibraryPage(page)
        video_name = "How do you stay motivated and"
        library_page.check_download_icon_in_thumbnail_of_video(video_name)
    with allure.step("Click on Download button will be able to download video"):
        downloaded_file = library_page.click_on_download_button_in_thumbnail_of_video(video_name)
        is_download_ok = library_page.check_file_is_downloaded_successfully(downloaded_file)
        assert is_download_ok is True
