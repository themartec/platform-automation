import requests
from common_src.secret import MartecSecret


def get_header(url):
    return MartecSecret(url).get_martec_header()


def post_medias(url, file_list_dir, media_list_type):
    payload = {}
    files = []
    for idx, file in enumerate(file_list_dir):
        files.append(('files', (file, open(file, 'rb'), media_list_type[idx])))

    print(f"files: {files}")
    response = requests.request("POST", url, headers=get_header(url), data=payload, files=files)
    print(f"    - [API Response] status_code={response.status_code}, text: {response.text}")

    return response


def get_medias(url, data_type):
    # print(f"url: {url}, header: {get_header(url)}")
    id_list = []
    response = requests.request("GET", url, headers=get_header(url))
    json_data = response.json()
    media_list = json_data['data'][data_type]
    for media in media_list:
        id_list.append(media["id"])
    return id_list


class MartecMediaAPIRequest:

    def __init__(self, base_url):
        self.base_url = f"{base_url}v1/media"

    def get_media_ids_by_type(self, media_type):
        media_url = f"{self.base_url}"
        print(f"   - get: {media_url}")
        id_list = get_medias(media_url, media_type)
        print(f"    - media_type: {media_type}, id_list: {id_list}")
        return id_list

    def remove_media_id(self, media_id):
        base_url = f"{self.base_url}/{media_id}"
        print(f"    - delete: {base_url}, media_id: {media_id}")
        headers_rem = MartecSecret(base_url).get_header_with_content_type()
        response = requests.request("DELETE", base_url, headers=headers_rem)
        print(f"    - [API Response] status_code={response.status_code}, text: {response.text}")

        return response

    def remove_media_ids(self, media_type):
        ids = self.get_media_ids_by_type(media_type)
        for id_code in ids:
            self.remove_media_id(id_code)
        print(f"    - Remove For {media_type} is completed with removed media is {len(ids)}")

    def post_media(self, file_list_dir, media_list_type):
        media_url = f"{self.base_url}"
        print(f"   - post: {media_url}")
        print(f"   - file_list_dir: {file_list_dir}")
        print(f"   - media_list_type: {media_list_type}")
        return post_medias(media_url, file_list_dir, media_list_type)
