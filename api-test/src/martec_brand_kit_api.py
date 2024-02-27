import json
import requests
from common.secret import MartecSecret


def get_header(url):
    return MartecSecret(url).get_martec_header()


def get_header_custom(url):
    if "staging" in url:
        headers = {'Authorization': MartecSecret(url).get_martec_token(), 'Content-Type': 'application/json'}
    elif "dev" in url:
        headers = {'Authorization': MartecSecret(url).get_martec_token(), 'Content-Type': 'application/json'}
    else:
        headers = ""
    return headers


def post_multi_images(url, file_list_dir):
    payload = {}
    files = []
    for file in file_list_dir:
        files.append(('images', (file, open(file, 'rb'), f'image/{file.split(".")[-1]}')))

    response = requests.request("POST", url, headers=get_header(url), data=payload, files=files)
    print(f"[API Response] status_code={response.status_code}, text: {response.text}")

    return response


def post_as_logos(url, file_list_dir):
    payload = {}
    files = []
    for file in file_list_dir:
        files.append(('logos', (file, open(file, 'rb'), f'image/{file.split(".")[-1]}')))

    response = requests.request("POST", url, headers=get_header(url), data=payload, files=files)
    print(f"[API Response] status_code={response.status_code}, text: {response.text}")
    return response


def post_as_videos(url, file_list_dir):
    payload = {}
    files = []
    for file in file_list_dir:
        files.append(('videos', (file, open(file, 'rb'), f'video/{file.split(".")[-1]}')))
    response = requests.request("POST", url, headers=get_header(url), data=payload, files=files)
    print(f"[API Response] status_code={response.status_code}, text: {response.text}")
    return response


def post_as_musics(url, file_list_dir):
    payload = {}
    files = []
    for file in file_list_dir:
        files.append(('musics', (file, open(file, 'rb'), f'audio/mpeg')))
    response = requests.request("POST", url, headers=get_header(url), data=payload, files=files)
    print(f"[API Response] status_code={response.status_code}, text: {response.text}")
    return response


def post_as_all_custom(url, file_list_dir):
    # mp3 must be first
    payload = {}
    files = [('alls', (file_list_dir[0], open(file_list_dir[0], 'rb'), 'audio/mpeg')),
             ('alls', (file_list_dir[1], open(file_list_dir[1], 'rb'), 'image/jpeg'))]

    response = requests.request("POST", url, headers=get_header(url), data=payload, files=files)
    print(f"[API Response] status_code={response.status_code}, text: {response.text}")
    return response


def post_as_all_for_video(url, file_list_dir):
    # mp3 must be first
    payload = {}
    files = [('alls', (file_list_dir[0], open(file_list_dir[0], 'rb'), f'video/{file_list_dir[0].split(".")[-1]}'))]

    response = requests.request("POST", url, headers=get_header(url), data=payload, files=files)
    print(f"[API Response] status_code={response.status_code}, text: {response.text}")
    return response


class MartecBrandKitAPIRequest:

    def __init__(self, base_url):
        self.base_url = base_url

    def remove_media(self):
        print(f"    - put: {self.base_url}")
        headers_rem = get_header_custom(self.base_url)
        payload = json.dumps({
            "videos": [],
            "images": [],
            "logos": [],
            "musics": []
        })
        response = requests.request("PUT", self.base_url, headers=headers_rem, data=payload)
        print(f"[API Response] status_code={response.status_code}, text: {response.text}")

        return response

    def post_as_images(self, file_list_dir):
        media_url = f"{self.base_url}upload-images"
        print(f"   - post: {media_url}")
        print(f"   - file_list_dir: {file_list_dir}")
        return post_multi_images(media_url, file_list_dir)

    def post_as_logos(self, file_list_dir):
        media_url = f"{self.base_url}upload-logos"
        print(f"   - post: {media_url}")
        print(f"   - file_list_dir: {file_list_dir}")
        return post_as_logos(media_url, file_list_dir)

    def post_as_videos(self, file_list_dir):
        media_url = f"{self.base_url}upload-videos"
        print(f"   - post: {media_url}")
        print(f"   - file_list_dir: {file_list_dir}")
        return post_as_videos(media_url, file_list_dir)

    def post_as_musics(self, file_list_dir):
        media_url = f"{self.base_url}upload-musics"
        print(f"   - post: {media_url}")
        print(f"   - file_list_dir: {file_list_dir}")
        return post_as_musics(media_url, file_list_dir)

    def post_as_all(self, file_list_dir):
        media_url = f"{self.base_url}upload-alls"
        print(f"   - post: {media_url}")
        print(f"   - file_list_dir: {file_list_dir}")
        return post_as_all_custom(media_url, file_list_dir)

    def post_as_all_for_video(self, file_list_dir):
        media_url = f"{self.base_url}upload-alls"
        print(f"   - post: {media_url}")
        print(f"   - file_list_dir: {file_list_dir}")
        return post_as_all_for_video(media_url, file_list_dir)
