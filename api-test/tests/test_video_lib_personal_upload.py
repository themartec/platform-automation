import os
import logging
import allure

from src.martec_media_api import MartecMediaAPIRequest
from common.date import get_date_as_yyyymmdd
from src.get_studio_upload_download_info import get_upload_time

cwd = os.getcwd()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@allure.title("[C2545] Upload Personal Media - Image upload for single [4K, 3.3MB, PNG] image ")
@allure.description("Image with format 4K, 3.3MB, PNG")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2545")
def test_upload_for_single_image(reset_state, get_base_studio_api_url):
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media([f"{cwd}/test_data/sample_image_4k_01.png"],
                                                                 ['image/png'])
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(data) > 0
        assert data["message"] == "Response Success"
        img_obj = data["data"]
        assert len(img_obj) == 1
        img_obj = img_obj[0]
        assert int(img_obj["width"]) > 0
        assert int(img_obj["height"]) > 0
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = img_obj["name"]
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


@allure.title("[C2544] Upload Personal Media - Image upload for multiple mixed images format ")
@allure.description("Mixed Image with format [JPEG, HD, 212KB], [PNG, 4K, 3.3MB], [GIF, HD, 8.7MB]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2544")
def test_upload_for_multiple_images(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/screen_auto.jpeg",
                     f"{cwd}/test_data/sample_image_4k_01.png",
                     f"{cwd}/test_data/gif_image_auto.gif"]
    media_list_type = ["image/jpeg", "image/png", "image/gif"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(data) > 0
        assert data["message"] == "Response Success"
        assert len(data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = data["data"][0]["name"]
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


@allure.title("[C2546] Upload Personal Media - Video upload for single [4K, < 100MB, mp4] video")
@allure.description("Video with format MP4,4K,40MB")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2546")
def test_upload_for_single_video_below_100MB(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_4k_video_less100MB_03.mp4"]
    media_list_type = ["media/mp4"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        json_data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        file_size = int(json_data["data"][0]["fileSize"]) / 1048576
        logger.info(f'  - 1st Video Size: {file_size:.2f} MB')
        assert len(json_data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"][0]["name"]
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


@allure.title("[C2547] Upload Personal Media - Video upload for single [HD, > 100MB, mp4] video")
@allure.description("Video with format MP4,HD,132MB")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2547")
def test_upload_for_single_video_greater_than_100MB(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_hd_video_gr100MB.mp4"]
    media_list_type = ["media/mp4"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        json_data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        file_size = int(json_data["data"][0]["fileSize"]) / 1048576
        logger.info(f'  - 1st Video Size: {file_size:.2f} MB')
        assert len(json_data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"][0]["name"]
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


@allure.title("[C2548] Upload Personal Media - Video upload for single [HD, 17MB, mp4] video")
@allure.description("Video with format MP4, HD, 17MB")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2548")
def test_upload_for_single_video_17MB(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_video_hd_17MB.mp4"]
    media_list_type = ["media/mp4"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        json_data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        file_size = int(json_data["data"][0]["fileSize"]) / 1048576
        logger.info(f'  - 1st Video Size: {file_size:.2f} MB')
        assert len(json_data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"][0]["name"]
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


@allure.title("[C2549] Upload Personal Media - Video upload for multiple mixed videos")
@allure.description("Mixed Video with format [MOV, HD, 0.68MB], [MP4, HD, 45.89 MB]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2549")
def test_upload_for_multiple_videos(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4",
                     f"{cwd}/test_data/sample_video_02.mov"]
    media_list_type = ["media/mp4", "media/mov"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        json_data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        logger.info(f'  - 1st Video Size: {int(json_data["data"][0]["fileSize"]) / 1048576:.2f} MB')
        logger.info(f'  - 2nd Video Size: {int(json_data["data"][1]["fileSize"]) / 1048576:.2f} MB')
        assert len(json_data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"][0]["name"]
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


@allure.title("[C2550] Upload Personal Media - Music upload for single [mp3, 1.01MB] music")
@allure.description("Music with format [mp3, 1.01MB]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2550")
def test_upload_for_single_music(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3"]
    media_list_type = ["audio/mp3"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        json_data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        logger.info(f'  - 1st Music Size: {int(json_data["data"][0]["fileSize"]) / 1048576:.2f} MB')
        assert len(json_data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"][0]["name"]
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


@allure.title("[C2551] Upload Personal Media - Music upload for multiple mixed musics")
@allure.description("Mixed Music with format [mp3, 1.01MB],[aac, 3.87MB]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2551")
def test_upload_for_multiple_musics(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3",
                     f"{cwd}/test_data/sample_aac_music_3.87mb.aac"]
    media_list_type = ["audio/mp3", "audio/aac"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        json_data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        logger.info(f'  - 1st Music Size: {int(json_data["data"][0]["fileSize"]) / 1048576:.2f} MB')
        logger.info(f'  - 1st Music Size: {int(json_data["data"][1]["fileSize"]) / 1048576:.2f} MB')
        assert len(json_data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"][0]["name"]
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


@allure.title("[C2552] Upload Personal Media - All upload for single [HD, 48MB, mp4] video")
@allure.description("Single Video Upload")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2552")
def test_upload_for_all_videos(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4"]
    media_list_type = ["media/mp4"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        json_data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        assert len(json_data["data"]) == 1
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"][0]["name"]
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


@allure.title("[C2553] Upload Personal Media - All upload for mixed medias (music, image & video)")
@allure.description("Mixed Music, Image & Video with format [mp3, JPEG, mp4]")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}C2553")
def test_upload_for_all_mixed_media(reset_state, get_base_studio_api_url):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3",
                     f"{cwd}/test_data/logo_auto.jpeg",
                     f"{cwd}/test_data/sample_video_hd_17MB.mp4",
                     ]
    media_list_type = ["audio/mp3", "image/jpeg", "media/mp4"]
    with allure.step("Call API"):
        response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
        logger.info(f"[API Response] \n{response.text}")
    with allure.step("Validate API Response"):
        json_data = response.json()
        assert response.status_code == 201  # Validation of status code
        assert len(json_data) > 0
        assert json_data["message"] == "Response Success"
        assert len(json_data["data"]) == len(file_list_dir)
    with allure.step("Performance Metric"):
        current_date = get_date_as_yyyymmdd()
        file_name = json_data["data"][0]["name"]
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
