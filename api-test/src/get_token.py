import json

import requests
from dotenv import load_dotenv

load_dotenv()


def get_token_from_account_for_studio(base_url):
    if 'staging' in base_url:
        endpoint = "https://apistaging.themartec.com:443/v1/studio/login"
    else:
        endpoint = "https://apidev.themartec.com:443/v1/studio/login"
    payload = json.dumps(
        {"email": "huong.trinh@themartec.com",
         "password": "AutoOfMartec@1234"})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", endpoint, headers=headers, data=payload)
    # print(f"    - [API Response][Token Get] status_code={response.status_code}, text: {response.text}")
    return 'Bearer ' + response.json()["data"]["token"]


def get_token_from_account_for_martec_api(base_url):
    if 'staging' in base_url:
        endpoint = "https://apistaging.themartec.com:443/v1/auth/login"
    else:
        endpoint = "https://apidev.themartec.com:443/v1/auth/login"
    payload = json.dumps(
        {"email": "huong.trinh@themartec.com",
         "password": "AutoOfMartec@1234"})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", endpoint, headers=headers, data=payload)
    token = 'Bearer ' + response.json()["data"]["token"]
    # print(f"    - [API Response][Token Get Martec] status_code={response.status_code}, token: {token}")
    return token
