
import os
import cv2, numpy
from flask import (redirect, render_template, request, url_for, current_app)
from app import webapp, directory, account, main
from urllib.parse import unquote_plus


@webapp.route('/api/upload', methods=['POST'])
def photo_upload_handler():
   # Get requests
   # NOT TESTED YET!
    username = request.form.get('username')
    password = request.form.get('password')
    if username is not None or password is not None:
        err_msg = account.account_login(username, password)
        if err_msg:
            return main.main_guest_welcome(username, password, err_msg)

    photo = request.files['file']
    # Should change the filename, store the original name to sql
    # This is for both security and business logic consideration
    filename = photo.filename
    photo_bytes = photo.read()
   
    generate_and_save_thumbnail_for_photo(photo_bytes, \
    os.path.join(directory.get_user_thumbnails_dir_path(), filename))

    save_photo_in_bytes(photo_bytes, \
    os.path.join(directory.get_user_photos_dir_path(), filename))
   
    return redirect('/')
    #return render_template('user_welcome.html',title='Photo Upload Successfully', username=account.account_get_logged_in_user())
def save_photo_in_bytes(photo_bytes, path):
    f = open(path, 'wb')
    f.write(photo_bytes)

def generate_and_save_thumbnail_for_photo(photo_bytes, path):
    cv_img = generate_thumbnail_for_photo(photo_bytes)
    cv2.imwrite(path, cv_img) 

def generate_thumbnail_for_photo(photo_bytes):
    numpy_img = numpy.fromstring(photo_bytes, numpy.uint8)
    cv_img = cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)
    return cv2.resize(cv_img,current_app.config["THUMBNAIL_SIZE"])

def get_thumbnails():
    '''
    (user_thumbnails_dir_rel, [thumbnail_file])
    '''
    user_thumbnails_dir = directory.get_user_thumbnails_dir_path()
    user_thumbnails_dir_rel = directory.get_user_thumbnails_dir_path(False)

    # TODO: Also display the original file name
    return (user_thumbnails_dir_rel, [f for f in os.listdir(user_thumbnails_dir) if os.path.isfile(os.path.join(user_thumbnails_dir, f))])

@webapp.route('/api/photo_display', methods=['POST'])
def display_photo_handler():
    # TODO: Also display the original file name
    if account.account_is_logged_in():
        photo_file = request.form.get('photo_file')
        #Escape html encoding using unquote_plus
        return render_template(
            'display_photo.html', photo_file=unquote_plus(photo_file), \
             photo_dir_path=directory.get_user_photos_dir_path(False))
    else:
        return render_template('empty_go_home.html', title='Error', message='Please try again!')

# Mock database for photos
# {file_id: (original_filename, user)}
photos = dict()