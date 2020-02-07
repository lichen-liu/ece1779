
import os
from flask import (redirect, render_template, request, url_for, current_app, abort)
#The handour says you CAN user MaxxMagic, I think it means we can use anything we want
# they will run loadtester, we better stick with the handout to avoid risks 
#from PIL import Image
from app import webapp, directory, account, main, utility


@webapp.route('/api/upload', methods=['POST'])
def photo_upload_handler():
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

    # Check file size
    cl = request.content_length
    MAX_FILE_SIZE = 5 * 1024 * 1024
    if cl is not None and cl > MAX_FILE_SIZE:
        if is_from_api:
            abort(413)
        else:
            return main.main(
                user_welcome_args=main.UserWelcomeArgs(
                    error_message='Error! File too large (' + utility.convert_bytes(cl) + '). It must be smaller than ' + utility.convert_bytes(MAX_FILE_SIZE) + '.'))

    photo_file = request.files['file']
    # Should change the filename, store the original name to sql
    # This is for both security and business logic consideration
    filename = photo_file.filename
    photo_file.save(os.path.join(directory.get_user_photos_dir_path(), filename))

    # thumbnail = get_thumbnail_for_image(photo_file)
    # thumbnail.save(os.path.join(directory.get_user_thumbnail_directory_path(), filename))
   
    return redirect('/')
    #return render_template('user_welcome.html',title='Photo Upload Successfully', username=account.account_get_logged_in_user())


# #Just use this for now, my friend
# #It crashes on my computer
# def get_thumbnail_for_image(image_file):
#     image = Image.open(image_file)
#     image.thumbnail(current_app.config["THUMBNAIL_SIZE"], Image.ANTIALIAS)
#     return image


def get_thumbnails():
    '''
    (user_thumbnails_dir_rel, [thumbnail_file])
    '''
    user_thumbnails_dir = directory.get_user_photos_dir_path()
    user_thumbnails_dir_rel = directory.get_user_photos_dir_path(False)

    # TODO: Also display the original file name
    return (user_thumbnails_dir_rel, [f for f in os.listdir(user_thumbnails_dir) if os.path.isfile(os.path.join(user_thumbnails_dir, f))])


@webapp.route('/api/photo_display', methods=['POST'])
def display_photo_handler():
    # TODO: Also display the original file name
    if account.account_is_logged_in():
        photo_file = request.form.get('photo_file')
        return render_template(
            'display_photo.html', photo_file=photo_file, photo_dir_path=directory.get_user_photos_dir_path(False))
    else:
        return render_template('empty_go_home.html', title='Error', message='Please try again!')

# Mock database for photos
# {file_id: (original_filename, user)}
photos = dict()