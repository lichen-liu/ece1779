import os
from app import account


def get_static_dir_path():
    return os.path.join(os.getcwd(), 'static')


def get_root_dir_path(absolute=True):
    root_dir_name = 'users_data'
    if absolute:
        return os.path.join(get_static_dir_path(), root_dir_name)
    else:
        return root_dir_name


def get_user_dir_path(absolute=True):
    if absolute:
        return os.path.join(get_root_dir_path(absolute), account.account_get_logged_in_username())
    else:
        return get_root_dir_path(absolute) + '/' + account.account_get_logged_in_username()


def get_user_photos_dir_path(absolute=True):
    if absolute:
        return os.path.join(get_user_dir_path(absolute), 'photos')
    else:
        return get_user_dir_path(absolute) + '/' + 'photos'


def get_user_thumbnails_dir_path(absolute=True):
    if absolute:
        return os.path.join(get_user_dir_path(absolute), 'thumbnails')
    else:
        return get_user_dir_path(absolute) + '/' + 'thumbnails'


def get_user_rectangles_dir_path(absolute=True):
    if absolute:
        return os.path.join(get_user_dir_path(absolute), 'rectangles')
    else:
        return get_user_dir_path(absolute) + '/' + 'rectangles'


def get_yolo_dir_path(absolute=True):
    if absolute:
        return os.path.join(get_static_dir_path(), 'yolo')
    else:
        return get_static_dir_path() + '/' + 'yolo'


def create_static_dir_if_necessary():
    if not os.path.exists(get_static_dir_path()):
        os.mkdir(get_static_dir_path())


def create_root_dir_if_necessary():
    if not os.path.exists(get_root_dir_path()):
        os.mkdir(get_root_dir_path())


def create_user_dir_if_necessary():
    if not os.path.exists(get_user_dir_path()):
        os.mkdir(get_user_dir_path())


def create_user_photos_dir_if_necessary():
    if not os.path.exists(get_user_photos_dir_path()):
        os.mkdir(get_user_photos_dir_path())


def create_user_thumbnails_dir_if_necessary():
    if not os.path.exists(get_user_thumbnails_dir_path()):
        os.mkdir(get_user_thumbnails_dir_path())


def create_user_rectangles_dir_if_necessary():
    if not os.path.exists(get_user_rectangles_dir_path()):
        os.mkdir(get_user_rectangles_dir_path())


def create_yolo_dir_if_necessary():
    if not os.path.exists(get_yolo_dir_path()):
        os.mkdir(get_yolo_dir_path())


#Thinking abour calling this function before user login
def create_shared_if_necessary():
    create_static_dir_if_necessary()
    create_root_dir_if_necessary()


def create_user_directory_if_necessary():
    create_static_dir_if_necessary()
    create_yolo_dir_if_necessary()
    create_root_dir_if_necessary()
    create_user_dir_if_necessary()
    create_user_photos_dir_if_necessary()
    create_user_thumbnails_dir_if_necessary()
    create_user_rectangles_dir_if_necessary()
