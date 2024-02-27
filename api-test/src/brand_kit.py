from src.martec_api_method import MartecAPIRequest


class BrandKit:

    def __init__(self, base_url):
        self.base_url = f"{base_url}v1/brand-kit/"

    def remove_media(self):
        return MartecAPIRequest(self.base_url).remove_media()

    def upload_media_image(self, file_dir):
        return MartecAPIRequest(self.base_url).post_as_media(file_dir)

    def upload_image_list(self, file_list_dir):
        return MartecAPIRequest(self.base_url).post_as_images(file_list_dir)

    def upload_logos_list(self, file_list):
        return MartecAPIRequest(self.base_url).post_as_logos(file_list)

    def upload_video_list(self, file_list):
        return MartecAPIRequest(self.base_url).post_as_videos(file_list)

    def upload_music_list(self, file_list):
        return MartecAPIRequest(self.base_url).post_as_musics(file_list)

    def upload_all_list(self, file_list):
        return MartecAPIRequest(self.base_url).post_as_all(file_list)

    def upload_all_for_video(self, file_list):
        return MartecAPIRequest(self.base_url).post_as_all_for_video(file_list)
