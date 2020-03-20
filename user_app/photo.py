import os

from flask import redirect, render_template, request, current_app, abort, jsonify
from user_app import webapp, account, main, image_processing
from common_lib import utility, database, s3


@webapp.route('/api/upload', methods=['POST'])
def photo_upload_handler():
    is_from_api = False
    username = request.form.get('username')
    password = request.form.get('password')
    if username is not None or password is not None:
        is_from_api = True
    print('is_from_api=' + str(is_from_api), flush=True)

    error_message = validate_user_and_input_format(request)
    if error_message is not None:
        if is_from_api:
            return error_message
        else:
            return main.main(user_welcome_args=main.UserWelcomeArgs(error_message=error_message))

    if not account.account_is_logged_in():
        error_message = 'Invalid Operation! You are not logged in!'
        if is_from_api:
            return error_message
        else:
            return render_template('empty_go_home.html', title='Error', message=error_message)

    error_message = process_and_save_image(request)

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
    original_filename = image.filename
    original_photo_file_bytes = image.read()

    # Register the photo in database
    photo_id = database.create_new_photo(account.account_get_logged_in_userid(), original_filename)
    if photo_id:
        # Get the new filename
        extension = utility.get_file_extension(original_filename)
        saved_filename = str(photo_id) + extension

        # Save the original photo
        original_photo_s3_key = s3.PHOTOS_DIR + saved_filename
        res = s3.upload_file_bytes_object(key=original_photo_s3_key, file_bytes=original_photo_file_bytes)
        assert res

        # Save the rectanged photo
        rectangled_photo_cv_bytes = image_processing.detect_and_draw_rectangles_on_cv_image(image_processing.convert_file_bytes_to_cv_bytes(original_photo_file_bytes))
        rectangled_photo_s3_key = s3.RECTANGLES_DIR + saved_filename
        rectangled_photo_file_bytes = image_processing.convert_cv_bytes_to_file_bytes(extension, rectangled_photo_cv_bytes)
        res = s3.upload_file_bytes_object(key=rectangled_photo_s3_key, file_bytes=rectangled_photo_file_bytes)
        assert res

        thumbnail_cv_bytes = image_processing.generate_thumbnail_for_cv_image(rectangled_photo_cv_bytes)
        thumbnail_s3_key = s3.THUMBNAILS_DIR + saved_filename
        thumbnail_file_bytes = image_processing.convert_cv_bytes_to_file_bytes(extension, thumbnail_cv_bytes)
        res = s3.upload_file_bytes_object(key=thumbnail_s3_key, file_bytes=thumbnail_file_bytes)
        assert res

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
    saved_photo_file_name = str(photo_id) + utility.get_file_extension(photo_name)
    photo_s3_key = s3.PHOTOS_DIR + saved_photo_file_name
    thumbnail_s3_key = s3.THUMBNAILS_DIR + saved_photo_file_name
    rectangle_s3_key = s3.RECTANGLES_DIR + saved_photo_file_name

    s3.delete_object(key=photo_s3_key)
    s3.delete_object(key=thumbnail_s3_key)
    s3.delete_object(key=rectangle_s3_key)

    database.delete_photo(photo_id)


def is_extension_allowed(filename):
    extension = utility.get_file_extension(filename)
    return extension and (extension in current_app.config['ALLOWED_IMAGE_EXTENSION'])


@webapp.route('/api/photo_display', methods=['POST'])
def display_photo_handler():
    # TODO: Also display the original file name
    if account.account_is_logged_in():
        photo_id_str = request.form.get('photo_id')

        result = database.get_photo(int(photo_id_str))
        if result:
            user_id, photo_name = result
            if user_id == account.account_get_logged_in_userid():
                saved_photo_file = photo_id_str + utility.get_file_extension(photo_name)

                rectangled_photo_url = s3.get_object_url(key=s3.RECTANGLES_DIR + saved_photo_file)
                rectangled_photo_size = s3.get_bucket_content_size(key=s3.RECTANGLES_DIR + saved_photo_file)[0]
                original_photo_url = s3.get_object_url(key=s3.PHOTOS_DIR + saved_photo_file)
                original_photo_size = s3.get_bucket_content_size(key=s3.PHOTOS_DIR + saved_photo_file)[0]

                if rectangled_photo_url and original_photo_url:
                    return render_template(
                        'display_photo.html', saved_photo_file=saved_photo_file,
                        photo_name=photo_name, photo_id=int(photo_id_str),
                        rectangled_photo_url=rectangled_photo_url,
                        original_photo_url=original_photo_url,
                        rectangled_photo_size=utility.convert_bytes_to_human_readable(rectangled_photo_size),
                        original_photo_size=utility.convert_bytes_to_human_readable(original_photo_size))

    return render_template('empty_go_home.html', title='Error', message='Please try again!')


@webapp.route('/api/render_thumbnail_gallery', methods=['POST'])
def render_thumbnail_gallery():
    return jsonify({'data': render_template('thumbnail_gallery.html', thumbnails=get_thumbnails())})


def get_thumbnails():
    '''
    [(photo_id_str, photo_name, thumbnail_url)]
    '''
    result = list()
    rows = database.get_account_photo(account.account_get_logged_in_userid())
    if rows:
        for photo_id, photo_name in rows:
            photo_id_str = str(photo_id)
            thumbnail_s3_key = s3.THUMBNAILS_DIR + photo_id_str + utility.get_file_extension(photo_name)
            thumbnail_url = s3.get_object_url(key=thumbnail_s3_key)
            if thumbnail_url:
                result.append((photo_id_str, photo_name, thumbnail_url))

    return result
