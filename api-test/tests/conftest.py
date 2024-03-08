import pytest
from src.martec_media_api import MartecMediaAPIRequest
from src.brand_kit_tab import BrandKitTab
from src.brand_kit import BrandKit
from common.endpoint import ENDPOINT


@pytest.fixture(scope="function")
def set_up_tear_down(request) -> str:
    pass


@pytest.fixture(scope="function")
def get_base_studio_api_url(request) -> str:
    test_env = get_env_from_command(request)
    return ENDPOINT(test_env).mapping_endpoint_studio_api()


def pytest_addoption(parser):
    parser.addoption("--env_id", action="store")


def get_env_from_command(request):
    name_value = request.config.option.env_id
    if name_value is None:
        print(f"end_id is not defined !")
        # pytest.skip()
        raise Exception('end_id is not defined !')
    return name_value


@pytest.fixture(scope="function")
def reset_state(request):
    print("\nPerforming set up...")
    end_id = get_env_from_command(request)
    base_url = ENDPOINT(end_id).mapping_endpoint_studio_api()
    martec_media = MartecMediaAPIRequest(base_url)
    martec_media.remove_media_ids("images")
    martec_media.remove_media_ids("videos")
    martec_media.remove_media_ids("audios")

    def finalizer():
        print("\nPerforming teardown...")
        martec_media.remove_media_ids("images")
        martec_media.remove_media_ids("videos")
        martec_media.remove_media_ids("audios")

    request.addfinalizer(finalizer)
    return base_url


@pytest.fixture(scope="function")
def reset_state_brand_kit_tab(request) -> str:
    print("\nPerforming set up...")
    end_id = get_env_from_command(request)
    base_url = ENDPOINT(end_id).mapping_endpoint_martec_api()
    print(f"[SET UP] base_url: {base_url}")
    brand_kit_page = BrandKitTab(base_url)
    brand_kit_page.remove_logo_brand_kit_tab()

    def finalizer():
        print("\nPerforming teardown...")
        print(f"[TEAR DOWN] base_url: {base_url}")
        brand_kit_page.remove_logo_brand_kit_tab()

    request.addfinalizer(finalizer)
    return base_url


@pytest.fixture
def reset_state_studio_video(request):
    print("\nPerforming set up...")
    end_id = get_env_from_command(request)
    base_url = ENDPOINT(end_id).mapping_endpoint_studio_api()
    print(f"[SET UP] base_url: {base_url}")
    brand_kit_page = BrandKit(base_url)
    brand_kit_page.remove_media_in_video_lib()

    def finalizer():
        print("\nPerforming teardown...")
        print(f"[TEAR DOWN] base_url: {base_url}")
        brand_kit_page.remove_media_in_video_lib()

    request.addfinalizer(finalizer)

    return base_url
