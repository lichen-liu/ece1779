from datetime import timedelta

class Config(object):
    SECRET_KEY = 'NIDEMAMAMASHANGJIUYAOBAOZHALE'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes = 100)
    SESSION_REFRESH_EACH_REQUEST = True
    THUMBNAIL_SIZE = (120,120)
    MAXIMUM_IMAGE_SIZE = 20 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSION = set(['.png', '.jpg', '.jpeg', '.gif'])
    USE_IMAGE_BATCH_RUNNER = False