import os
from app import account

def get_relative_user_root_path_in_static():
    return os.path.join('users_data/', account.account_get_logged_in_user())

def get_relative_user_photo_path_in_static():
    return os.path.join(get_relative_user_root_path_in_static(), 'photos')

def get_relative_user_thumbnail_path_in_static():
    return os.path.join(get_relative_user_root_path_in_static(), 'thumbnails')

def get_absolute_path_to_static_folder():
    return os.path.join(os.getcwd(), 'app/static')

def get_root_data_directory_path():
    return os.path.join(get_absolute_path_to_static_folder(), 'users_data')

def get_user_data_directory_path():
    return os.path.join(get_absolute_path_to_static_folder(), get_relative_user_root_path_in_static())

def get_user_photo_directory_path():
    return os.path.join(get_absolute_path_to_static_folder(), get_relative_user_photo_path_in_static())

def get_user_thumbnail_directory_path():
    return os.path.join(get_absolute_path_to_static_folder(), get_relative_user_thumbnail_path_in_static())

