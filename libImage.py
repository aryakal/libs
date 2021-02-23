import os
from PIL import Image
from datetime import datetime


class LibImage:

    @staticmethod
    def get_image_stat(image_path):
        with Image.open(image_path) as im:
            dict_info = im._getexif()
            if dict_info is not None and 36867 in dict_info:
                return datetime.strptime(dict_info[36867], "%Y:%m:%d %H:%M:%S")
            else:
                return None

    @staticmethod
    def get_all_media_from_folder(from_file_location_dir):
        out_files = []
        for root_dir, dir_names, file_names in os.walk(from_file_location_dir):
            for file_name in file_names:
                ext = os.path.splitext(file_name)[1].lower()
                if ext in [".jpg", ".jpeg", ".png",  # all images
                           ".mp4", ".avi"]:                  # all vedio
                    file_path = os.path.join(root_dir, file_name)
                    out_files.append(file_path)
        return out_files

    @staticmethod
    def helper_is_file_image(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        return ext in [".jpg", ".jpeg", ".png"]

    @staticmethod
    def helper_is_file_vid(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        return ext in [".mp4", ".avi"]






