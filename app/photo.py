import os
import numpy
import cv2

# Get rid of warning messages
import sys
stderr = sys.stderr
stdout = sys.stdout
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
sys.stderr = open(os.devnull, 'w')
sys.stdout = open(os.devnull, 'w')
sys.stdwarn = open(os.devnull, 'w')
import cvlib as cv
sys.stderr = stderr
sys.stdout = stdout

from flask import redirect, render_template, request, current_app, abort, jsonify
from app import webapp, directory, account, main, utility, ibr_queue, batch_task_helper, yolo_net, database, image_pool_runner


@webapp.route('/api/upload', methods=['POST'])
def photo_upload_handler():
    is_from_api = False
    username = request.form.get('username')
    password = request.form.get('password')
    if username is not None or password is not None:
        is_from_api = True
    print('is_from_api=' + str(is_from_api))

    error_message = validate_user_and_input_format(request)
    if error_message is not None:
        if is_from_api:
            return error_message
        else:
            return main.main(user_welcome_args=main.UserWelcomeArgs(error_message=error_message))

    image_processing_choice = webapp.config.get('IMAGE_PROCESSING_CHOICE')
    if image_processing_choice == 0:
        # Per-request version
        error_message = process_and_save_image(request)
    elif image_processing_choice == 1:
        # image_batch_runner version
        error_message = try_enqueue_ibr_task(request)
    elif image_processing_choice == 2:
        # image_pool_runner version
        error_message = try_enqueue_ipr_task(request)
    else:
        assert(False)

    if error_message is not None:
        if is_from_api:
            return error_message
        else:
            return main.main(user_welcome_args=main.UserWelcomeArgs(error_message=error_message))

    if is_from_api:
        return '/api/upload successful!'
    else:
        return redirect('/')


def validate_user_and_input_format(request):
    # Get requests
    # NOT TESTED YET!
    username = request.form.get('username')
    password = request.form.get('password')
    if username is not None or password is not None:
        err_msg = account.account_login(username, password)
        if err_msg:
            return err_msg

    content_length = request.content_length
    if content_length is not None and content_length > current_app.config['MAXIMUM_IMAGE_SIZE']:
        return 'Error! File too large (' + utility.convert_bytes_to_human_readable(content_length) + \
            '). It must be smaller than ' + \
            utility.convert_bytes_to_human_readable(
                current_app.config['MAXIMUM_IMAGE_SIZE']) + '.'

    if request.files.get('file') is None or request.files['file'].filename == '':
        return 'No file was uploaded'
    if is_extension_allowed(request.files['file'].filename) is not True:
        return 'File extension is not allowed'


def process_and_save_image(request):
    image = request.files['file']
    file_name = image.filename
    photo_bytes = image.read()

    # Register the photo in database
    photo_id = database.create_new_photo(
        account.account_get_logged_in_userid(), file_name)
    if photo_id:
        # Get the new filename
        saved_file_name = str(photo_id) + utility.get_file_extension(file_name)

        # Save the original photo
        origin_photo_path = os.path.join(
            directory.get_photos_dir_path(), saved_file_name)
        save_bytes_img(photo_bytes, origin_photo_path)

        # Save the rectanged photo
        rectangled_photo = draw_rectangles_on_photo(photo_bytes)
        rectangled_photo_path = os.path.join(
            directory.get_rectangles_dir_path(), saved_file_name)
        batch_task_helper.save_cv_img(rectangled_photo, rectangled_photo_path)

        thumbnail = batch_task_helper.generate_thumbnail_for_cv_img(
            rectangled_photo)
        thumbnail_path = os.path.join(
            directory.get_thumbnails_dir_path(), saved_file_name)
        batch_task_helper.save_cv_img(thumbnail, thumbnail_path)
    else:
        return 'Server has encountered a problem with database when storing the photo'


@webapp.route('/api/delete_photo', methods=['POST'])
# Handler to delete photo
def delete_photo_handler():
    photo_id = request.form.get('photo_id')
    error_message = delete_photo(photo_id)

    if error_message:
        return render_template('empty_go_home.html', title='Error', message=error_message)
    else:
        return redirect('/')


def delete_photo(photo_id):
    '''
    Return error_message if errored; otherwise None
    '''
    if not account.account_is_logged_in():
        return 'Please try again!'
    
    # Verify session
    res = database.get_photo(photo_id)
    if not res:
        return 'Photo does not exist!'
    userid, photo_name = res
    if userid != account.account_get_logged_in_userid():
        return 'Operation is not allowed!'

    print('Deleting ', photo_id, photo_name)
    saved_photo_file = str(photo_id) + utility.get_file_extension(photo_name)
    photo_path = os.path.join(directory.get_photos_dir_path(), saved_photo_file)
    thumbnail_path = os.path.join(directory.get_thumbnails_dir_path(), saved_photo_file)
    rectangle_path = os.path.join(directory.get_rectangles_dir_path(), saved_photo_file)

    if os.path.exists(photo_path):
        os.remove(photo_path)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
    if os.path.exists(rectangle_path):
        os.remove(rectangle_path)

    database.delete_photo(photo_id)


def draw_rectangles_on_photo(photo_bytes):
    cv_img = decode_bytes_to_cv_image(photo_bytes)
    cv_img_list = []
    cv_img_list.append(cv_img)
    net = yolo_net.new_yolo_net()
    boxes, descriptions = batch_task_helper.detect_objects_on_images(
        cv_img_list, net)
    return batch_task_helper.draw_rectangles(cv_img, boxes[0], descriptions[0])


def decode_bytes_to_cv_image(photo_bytes):
    numpy_img = numpy.fromstring(photo_bytes, numpy.uint8)
    return cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)


def try_enqueue_ipr_task(request):
    image = request.files['file']
    file_name = image.filename
    photo_bytes = image.read()

    # Register the photo in database
    photo_id = database.create_new_photo(account.account_get_logged_in_userid(), file_name)
    if photo_id:
        # Get the new filename
        saved_file_name = str(photo_id) + utility.get_file_extension(file_name)

        # Save the original photo
        origin_photo_path = os.path.join(directory.get_photos_dir_path(), saved_file_name)
        save_bytes_img(photo_bytes, origin_photo_path)

        # Add to the task queue
        is_successful = image_pool_runner.send_image_task_to_pool(*prepare_task(saved_file_name))
        if not is_successful:
            if os.path.exists(origin_photo_path):
                os.remove(origin_photo_path)
            database.delete_photo(photo_id)
            return 'Server are handling too many requests, please try again later'
    else:
        return 'Server has encountered a problem with database when storing the photo'


def try_enqueue_ibr_task(request):
    image = request.files['file']
    file_name = image.filename
    photo_bytes = image.read()
    task_queue = ibr.queue.get_queue()

    with task_queue.acquire_lock() as acquired:
        if(acquired):
            if not task_queue.is_full():
                # Register the photo in database
                photo_id = database.create_new_photo(
                    account.account_get_logged_in_userid(), file_name)
                if photo_id:
                    # Get the new filename
                    saved_file_name = str(photo_id) + \
                        utility.get_file_extension(file_name)

                    # Add to the task queue
                    is_successful = task_queue.add(ibr_queue.Task(*prepare_task(saved_file_name)))
                    assert is_successful

                    # Save the original photo
                    origin_photo_path = os.path.join(
                        directory.get_photos_dir_path(), saved_file_name)
                    save_bytes_img(photo_bytes, origin_photo_path)
                else:
                    return 'Server has encountered a problem with database when storing the photo'
            else:
                return 'Server are handling too many requests, please try again later'
        else:
            return 'Server are overloaded, please try again later'


def prepare_task(file_name):
    source_path = os.path.join(directory.get_photos_dir_path(), file_name)
    thumbnail_dest_path = os.path.join(directory.get_thumbnails_dir_path(), file_name)
    rectangled_dest_path = os.path.join(directory.get_rectangles_dir_path(), file_name)
    return (source_path, thumbnail_dest_path, rectangled_dest_path)


def is_extension_allowed(file_name):
    extension = utility.get_file_extension(file_name)
    return extension and (extension in current_app.config['ALLOWED_IMAGE_EXTENSION'])


def save_bytes_img(photo_bytes, path):
    f = open(path, 'wb')
    f.write(photo_bytes)


@webapp.route('/api/photo_display', methods=['POST'])
def display_photo_handler():
    # TODO: Also display the original file name
    if account.account_is_logged_in():
        photo_id_str = request.form.get('photo_id')

        result = database.get_photo(int(photo_id_str))
        if result:
            _, photo_name = result
            saved_photo_file = photo_id_str + \
                utility.get_file_extension(photo_name)

            return render_template(
                'display_photo.html', saved_photo_file=saved_photo_file,
                photo_name=photo_name, photo_id=int(photo_id_str),
                processed_photo_dir=directory.get_rectangles_dir_path(False),
                original_photo_dir=directory.get_photos_dir_path(False))

    return render_template('empty_go_home.html', title='Error', message='Please try again!')


@webapp.route('/api/render_thumbnail_gallery', methods=['POST'])
def render_thumbnail_gallery():
    print('Received Refresh')
    return jsonify({'data': render_template('thumbnail_gallery.html', thumbnail_dir_path=directory.get_thumbnails_dir_path(False), thumbnails=get_thumbnails())})


def get_thumbnails():
    '''
    [(photo_id_str, file_extension, photo_name)]
    '''

    user_thumbnails_dir = directory.get_thumbnails_dir_path()

    result = list()
    rows = database.get_account_photo(account.account_get_logged_in_userid())
    if rows:
        for photo_id, photo_name in rows:
            extension = utility.get_file_extension(photo_name)
            photo_id_str = str(photo_id)
            if os.path.exists(os.path.join(user_thumbnails_dir, photo_id_str + extension)):
                result.append((photo_id_str, extension, photo_name))

    return result
