import requests
from common.secret import MartecSecret


def post_medias(secret, url, file_list_dir, media_list_type):
    payload = {}
    files = []
    for idx, file in enumerate(file_list_dir):
        files.append(('files', (file, open(file, 'rb'), media_list_type[idx])))

    # print(f"files: {files}")
    response = requests.request("POST", url, headers=secret.get_martec_studio_api_header(), data=payload, files=files)
    print(f"    - [API Response][post_medias] status_code={response.status_code}, text: {response.text}")

    return response


def get_medias(secret, url, data_type):
    id_list = []
    response = requests.request("GET", url, headers=secret.get_martec_studio_api_header())
    json_data = response.json()
    print(f"    - [API Response][get_medias] status_code={response.status_code}, json_data: {json_data}")
    media_list = json_data['data'][data_type]
    for media in media_list:
        id_list.append(media["id"])
    return id_list


class MartecMediaAPIRequest:

    def __init__(self, base_url):
        self.base_url = f"{base_url}v1/media"
        self.secret = MartecSecret(self.base_url)

    def get_media_ids_by_type(self, media_type):
        media_url = f"{self.base_url}"
        id_list = get_medias(self.secret, media_url, media_type)
        print(f"   - get_media_ids_by_type: {media_url},\nmedia_type: {media_type}, id_list: {id_list}")
        return id_list

    def remove_media_id(self, media_id):
        base_url = f"{self.base_url}/{media_id}"
        print(f"    - [remove_media_id] delete: {base_url}, media_id: {media_id}")
        headers_rem = self.secret.get_martec_studio_api_header_with_content_type()
        response = requests.request("DELETE", base_url, headers=headers_rem)
        print(f"    - [API Response][remove_media_id] status_code={response.status_code}, text: {response.text}")

        return response

    def remove_media_ids(self, media_type):
        ids = self.get_media_ids_by_type(media_type)
        for id_code in ids:
            self.remove_media_id(id_code)
        print(f"    - [remove_media_ids] Remove For {media_type} is completed with removed media is {len(ids)}")

    def post_media(self, file_list_dir, media_list_type):
        media_url = f"{self.base_url}"
        print(f"   - [post_media] post: {media_url}, file_list_dir: {file_list_dir}, media_list_type:"
              f" {media_list_type}")
        return post_medias(self.secret, media_url, file_list_dir, media_list_type)
