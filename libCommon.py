import os
import logging
import hashlib
import time
import zipfile
from datetime import datetime


class LibCommon:
    def __init__(self):
        pass

    @staticmethod
    def version():
        return "0.1", datetime(2021, 2, 22)

    @staticmethod
    def init_logging(level=logging.INFO, file_path=None, fmt="[%(levelname)-5s], %(asctime)s, %(name)8s, %(message)s"):
        logging.getLogger("service").setLevel(logging.INFO)
        logging.getLogger("pyHS100.protocol").setLevel(logging.INFO)
        LibCommon.helper_logging_stop("urllib3.connectionpool")
        
        handlers = [logging.StreamHandler()]
        
        if file_path is not None:
            path_dir, path_file = os.path.split(file_path)
            LibCommon.helper_create_directory(path_dir)
            handlers.append(logging.FileHandler(file_path))
            
        logging.basicConfig(
            level=level,
            format=fmt,
            handlers=handlers
        )

    @staticmethod
    def init_logging_without_file(level=logging.DEBUG):
        LibCommon.init_logging(level)

    @staticmethod
    def helper_logging_stop(name):
        url_logger = logging.getLogger(name)
        url_logger.setLevel(logging.ERROR)

    @staticmethod
    def helper_create_directory(dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def helper_remove_empty_dirs(root_dir_path):
        if not os.path.isdir(root_dir_path):
            return
        logger = logging.getLogger("libCommon")
        items = os.listdir(root_dir_path)
        logger.debug("scan {:5d} {}".format(len(items), root_dir_path))
        if len(items) == 0:
            logger.debug("del {}".format(root_dir_path))
            try:
                os.rmdir(root_dir_path)
            except:
                logger.error("Cannot delete folder {}".format(root_dir_path))
        else:
            for item in items:
                path = os.path.join(root_dir_path, item)
                if os.path.isdir(path):
                    LibCommon.helper_remove_empty_dirs(path)\

            items = os.listdir(root_dir_path)
            if len(items) == 0:
                logger.debug("del {}".format(root_dir_path))
                try:
                    os.rmdir(root_dir_path)
                except:
                    logger.error("Cannot delete folder {}".format(root_dir_path))

    @staticmethod
    def helper_current_time():
        return datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]

    @staticmethod
    def helper_current_utc_time():
        dt = datetime.utcnow()
        return "{}T{}Z".format(dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S"))

    @staticmethod
    def get_current_time():
        return LibCommon.get_time(datetime.now())

    @staticmethod
    def get_time(dt):
        return dt.strftime("%Y%m%d-%H%M%S-%f")[:-3]

    @staticmethod
    def parse_time(str_dt):
        return datetime.strptime(str_dt, "%Y%m%d-%H%M%S-%f")

    @staticmethod
    def get_current_day():
        return LibCommon.get_day(datetime.now())

    @staticmethod
    def get_day(dt):
        return dt.strftime("%Y%m%d")

    @staticmethod
    def get_media_file_extensions():
        return [".jpg", ".mp4"]

    @staticmethod
    def helper_is_media_file_ext(ext):
        return ext in [".jpg", ".mp4"]

    @staticmethod
    def helper_get_hash_md5(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            return hashlib.md5(data).hexdigest()

    @staticmethod
    def helper_get_hash_sha1(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            return hashlib.sha1(data).hexdigest()

    @staticmethod
    def convert_file_size_to_str(size):
        if size >= 1024 * 1024 * 1024:
            return "%0.02f GB" % (size / (1024 * 1024 * 1024))
        elif size >= 1024 * 1024:
            return "%0.02f MB" % (size / (1024 * 1024))
        elif size >= 1024:
            return "%0.02f KB" % (size / 1024)
        else:
            return "%0.02f bt" % (size / 1.0)

    @staticmethod
    def hack_wait():
        while True:
            time.sleep(3600)

    @staticmethod
    def helper_zip_files(path, file_paths, logger=None):
        zip_file = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
        for file_path, suggested_path in file_paths:
            zip_file.write(file_path,
                           suggested_path)
            if logger is not None:
                logger.debug("zip: {}".format(suggested_path))
        zip_file.close()

    @staticmethod
    def helper_unzip_all(zip_file_path, out_path):
        LibCommon.helper_create_directory(out_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zipObj:
            zipObj.extractall(out_path)

    @staticmethod
    def helper_get_all_files(dir_path):
        out_files = []
        for root_dir, dir_paths, file_names in os.walk(dir_path):
            for file_name in file_names:
                file_path = os.path.join(root_dir, file_name)
                out_files.append((file_path, file_name))
        return out_files

    @staticmethod
    def helper_get_all_files_with_ext(dir_path, ext):
        out_files = []
        for root_dir, dir_paths, file_names in os.walk(dir_path):
            for file_name in file_names:
                if file_name.lower().endswith(ext):
                    file_path = os.path.join(root_dir, file_name)
                    out_files.append((file_path, file_name))
        return out_files



