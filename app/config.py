from datetime import timedelta


class Config(object):
    SECRET_KEY = 'NIDEMAMAMASHANGJIUYAOBAOZHALE'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes= 60 * 24)
    SESSION_REFRESH_EACH_REQUEST = True
    MAXIMUM_IMAGE_SIZE = 20 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSION = set(['.png', '.jpg', '.jpeg', '.gif']) # Lower case
    IMAGE_PROCESSING_CHOICE = 0
