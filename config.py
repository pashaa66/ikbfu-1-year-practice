import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "ikbfu_secret_key"

    BASE_IMAGE_PATH = os.path.join(basedir, "static", "img")

    REALTOR_IMAGE_PATH = os.path.join(BASE_IMAGE_PATH, "realtor")
    ANNOUNCEMENT_IMAGE_PATH = os.path.join(BASE_IMAGE_PATH, "announcement")

    UPLOAD_FOLDER = BASE_IMAGE_PATH
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
