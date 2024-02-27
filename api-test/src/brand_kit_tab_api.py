import json

import requests

bear_token_brand_kit = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFIVnZibWN1ZEhKcGJtaEFkR2hsYldGeWRHVmpMbU52YlE9PSIsImF1dGhfaWQiOiIzZDc3M2E2Ni02ZjM2LTRlN2ItYjAxNi1kZjZmMjNiYzBjN2UiLCJjb21wYW55X2lkIjoiYzJiZWExZDktNDhmYS00YTQ1LThkMDgtM2NjNDAwNGU3ODY0IiwiY29tcGFueV9uYW1lIjoiVGhlIE1hcnRlYyIsImF1ZCI6IkJyb3dzZXIiLCJjcmVhdGVkX2F0IjoiMjAyNC0wMi0xOVQxMzo1MToyMS42MjdaIiwicGxhdGZvcm0iOiJFTVBMT1lFUiIsImlhdCI6MTcwODkyMDMyMSwiZXhwIjoxNzA5MDA2NzIxfQ.rt_0BSxKWaMiuLAsyXOKAu7YeaXSejESGlNS0uMcVXQ'

headers_brand_kit = {'Authorization': bear_token_brand_kit}


def post_as_logo_brand_kit(url, file_list_dir):
    payload = {}
    files = []
    for file in file_list_dir:
        files.append(('logos', (file, open(file, 'rb'), f'image/{file.split(".")[-1]}')))

    response = requests.request("POST", url, headers=headers_brand_kit, data=payload, files=files)
    print(f"[API Response] status_code={response.status_code}, text: {response.text}")
    return response


class MartecAPIRequest_BrandKitTab:

    def __init__(self, base_url):
        self.base_url = base_url

    def remove_logo(self):
        print(f"    - put: {self.base_url}")
        headers_rem = {'Authorization': bear_token_brand_kit, 'Content-Type': 'application/json'}
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
