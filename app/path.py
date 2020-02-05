import os
from app import account

def get_root_data_directory_path():
    return os.path.join(os.getcwd(), 'users_data')

def get_user_data_directory_path():
    return os.path.join(get_root_data_directory_path(), account.account_get_logged_in_user())

def get_user_photo_directory_path():
    return os.path.join(get_user_data_directory_path(), 'photos')

def get_user_thumbnail_directory_path():
    return os.path.join(get_user_data_directory_path(), 'thumbnails')