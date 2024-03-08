class ENDPOINT:

    def __init__(self, env_id):
        self.env_id = env_id

    def mapping_endpoint_martec_api(self):
        if self.env_id == '1':
            env_name = 'staging'
        else:
            env_name = 'dev'

        return f"https://api{env_name}.themartec.com/"

    def mapping_endpoint_studio_api(self):
        if self.env_id == '1':
            env_name = 'staging'
        else:
            env_name = 'dev'
        return f"https://studio{env_name}-api.themartec.com/"

