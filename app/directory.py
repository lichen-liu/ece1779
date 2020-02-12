import os


def get_static_dir_path():
    return os.path.join(os.getcwd(), 'static')


def get_yolo_dir_path():
        return os.path.join(os.getcwd(), 'yolo')


def get_root_dir_path(absolute=True):
    root_dir_name = 'data'
    if absolute:
        return os.path.join(get_static_dir_path(), root_dir_name)
    else:
        return root_dir_name


def get_photos_dir_path(absolute=True):
    if absolute:
        return os.path.join(get_root_dir_path(absolute), 'photos')
    else:
        return get_root_dir_path(absolute) + '/' + 'photos'


def get_thumbnails_dir_path(absolute=True):
    if absolute:
        return os.path.join(get_root_dir_path(absolute), 'thumbnails')
    else:
        return get_root_dir_path(absolute) + '/' + 'thumbnails'


def get_rectangles_dir_path(absolute=True):
    if absolute:
        return os.path.join(get_root_dir_path(absolute), 'rectangles')
    else:
        return get_root_dir_path(absolute) + '/' + 'rectangles'


def create_static_dir_if_necessary():
    if not os.path.exists(get_static_dir_path()):
        os.mkdir(get_static_dir_path())


def create_root_dir_if_necessary():
    if not os.path.exists(get_root_dir_path()):
        os.mkdir(get_root_dir_path())


def create_photos_dir_if_necessary():
    if not os.path.exists(get_photos_dir_path()):
        os.mkdir(get_photos_dir_path())


def create_thumbnails_dir_if_necessary():
    if not os.path.exists(get_thumbnails_dir_path()):
        os.mkdir(get_thumbnails_dir_path())


def create_rectangles_dir_if_necessary():
    if not os.path.exists(get_rectangles_dir_path()):
        os.mkdir(get_rectangles_dir_path())


def create_yolo_dir_if_necessary():
    if not os.path.exists(get_yolo_dir_path()):
        os.mkdir(get_yolo_dir_path())


def create_directories_if_necessary():
    create_static_dir_if_necessary()
    create_yolo_dir_if_necessary()
    create_root_dir_if_necessary()
    create_photos_dir_if_necessary()
    create_thumbnails_dir_if_necessary()
    create_rectangles_dir_if_necessary()
