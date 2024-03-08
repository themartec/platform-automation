import requests
from common.secret import MartecSecret


def get_download_time(base_url: str, time: str, info_to_get: str, file_name: str):
    url = f"{base_url}v1/track-upload?startTime={time}&type=export"
    print(f"+ [API Call] url: {url}")
    response = requests.request("GET", url,
                                headers=MartecSecret(url).get_martec_studio_api_header())

    print(f"+ [API Response] status_code={response.status_code}, text: {response.text}")
    if response.status_code == 200:
        res = response.json()
        res_data = res['data']
        for obj in res_data:
            tmp_data = obj['fileName']
            if file_name == tmp_data:
                print(f"    - info_to_get: {info_to_get}, expected_info: {file_name}, current_info: {tmp_data}")
                return obj[info_to_get]
        return None
    else:
        return None


def get_upload_time(base_url: str, time: str, info_to_get: str, file_name: str):
    url = f"{base_url}v1/track-upload?startTime={time}&type=upload"
    print(f"+ [API Call] url: {url}")
    response = requests.request("GET", url,
                                headers=MartecSecret(url).get_martec_studio_api_header())

    print(f"+ [API Response] status_code={response.status_code}, text: {response.text}")
    if response.status_code == 200:
        res = response.json()
        res_data = res['data']
        for obj in res_data:
            tmp_data = obj['fileName']
            if file_name == tmp_data:
                print(f"    - info_to_get: {info_to_get}, expected_info: {file_name}, current_info: {tmp_data}")
                return obj[info_to_get]
        return None
    else:
        return None

#
# a = get_download_time('https://studiostaging-api.themartec.com/',
#                     '2024-03-06',
#                     "duration",
#                     'what-tools-or-technologies-have-you-found-helpful-in-facilitating-remote-collaboration-29541024699131935.mp4')
# print(a)
