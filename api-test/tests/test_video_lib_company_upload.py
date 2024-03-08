import os
import logging
import allure
from dotenv import load_dotenv
from src.brand_kit import BrandKit

from common.date import get_date_as_yyyymmdd

from src.get_studio_upload_download_info import get_upload_time

cwd = os.getcwd()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@allure.title("[C2554] Upload Company Brand - Image upload for single [HD, 1.1MB, PNG] image")
@allure.description("Single image with format [HD, 1.1MB, PNG]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2554")
def test_upload_for_SINGLE_image(reset_state_studio_video, get_base_studio_api_url):
    file_name = "shrimp_auto"
    file_list_dir = [f"{cwd}/test_data/{file_name}.png"]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_image_list(file_list_dir)
    data = response.json()
    logger.info(f"[API Response] \n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(data) > 0
    assert data["message"] == "Response Success"
    img_obj = data["data"]["images"]
    assert len(img_obj) == 1, "Validate uploading for one media only"
    img_obj = img_obj[0]
    assert file_name in str(img_obj["imageName"])
    assert str(img_obj["Link"]) != ""
    assert int(img_obj["width"]) > 0
    assert int(img_obj["height"]) > 0
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = img_obj["imageName"]
        speed_time = get_upload_time(get_base_studio_api_url,
                                     current_date,
                                     "duration",
                                     file_name)
        logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, speed_time: {speed_time}")
        file_size = get_upload_time(get_base_studio_api_url,
                                    current_date,
                                    "fileSize",
                                    file_name) / (1024 * 1024)
        logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB")


@allure.title("[C2555] Upload Company Brand - Image upload for multiple mixed image formats")
@allure.description("Mixed Image with format JPEG, PNG, GIF")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2555")
def test_upload_for_multiple_images(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/screen_auto.jpeg",
                     f"{cwd}/test_data/shrimp_auto.png",
                     f"{cwd}/test_data/gif_image_auto.gif"]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_image_list(file_list_dir)
    with allure.step("Validate API Response"):
        data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(data) > 0
        assert data["message"] == "Response Success"
        assert len(data["data"]["images"]) == len(file_list_dir), "Validate uploading for one media only"
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        images = data["data"]["images"]
        for image in images:
            file_name = image["imageName"]
            speed_time = get_upload_time(get_base_studio_api_url,
                                         current_date,
                                         "duration",
                                         file_name)
            logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, speed_time: {speed_time}")
            file_size = get_upload_time(get_base_studio_api_url,
                                        current_date,
                                        "fileSize",
                                        file_name) / (1024 * 1024)
            logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB")


@allure.title("[C2556] Upload Company Brand - Logo upload for multiple mixed logos")
@allure.description("Mixed Logos with format JPEG, PNG")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2556")
def test_upload_for_multiple_logos(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_logo_01.jpeg", f"{cwd}/test_data/sample_logo_02.png"]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_logos_list(file_list_dir)
    with allure.step("Validate API Response"):
        data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(data) > 0
        assert data["message"] == "Response Success"
        assert len(data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        images = data["data"]
        for image in images:
            file_name = image["logoName"]
            speed_time = get_upload_time(get_base_studio_api_url,
                                         current_date,
                                         "duration",
                                         file_name)
            logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, speed_time: {speed_time}")
            file_size = get_upload_time(get_base_studio_api_url,
                                        current_date,
                                        "fileSize",
                                        file_name) / (1024 * 1024)
            logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB")


@allure.title("[C2557] Upload Company Brand - Video upload for single [HD, < 100MB, mp4] video")
@allure.description("Video with format MP4, 45.89 MB")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2557")
def test_upload_for_single_video(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4"]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_video_list(file_list_dir)
    with allure.step("Validate API Response"):
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        file_size = int(json_data["data"]["videos"][0]["fileSize"]) / 1048576
        logger.info(f'  - 1st Video Size: {file_size:.2f} MB')
        assert len(json_data["data"]["videos"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        videos = json_data["data"]["videos"]
        for video in videos:
            file_name = video["videoName"]
            speed_time = get_upload_time(get_base_studio_api_url,
                                         current_date,
                                         "duration",
                                         file_name)
            logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, speed_time: {speed_time}")
            file_size = get_upload_time(get_base_studio_api_url,
                                        current_date,
                                        "fileSize",
                                        file_name) / (1024 * 1024)
            logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB")


@allure.title("[C2558] Upload Company Brand - Video upload for multiple mixed videos")
@allure.description("Mixed Video with format [MOV, 0.68MB], [MP4, 45.89 MB]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2558")
def test_upload_for_multiple_videos(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4",
                     f"{cwd}/test_data/sample_video_02.mov"]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_video_list(file_list_dir)
    with allure.step("Validate API Response"):
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        assert len(json_data["data"]["videos"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        videos = json_data["data"]["videos"]
        for video in videos:
            file_name = video["videoName"]
            speed_time = get_upload_time(get_base_studio_api_url,
                                         current_date,
                                         "duration",
                                         file_name)
            file_size = get_upload_time(get_base_studio_api_url,
                                        current_date,
                                        "fileSize",
                                        file_name) / (1024 * 1024)
            logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB, "
                        f"speed_time: {speed_time} seconds")


@allure.title("[C2559] Upload Company Brand - Music upload for single [mp3, 5MB] music")
@allure.description("Music with format [mp3, 5MB]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2559")
def test_upload_for_single_music(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_music_02.mp3"]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_music_list(file_list_dir)
    with allure.step("Validate API Response"):
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        logger.info(f'  - 1st Music Size: {int(json_data["data"]["musics"][0]["fileSize"]) / 1048576:.2f} MB')
        assert len(json_data["data"]["musics"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"]["musics"][0]["musicName"]
        speed_time = get_upload_time(get_base_studio_api_url,
                                     current_date,
                                     "duration",
                                     file_name)
        file_size = get_upload_time(get_base_studio_api_url,
                                    current_date,
                                    "fileSize",
                                    file_name) / (1024 * 1024)
        logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB, "
                    f"speed_time: {speed_time} seconds")


@allure.title("[C2560] Upload Company Brand - Music upload for multiple mixed musics")
@allure.description("Mixed Music with format [mp3, 1.01MB, 5.07MB]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2560")
def test_upload_for_multiple_musics(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3",
                     f"{cwd}/test_data/sample_music_02.mp3"]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_music_list(file_list_dir)
    with allure.step("Validate API Response"):
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        assert len(json_data["data"]["musics"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        musics = json_data["data"]["musics"]
        for music in musics:
            file_name = music["musicName"]
            speed_time = get_upload_time(get_base_studio_api_url,
                                         current_date,
                                         "duration",
                                         file_name)

            file_size = get_upload_time(get_base_studio_api_url,
                                        current_date,
                                        "fileSize",
                                        file_name) / (1024 * 1024)
            logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB, "
                        f"speed_time: {speed_time} seconds")


@allure.title("[C2561] Upload Company Brand - Video upload for single [4K, 38MB, mp4] video")
@allure.description("Video with format MP4, 38MB, 4K")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2561")
def test_upload_for_single_video(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_4k_video_less100MB_03.mp4"]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_video_list(file_list_dir)
    with allure.step("Validate API Response"):
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        file_size = int(json_data["data"]["videos"][0]["fileSize"]) / 1048576
        assert len(json_data["data"]["videos"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"]["videos"][0]["videoName"]
        speed_time = get_upload_time(get_base_studio_api_url,
                                     current_date,
                                     "duration",
                                     file_name)

        file_size = get_upload_time(get_base_studio_api_url,
                                    current_date,
                                    "fileSize",
                                    file_name) / (1024 * 1024)
        logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB, "
                    f"speed_time: {speed_time} seconds")


@allure.title("[C2562] Upload Company Brand - All upload for single [HD, 17MB, mp4] video")
@allure.description("Single Video Upload")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2562")
def test_upload_for_all_video(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_video_hd_17MB.mp4"
                     ]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_all_for_video(file_list_dir)
    with allure.step("Validate API Response"):
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        assert len(json_data["data"]["videos"]) == 1
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"]["videos"][0]["videoName"]
        speed_time = get_upload_time(get_base_studio_api_url,
                                     current_date,
                                     "duration",
                                     file_name)
        file_size = get_upload_time(get_base_studio_api_url,
                                    current_date,
                                    "fileSize",
                                    file_name) / (1024 * 1024)
        logger.info(f"[Performance Metric][{current_date}] file name: {file_name}, file_size: {file_size:.2f} MB, "
                    f"speed_time: {speed_time} seconds")


@allure.title("[C2563] Upload Company Brand - All upload for mixed medias (music, image)")
@allure.description("Mixed Music & Image with format [mp3, JPEG]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2563")
def test_upload_for_all_mixed_media(reset_state_studio_video, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3",
                     f"{cwd}/test_data/logo_auto.jpeg"
                     ]
    with allure.step("Call API"):
        response = BrandKit(reset_state_studio_video).upload_all_list(file_list_dir)
    with allure.step("Validate API Response"):
        json_data = response.json()
        logger.info(f"[API Response] \n{response.text}")
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        assert len(json_data["data"]["musics"]) == 1
        assert len(json_data["data"]["images"]) == 1
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name_music = json_data["data"]["musics"][0]["videoName"]
        speed_time = get_upload_time(get_base_studio_api_url,
                                     current_date,
                                     "duration",
                                     file_name_music)

        file_size = get_upload_time(get_base_studio_api_url,
                                    current_date,
                                    "fileSize",
                                    file_name_music) / (1024 * 1024)
        logger.info(
            f"[Performance Metric][{current_date}] file name: {file_name_music}, file_size: {file_size:.2f} MB, "
            f"speed_time: {speed_time} seconds")

        file_name_image = json_data["data"]["images"][0]["videoName"]
        speed_time = get_upload_time(get_base_studio_api_url,
                                     current_date,
                                     "duration",
                                     file_name_image)

        file_size = get_upload_time(get_base_studio_api_url,
                                    current_date,
                                    "fileSize",
                                    file_name_image) / (1024 * 1024)
        logger.info(
            f"[Performance Metric][{current_date}] file name: {file_name_image}, file_size: {file_size:.2f} MB, "
            f"speed_time: {speed_time} seconds")
