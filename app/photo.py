
import os
#OpenCV imports
import cv2, numpy
import cvlib as cv
from cvlib.object_detection import draw_bbox
#Flask imports
from flask import (redirect, render_template, request, url_for, current_app, abort, jsonify)
from app import webapp, directory, account, main, utility, queue, batch_task_helper, yolo_net
#Url utility imports
from urllib.parse import unquote_plus


@webapp.route('/api/upload', methods=['POST'])
def photo_upload_handler():
    error_message = validate_user_and_input_format(request)
    if error_message is not None:
        return main.main(user_welcome_args=main.UserWelcomeArgs(error_message=error_message))

    #Batch processing version
    error_message = try_enqueue_task(request)
    if error_message is not None:
        return main.main(user_welcome_args=main.UserWelcomeArgs(error_message=error_message))

    #Per-request version
    #process_and_save_image(request)

    return redirect('/')


def validate_user_and_input_format(request):
    # Get requests
    # NOT TESTED YET!
    is_from_api = False
    username = request.form.get('username')
    password = request.form.get('password')
    if username is not None or password is not None:
        err_msg = account.account_login(username, password)
        if err_msg:
            abort(401)
        else:
            is_from_api = True

    content_length = request.content_length
    if content_length is not None and content_length > current_app.config['MAXIMUM_IMAGE_SIZE']:
        if is_from_api:
            abort(413)
        else:
            return 'Error! File too large (' + utility.convert_bytes(content_length) + \
            '). It must be smaller than ' + utility.convert_bytes(current_app.config['MAXIMUM_IMAGE_SIZE']) + '.'

    if request.files.get('file') is None or request.files['file'].filename == '':
        return 'No file was uploaded'
    if is_extension_allowed(request.files['file'].filename) is not True:
        return 'File extension is not allowed'

def process_and_save_image(request):
    image = request.files['file']
    file_name = image.filename
    photo_bytes = image.read()

    origin_photo_path = os.path.join(directory.get_user_photos_dir_path(), file_name)
    save_bytes_img(photo_bytes, origin_photo_path)

    rectangled_photo = draw_rectangles_on_photo(photo_bytes)
    rectangled_photo_path = os.path.join(directory.get_user_rectangles_dir_path(), file_name)
    batch_task_helper.save_cv_img(rectangled_photo, rectangled_photo_path)

    thumbnail = generate_thumbnail_for_cv_img(rectangled_photo)
    thumbnail_path = os.path.join(directory.get_user_thumbnails_dir_path(), file_name)
    batch_task_helper.save_cv_img(thumbnail, thumbnail_path)

def draw_rectangles_on_photo(photo_bytes):
    cv_img = decode_bytes_to_cv_image(photo_bytes)
    cv_img_list = []
    cv_img_list.append(cv_img) 
    net = yolo_net.new_yolo_net()
    boxes, descriptions = batch_task_helper.detect_objects_on_images(cv_img_list, net)
    return batch_task_helper.draw_rectangles(cv_img, boxes[0], descriptions[0])

def decode_bytes_to_cv_image(photo_bytes):
    numpy_img = numpy.fromstring(photo_bytes, numpy.uint8)
    return cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)

def generate_thumbnail_for_cv_img(cv_img):
    return cv2.resize(cv_img,current_app.config["THUMBNAIL_SIZE"])


def try_enqueue_task(request):
    image = request.files['file']
    file_name = image.filename
    photo_bytes = image.read()
    task_queue = queue.get_queue()

    with task_queue.acquire_lock() as acquired:
        if(acquired):
            succeeded = task_queue.add(prepare_task(file_name))
            if(succeeded):
                origin_photo_path = os.path.join(directory.get_user_photos_dir_path(), file_name)
                save_bytes_img(photo_bytes, origin_photo_path)
            else:
                return "Server are handling too many requests, please try again later"
        else:
            return "Server are overloaded, please try again later"


def prepare_task(file_name):
     source_dir = directory.get_user_photos_dir_path() + '/' + file_name
     thumbnail_dest_dir = directory.get_user_thumbnails_dir_path() + '/' + file_name
     rectangled_dest_dir = directory.get_user_rectangles_dir_path() + '/' + file_name
     return queue.Task(source_dir, thumbnail_dest_dir, rectangled_dest_dir)


def is_extension_allowed(file_name):
    return '.' in file_name and file_name.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_IMAGE_EXTENSION']
   

def save_bytes_img(photo_bytes, path):
    f = open(path, 'wb')
    f.write(photo_bytes)


@webapp.route('/api/photo_display', methods=['POST'])
def display_photo_handler():
    # TODO: Also display the original file name
    if account.account_is_logged_in():
        photo_file = request.form.get('photo_file')
        #Escape html encoding using unquote_plus
        return render_template(
            'display_photo.html', photo_file=unquote_plus(photo_file), \
             processed_photo_dir = directory.get_user_rectangles_dir_path(False), \
             original_photo_dir = directory.get_user_photos_dir_path(False))
    else:
        return render_template('empty_go_home.html', title='Error', message='Please try again!')

@webapp.route('/api/render_thumbnail_gallery', methods=['POST'])
def render_thumbnail_gallery():
    print("received")
    user_thumbnails_dir_rel, thumbnails = get_thumbnails()
    return jsonify({'data': render_template('thumbnail_gallery.html', thumbnail_dir_path = user_thumbnails_dir_rel, thumbnails = thumbnails)})

def get_thumbnails():
    '''
    (user_thumbnails_dir_rel, [thumbnail_file])
    '''
    user_thumbnails_dir = directory.get_user_thumbnails_dir_path()
    user_thumbnails_dir_rel = directory.get_user_thumbnails_dir_path(False)

    # TODO: Also display the original file name
    return (user_thumbnails_dir_rel, [f for f in os.listdir(user_thumbnails_dir) if os.path.isfile(os.path.join(user_thumbnails_dir, f))])


# Mock database for photos
# {file_id: (original_filename, user)}
photos = dict()