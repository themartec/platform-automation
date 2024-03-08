from src.martec_brand_kit_tab_api import MartecAPIRequestFromBrandKitTab


class BrandKitTab:
    base_url = ""

    def __init__(self, base_url):
        self.base_url = f"{base_url}v1/studio/brand-kit/"
        self.martec_api = MartecAPIRequestFromBrandKitTab(self.base_url)

    def remove_logo_brand_kit_tab(self):
        return self.martec_api.remove_logo()

    def upload_logo_brand_kit_tab(self, file_list):
        return self.martec_api.post_as_logo_in_brand_kit_tab(file_list)
