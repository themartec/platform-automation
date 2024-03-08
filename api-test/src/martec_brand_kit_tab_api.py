import json
from common.secret import MartecSecret
import requests



class MartecAPIRequestFromBrandKitTab:

    def __init__(self, base_url):
        self.base_url = base_url
        self.secret = MartecSecret(self.base_url)

    def remove_logo(self):
        print(f"[remove_logo] put: {self.base_url}")
        headers_rem = self.secret.get_martec_header_with_content_type()
        payload = json.dumps({"logos": [],
                              "fonts": [],
                              "colors": []})
        print(f"[remove_logo] headers_rem: {headers_rem}")
        response = requests.request("PUT", self.base_url, headers=headers_rem, data=payload)
        print(f"[API Response][remove_logo] status_code={response.status_code}, text: {response.text}")

        return response

    def post_as_logo_in_brand_kit_tab(self, file_list_dir):
        media_url = f"{self.base_url}logos"
        print(f"[post_as_logo_in_brand_kit_tab] post: {media_url}")
        print(f"[post_as_logo_in_brand_kit_tab] file_list_dir: {file_list_dir}")
        payload = {}
        files = []
        for file in file_list_dir:
            files.append(('logos', (file, open(file, 'rb'), f'image/{file.split(".")[-1]}')))

        header = self.secret.get_martec_header_without_content_type()

        response = requests.request("POST", media_url, headers=header, data=payload, files=files)
        print(f"[API Response][post_as_logo_brand_kit] status_code={response.status_code}, text: {response.text}")
        return response
