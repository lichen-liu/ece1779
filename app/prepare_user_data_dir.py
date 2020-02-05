import os
from app import path

def create_photo_root():
    if not os.path.exists(path.get_root_data_directory_path()):
        os.mkdir(path.get_root_data_directory_path())

def create_user_data_root_directory():
    if not os.path.exists(path.get_user_data_directory_path()):
        os.mkdir(path.get_user_data_directory_path())

def craete_user_photo_directory():
    if not os.path.exists(path.get_user_photo_directory_path()):
        os.mkdir(path.get_user_photo_directory_path())

def craete_user_thumbnail_directory():
    if not os.path.exists(path.get_user_thumbnail_directory_path()):
        os.mkdir(path.get_user_thumbnail_directory_path())