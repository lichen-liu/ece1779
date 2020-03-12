import os
import pathlib


def get_static_dir_path():
    return os.path.join(str(pathlib.Path(__file__).parent.absolute()), 'static')


def get_yolo_dir_path():
    return os.path.join(str(pathlib.Path(__file__).parent.absolute()), 'yolo')


def create_static_dir_if_necessary():
    if not os.path.exists(get_static_dir_path()):
        os.mkdir(get_static_dir_path())


def create_yolo_dir_if_necessary():
    if not os.path.exists(get_yolo_dir_path()):
        os.mkdir(get_yolo_dir_path())


def create_directories_if_necessary():
    create_static_dir_if_necessary()
    create_yolo_dir_if_necessary()
