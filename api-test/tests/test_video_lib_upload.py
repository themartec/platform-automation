import os
import logging
import pytest
import allure
from dotenv import load_dotenv
from src.brand_kit import BrandKit

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

    BrandKit(base_url).remove_media()

    def finalizer():
        print("\nPerforming teardown...")
        BrandKit(base_url).remove_media()

    request.addfinalizer(finalizer)

    return base_url


@allure.title("Studio - Upload Single Image")
@allure.description("Image with format PNG")
def test_upload_for_SINGLE_image(reset_state):
    file_name = "shrimp_auto"
    file_list_dir = [f"{cwd}/test_data/{file_name}.png"]
    response = BrandKit(reset_state).upload_image_list(file_list_dir)
    data = response.json()
    logger.info(f" - api response as text: {response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(data) > 0
    assert data["message"] == "Response Success"
    img_obj = data["data"]["images"]
    assert len(img_obj) == 1, "Validate uploading for one media only"
    img_obj = img_obj[0]
    assert file_name in str(img_obj["imageName"])
    assert str(img_obj["Link"]) != ""
    # logger.info(f" - size of image: {img_obj["width"]}x{img_obj["height"]}")
    assert int(img_obj["width"]) > 0
    assert int(img_obj["height"]) > 0


@allure.title("Studio - Upload Multiple Images")
@allure.description("Mixed Image with format JPEG, PNG, GIF")
def test_upload_for_multiple_images(reset_state):
    file_list_dir = [f"{cwd}/test_data/screen_auto.jpeg",
                     f"{cwd}/test_data/shrimp_auto.png",
                     f"{cwd}/test_data/gif_image_auto.gif"]

    response = BrandKit(reset_state).upload_image_list(file_list_dir)
    data = response.json()
    logger.info(f" - response as text: {response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(data) > 0
    assert data["message"] == "Response Success"
    assert len(data["data"]["images"]) == len(file_list_dir), "Validate uploading for one media only"


@allure.title("Studio - Upload Multiple Logos")
@allure.description("Mixed Logos with format JPEG, PNG")
def test_upload_for_multiple_logos(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_logo_01.jpeg", f"{cwd}/test_data/sample_logo_02.png"]
    response = BrandKit(reset_state).upload_logos_list(file_list_dir)
    data = response.json()
    logger.info(f" - response as text: {response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(data) > 0
    assert data["message"] == "Response Success"
    assert len(data["data"]) == len(file_list_dir)


@allure.title("Studio - Upload Single Video")
@allure.description("Video with format MP4, 45.89 MB")
def test_upload_for_single_video(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4"]
    response = BrandKit(reset_state).upload_video_list(file_list_dir)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    file_size = int(json_data["data"]["videos"][0]["fileSize"]) / 1048576
    logger.info(f'  - 1st Video Size: {file_size:.2f} MB')
    assert len(json_data["data"]["videos"]) == len(file_list_dir)


@allure.title("Studio - Upload Multiple Videos")
@allure.description("Mixed Video with format [MOV, 0.68MB], [MP4, 45.89 MB]")
def test_upload_for_multiple_videos(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4",
                     f"{cwd}/test_data/sample_video_02.mov"]
    response = BrandKit(reset_state).upload_video_list(file_list_dir)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    logger.info(f'  - 1st Video Size: {int(json_data["data"]["videos"][0]["fileSize"]) / 1048576:.2f} MB')
    logger.info(f'  - 2nd Video Size: {int(json_data["data"]["videos"][1]["fileSize"]) / 1048576:.2f} MB')
    assert len(json_data["data"]["videos"]) == len(file_list_dir)


@allure.title("Studio - Upload Single Music")
@allure.description("Music with format [mp3, 1.01MB]")
def test_upload_for_single_music(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3"]
    response = BrandKit(reset_state).upload_music_list(file_list_dir)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    logger.info(f'  - 1st Music Size: {int(json_data["data"]["musics"][0]["fileSize"]) / 1048576:.2f} MB')
    assert len(json_data["data"]["musics"]) == len(file_list_dir)


@allure.title("Studio - Upload Multiple Musics")
@allure.description("Mixed Music with format [mp3, 1.01MB, 5.07MB]")
def test_upload_for_multiple_musics(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3",
                     f"{cwd}/test_data/sample_music_02.mp3"]
    response = BrandKit(reset_state).upload_music_list(file_list_dir)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    logger.info(f'  - 1st Music Size: {int(json_data["data"]["musics"][0]["fileSize"]) / 1048576:.2f} MB')
    logger.info(f'  - 1st Music Size: {int(json_data["data"]["musics"][1]["fileSize"]) / 1048576:.2f} MB')
    assert len(json_data["data"]["musics"]) == len(file_list_dir)


@allure.title("Studio - Upload From All Tab For Video")
@allure.description("Single Video Upload")
def test_upload_for_all_video(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_video_01.mp4"
                     ]
    response = BrandKit(reset_state).upload_all_for_video(file_list_dir)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    assert len(json_data["data"]["videos"]) == 1


@allure.title("Studio - Upload From All Tab For Mixed Media")
@allure.description("Mixed Music & Image with format [mp3, JPEG]")
def test_upload_for_all_mixed_media(reset_state):
    file_list_dir = [f"{cwd}/test_data/sample_music_01.mp3",
                     f"{cwd}/test_data/logo_auto.jpeg"
                     ]
    response = BrandKit(reset_state).upload_all_list(file_list_dir)
    json_data = response.json()
    logger.info(f" - response as text:\n{response.text}")
    assert response.status_code == 201  # Validation of status code
    assert len(json_data) > 0
    assert json_data["message"] == "Response Success"
    assert len(json_data["data"]["musics"]) == 1
    assert len(json_data["data"]["images"]) == 1


