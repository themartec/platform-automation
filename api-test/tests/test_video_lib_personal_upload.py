import os
import logging
import pytest
import allure
from dotenv import load_dotenv

from src.martec_media_api import MartecMediaAPIRequest

cwd = os.getcwd()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def match_env(test_env: str):
    if test_env == "1":
        print(f"TEST_ENV=STAGING")
        base_url = "https://studiostaging-api.themartec.com/"
    elif test_env == "2":
        print(f"TEST_ENV=DEV")
        base_url = "https://studiodev-api.themartec.com/"
    else:
        print(f"TEST_ENV=PROD")
        base_url = ""
    return base_url


@pytest.fixture
def reset_state(request):
    print("\nPerforming set up...")
    load_dotenv()
    base_url = match_env(os.getenv('TEST_ENV'))
    MartecMediaAPIRequest(base_url).remove_media_ids("images")
    MartecMediaAPIRequest(base_url).remove_media_ids("videos")
    MartecMediaAPIRequest(base_url).remove_media_ids("audios")

    def finalizer():
        print("\nPerforming teardown...")
        MartecMediaAPIRequest(base_url).remove_media_ids("images")
        MartecMediaAPIRequest(base_url).remove_media_ids("videos")
        MartecMediaAPIRequest(base_url).remove_media_ids("audios")

    request.addfinalizer(finalizer)
    return base_url


@allure.title("[C2545] Upload Personal Media - Image upload for single [4K, 3.3MB, PNG] image ")
@allure.description("Image with format 4K, 3.3MB, PNG")
@allure.tag('C2545')
def test_upload_for_single_image(reset_state):
    response = MartecMediaAPIRequest(reset_state).post_media([f"{cwd}/test_data/sample_image_4k_01.png"], ['image/png'])
    data = response.json()
    logger.info(f" - api response as text: {response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(data) > 0
    assert data["message"] == "Response Success"
    img_obj = data["data"]
    assert len(img_obj) == 1
    img_obj = img_obj[0]
    assert int(img_obj["width"]) > 0
    assert int(img_obj["height"]) > 0


@allure.title("[C2544] Upload Personal Media - Image upload for multiple mixed images format ")
@allure.description("Mixed Image with format [JPEG, HD, 212KB], [PNG, 4K, 3.3MB], [GIF, HD, 8.7MB]")
@allure.tag("C2544")
def test_upload_for_multiple_images(reset_state):
    file_list_dir = [f"{cwd}/test_data/screen_auto.jpeg",
                     f"{cwd}/test_data/sample_image_4k_01.png",
                     f"{cwd}/test_data/gif_image_auto.gif"]
    media_list_type = ["image/jpeg", "image/png", "image/gif"]

    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    data = response.json()
    logger.info(f" - response as text: {response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(data) > 0
    assert data["message"] == "Response Success"
    assert len(data["data"]) == len(file_list_dir)


@allure.title("[C2546] Upload Personal Media - Video upload for single [4K, < 100MB, mp4] video")
@allure.description("Video with format MP4,4K,40MB")
@allure.tag("C2546")
def test_upload_for_single_video_below_100MB(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_4k_video_less100MB_03.mp4"]
    media_list_type = ["media/mp4"]
    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    file_size = int(json_data["data"][0]["fileSize"]) / 1048576
    logger.info(f'  - 1st Video Size: {file_size:.2f} MB')
    assert len(json_data["data"]) == len(file_list_dir)


@allure.title("[C2547] Upload Personal Media - Video upload for single [HD, > 100MB, mp4] video")
@allure.description("Video with format MP4,HD,132MB")
@allure.tag("C2547")
def test_upload_for_single_video_greater_than_100MB(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_hd_video_gr100MB.mp4"]
    media_list_type = ["media/mp4"]
    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    file_size = int(json_data["data"][0]["fileSize"]) / 1048576
    logger.info(f'  - 1st Video Size: {file_size:.2f} MB')
    assert len(json_data["data"]) == len(file_list_dir)


@allure.title("[C2548] Upload Personal Media - Video upload for single [HD, 17MB, mp4] video")
@allure.description("Video with format MP4, HD, 17MB")
@allure.tag("C2548")
def test_upload_for_single_video_17MB(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_video_hd_17MB.mp4"]
    media_list_type = ["media/mp4"]
    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    file_size = int(json_data["data"][0]["fileSize"]) / 1048576
    logger.info(f'  - 1st Video Size: {file_size:.2f} MB')
    assert len(json_data["data"]) == len(file_list_dir)


@allure.title("[C2549] Upload Personal Media - Video upload for multiple mixed videos")
@allure.description("Mixed Video with format [MOV, HD, 0.68MB], [MP4, HD, 45.89 MB]")
@allure.tag("C2549")
def test_upload_for_multiple_videos(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4",
                     f"{cwd}/test_data/sample_video_02.mov"]
    media_list_type = ["media/mp4", "media/mov"]
    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    logger.info(f'  - 1st Video Size: {int(json_data["data"][0]["fileSize"]) / 1048576:.2f} MB')
    logger.info(f'  - 2nd Video Size: {int(json_data["data"][1]["fileSize"]) / 1048576:.2f} MB')
    assert len(json_data["data"]) == len(file_list_dir)


@allure.title("[C2550] Upload Personal Media - Music upload for single [mp3, 1.01MB] music")
@allure.description("Music with format [mp3, 1.01MB]")
@allure.tag("C2550")
def test_upload_for_single_music(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3"]
    media_list_type = ["audio/mp3"]
    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    logger.info(f'  - 1st Music Size: {int(json_data["data"][0]["fileSize"]) / 1048576:.2f} MB')
    assert len(json_data["data"]) == len(file_list_dir)


@allure.title("[C2551] Upload Personal Media - Music upload for multiple mixed musics")
@allure.description("Mixed Music with format [mp3, 1.01MB],[aac, 3.87MB]")
@allure.tag("C2551")
def test_upload_for_multiple_musics(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3",
                     f"{cwd}/test_data/sample_aac_music_3.87mb.aac"]
    media_list_type = ["audio/mp3", "audio/aac"]
    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    logger.info(f'  - 1st Music Size: {int(json_data["data"][0]["fileSize"]) / 1048576:.2f} MB')
    logger.info(f'  - 1st Music Size: {int(json_data["data"][1]["fileSize"]) / 1048576:.2f} MB')
    assert len(json_data["data"]) == len(file_list_dir)


@allure.title("[C2552] Upload Personal Media - All upload for single [HD, 48MB, mp4] video")
@allure.description("Single Video Upload")
@allure.tag("C2552")
def test_upload_for_all_videos(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4"]
    media_list_type = ["media/mp4"]
    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    assert len(json_data["data"]) == 1


@allure.title("[C2553] Upload Personal Media - All upload for mixed medias (music, image & video)")
@allure.description("Mixed Music, Image & Video with format [mp3, JPEG, mp4]")
@allure.tag("C2553")
def test_upload_for_all_mixed_media(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3",
                     f"{cwd}/test_data/logo_auto.jpeg",
                     f"{cwd}/test_data/sample_video_hd_17MB.mp4",
                     ]
    media_list_type = ["audio/mp3", "image/jpeg", "media/mp4"]
    response = MartecMediaAPIRequest(reset_state).post_media(file_list_dir, media_list_type)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    assert len(json_data["data"]) == len(file_list_dir)
