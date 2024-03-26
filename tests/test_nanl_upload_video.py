import csv
import logging
import time
import allure
import os
import pandas as pd
import pytest
from datetime import datetime
from playwright.sync_api import BrowserContext

from common_src.pages.nanl import NoAppNoLoginPage
from utils.setup_before_test_nanl_upload import remove_file, init_csv_file_with_column

COMMON_STEP_NAME_01 = "Access Invited Collecttion Link"
cwd = os.getcwd()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

network_ref = "https://themartec.atlassian.net/wiki/spaces/AQ/pages/92045436/Network+Speed+References"
# Mbps -> byte/s
network_conditions = {
    'Network As Default Setting': {
    },
    'US Avg Fixed Broadband Network Speed': {
        'download': (237.41 * 125000),
        'upload': (28.55 * 125000),
        'latency': 13,
    },
    'US Avg Mobile Network Speed': {
        'download': (115.40 * 125000),
        'upload': (9.85 * 125000),
        'latency': 29,
    },
    'UK Avg Fixed Broadband Network Speed': {
        'download': (95.95 * 125000),
        'upload': (26.17 * 125000),
        'latency': 13,
    },
    'UK Avg Mobile Network Speed': {
        'download': (52.33 * 125000),
        'upload': (7.51 * 125000),
        'latency': 34,
    },
    'AU Avg Fixed Broadband Network Speed': {
        'download': (54.69 * 125000),
        'upload': (18.39 * 125000),
        'latency': 11,
    },
    'AU Avg Mobile Network Speed': {
        'download': (82.88 * 125000),
        'upload': (8.53 * 125000),
        'latency': 22,
    },
    'VN Avg Fixed Broadband Network Speed': {
        'download': (47.23 * 125000),
        'upload': (19.67 * 125000),
        'latency': 23,
    },
    'VN Avg Mobile Network Speed': {
        'download': (108.22 * 125000),
        'upload': (101.07 * 125000),
        'latency': 3,
    },
    'Fast 3G Network Speed': {
        'download': 180000,  # 1440 Kbps
        'upload': 84375,  # 675 Kbps
        'latency': 150,  # 150 ms
    }
}


def init_network_config(context: BrowserContext, condition):
    if condition == "Network As Default Setting":
        page = context.new_page()
        return page
    page = context.new_page()
    cdpSession = context.new_cdp_session(page)
    cdpSession.send("Network.emulateNetworkConditions", {
        'downloadThroughput': network_conditions[condition]['download'],
        'uploadThroughput': network_conditions[condition]['upload'],
        'latency': network_conditions[condition]['latency'],
        'offline': False
    })
    return page


def write_data(filename, data_row):
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data_row)


def calculate_avg_speed(file_name, env_name):
    with open(os.getenv("SPEED_PERFORMANCE_FILE"), 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Test Env", "Time", "Network Config", "Average Upload Speed"])

    with (open(file_name) as file_obj):
        df = pd.read_csv(file_obj)
        configs_list = ["Network As Default Setting",
                        "US Avg Fixed Broadband Network Speed",
                        "US Avg Mobile Network Speed",
                        "UK Avg Fixed Broadband Network Speed",
                        "UK Avg Mobile Network Speed",
                        "AU Avg Fixed Broadband Network Speed",
                        "AU Avg Mobile Network Speed",
                        "VN Avg Fixed Broadband Network Speed",
                        "VN Avg Mobile Network Speed"]

        total_speed = 0
        count = 0
        for config in configs_list:
            print(f"config: {config}")
            for idx, row in df.iterrows():
                if row["Network Config"] == config:
                    total_speed = row["Upload Speed"] + total_speed
                    count = count + 1

            avg_speed = round(total_speed / count, 2)
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("avg_speed.csv", 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([env_name, date_time, config, avg_speed])
            print(f"total_speed: {total_speed}, count: {count}, avg_speed: {avg_speed}")


# @pytest.mark.skip(reason="Feature is being updated")
@allure.title("[C2645] NANL - Upload Video In Multiple Configured Network")
@allure.description(f"Ref: {network_ref}")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2645")
@pytest.mark.parametrize("network_condition", network_conditions.keys())
def test_nanl_upload_video_under_network_conditions(get_env, set_up_tear_down_with_network_profile,
                                                    get_base_url,
                                                    network_condition
                                                    ):
    logger.info(f"network_condition: {network_condition}")
    logger.info(f"Details:\n{network_conditions[network_condition]}")
    FILE_NAME_01 = "upload_history.csv"
    FILE_NAME_02 = "avg_speed.csv"
    remove_file(FILE_NAME_01)
    remove_file(FILE_NAME_02)
    init_csv_file_with_column(["Time", "Network Config", "Upload Speed"], "upload_history.csv")

    with allure.step(f"Start browser with configure of {network_condition}"):
        context = set_up_tear_down_with_network_profile
        page = init_network_config(context, network_condition)
        tested_url = (
            f"{get_base_url}story/collection-link/The-Evolution-of-Test-Automation:-Test-For-Upload-Video-From"
            f"-Invited-Link/nP38VQK4doTAGmRV")
        page.goto(tested_url)
        time.sleep(5)
    with allure.step("Access No App No Login and Upload"):
        print(f"{cwd}")
        file_name_dir = f"{cwd}/test_data/media/1min_4k_22MB.mp4"
        assert os.path.exists(file_name_dir)
        no_app = NoAppNoLoginPage(page)
        no_app.tick_on_check_box_of_term()
        no_app.click_on_start_button()
        no_app.click_on_next_button()
        upload_time = no_app.set_file_name_to_upload(file_name_dir)

        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"[Write Data] cur_time: {cur_time}, network_condition: {network_condition}, upload_time: {upload_time}")
        write_data("upload_history.csv", [cur_time, network_condition, upload_time])
        calculate_avg_speed("upload_history.csv", get_env)

    with allure.step("Validate Uploaded Time Should Be Less Than 120 seconds"):
        print(f"Upload Time: {upload_time} (-1 means it took more than 2 minutes)")
        assert -1 < upload_time < 61
