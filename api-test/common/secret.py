from src.get_token import get_token_from_account_for_studio, get_token_from_account_for_martec_api


class MartecSecret:

    def __init__(self, base_url):
        self.base_url = base_url
        self.token_studio = get_token_from_account_for_studio(self.base_url)
        self.token_martec = get_token_from_account_for_martec_api(self.base_url)

    def get_martec_studio_api_header(self):
        return {'Authorization': self.token_studio}

    def get_martec_studio_api_header_with_content_type(self):
        return {'Authorization': self.token_studio,
                'Content-Type': 'application/json'}

    def get_martec_header_with_content_type(self):
        return {'Authorization': self.token_martec,
                'Content-Type': 'application/json'}

    def get_martec_header_without_content_type(self):
        return {'Authorization': self.token_martec}