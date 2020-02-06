import os
from app import account


def get_root_directory_path():
    return os.path.join(os.getcwd(), 'users_data')


def get_user_data_directory_path():
    return os.path.join(get_root_directory_path(), account.account_get_logged_in_user())


def get_user_photo_directory_path():
    return os.path.join(get_user_data_directory_path(), 'photos')


def get_user_thumbnail_directory_path():
    return os.path.join(get_user_data_directory_path(), 'thumbnails')


def create_root_directory():
    if not os.path.exists(get_root_directory_path()):
        os.mkdir(get_root_directory_path())


def create_user_data_directory():
    if not os.path.exists(get_user_data_directory_path()):
        os.mkdir(get_user_data_directory_path())


def create_user_photo_directory():
    if not os.path.exists(get_user_photo_directory_path()):
        os.mkdir(get_user_photo_directory_path())


def create_user_thumbnail_directory():
    if not os.path.exists(get_user_thumbnail_directory_path()):
        os.mkdir(get_user_thumbnail_directory_path())


def create_directory_if_necessary():
    create_root_directory()
    create_user_data_directory()
    create_user_photo_directory()
    create_user_thumbnail_directory()
