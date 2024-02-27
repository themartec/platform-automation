import json
from common.secret import MartecSecret
import requests


def get_header(url):
    return {'Authorization': MartecSecret(url).get_token_for_brand_kit_tab_api()}


def post_as_logo_brand_kit(url, file_list_dir):
    payload = {}
    files = []
    for file in file_list_dir:
        files.append(('logos', (file, open(file, 'rb'), f'image/{file.split(".")[-1]}')))

    response = requests.request("POST", url, headers=get_header(url), data=payload, files=files)
    print(f"[API Response] status_code={response.status_code}, text: {response.text}")
    return response


class MartecAPIRequestFromBrandKitTab:

    def __init__(self, base_url):
        self.base_url = base_url

    def remove_logo(self):
        print(f"    - put: {self.base_url}")
        headers_rem = {'Authorization': MartecSecret(self.base_url).get_token_for_brand_kit_tab_api(), 'Content-Type': 'application/json'}
        payload = json.dumps({"logos": [],
                              "fonts": [],
                              "colors": []})
        response = requests.request("PUT", self.base_url, headers=headers_rem, data=payload)
        print(f"[API Response] status_code={response.status_code}, text: {response.text}")

        return response

    def post_as_logo_in_brand_kit_tab(self, file_list_dir):
        media_url = f"{self.base_url}logos"
        print(f"   - post: {media_url}")
        print(f"   - file_list_dir: {file_list_dir}")
        return post_as_logo_brand_kit(media_url, file_list_dir)
