#from PIL import Image
import os

from flask import (flash, g, redirect, render_template, request, session,
                   url_for)

from app import account, webapp

size = (120,120)
users_photo_dir = os.path.join(os.path.join(os.getcwd(), '..'), 'users_photo')


@webapp.route('/api/upload', methods=['POST'])
def photo_upload_handler():
    user_photo_dir = os.path.join(users_photo_dir, account.account_get_logged_in_user())
    user_thumbnail_dir = os.path.join(user_photo_dir, 'thumbnails')

    photo_file = request.files['file']
    # filename here must be renamed, because we have to support user uploading different images with same name
    # This can be fixed by storing a mapping of file_id to file_name. Assign a new file_id, set path+file_id as filename
    filename = photo_file.filename

    if not os.path.exists(users_photo_dir):
        os.mkdir(users_photo_dir)
    if not os.path.exists(user_photo_dir):
        os.mkdir(user_photo_dir)
    if not os.path.exists(user_thumbnail_dir):
        os.mkdir(user_thumbnail_dir)
    photo_file.save(os.path.join(user_photo_dir, filename))

    # thumbnail = get_thumbnail_for_image(photo_file)
    # thumbnail.save(os.path.join(user_thumbnail_dir, filename))
    # return render_template('user_welcome.html',title='Photo Upload Successfully', username=account.account_get_logged_in_user())
    return redirect('/')


# def get_thumbnail_for_image(image_file):
#     image = Image.open(image_file)
#     image.thumbnail(size, Image.ANTIALIAS)
#     return image


# Mock database for photos
# {file_id: (original_filename, user)}
photos = dict()