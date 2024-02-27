from src.martec_brand_kit_tab_api import MartecAPIRequestFromBrandKitTab


class BrandKitTab:

    def __init__(self, base_url):
        self.base_url = f"{base_url}v1/studio/brand-kit/"

    def remove_logo_brand_kit_tab(self):
        return MartecAPIRequestFromBrandKitTab(self.base_url).remove_logo()

    def upload_logo_brand_kit_tab(self, file_list):
        return MartecAPIRequestFromBrandKitTab(self.base_url).post_as_logo_in_brand_kit_tab(file_list)