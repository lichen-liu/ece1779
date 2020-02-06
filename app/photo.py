
import os
from flask import (redirect, render_template, request, url_for, current_app)
#The handour says you CAN user MaxxMagic, I think it means we can use anything we want
# they will run loadtester, we better stick with the handout to avoid risks 
#from PIL import Image
from app import webapp, directory, account
from urllib.parse import unquote_plus


@webapp.route('/api/upload', methods=['POST'])
def photo_upload_handler():
   
    photo_file = request.files['file']
    filename = photo_file.filename
    photo_file.save(os.path.join(directory.get_user_photos_dir_path(), filename))

    # thumbnail = get_thumbnail_for_image(photo_file)
    # thumbnail.save(os.path.join(directory.get_user_thumbnail_directory_path(), filename))
   
    return redirect('/')
    #return render_template('user_welcome.html',title='Photo Upload Successfully', username=account.account_get_logged_in_user())


# #Just use this for now, my friend
# # it crashes on my computer
# def get_thumbnail_for_image(image_file):
#     image = Image.open(image_file)
#     image.thumbnail(current_app.config["THUMBNAIL_SIZE"], Image.ANTIALIAS)
#     return image


@webapp.route('/api/thumbnail_display', methods=['POST'])
def display_thumbnails():

    all_user_thumbnails = os.listdir(directory.get_user_photos_dir_path())

    return render_template('thumbnail_display.html', \
    thumbnails = all_user_thumbnails, \
    root_path = directory.get_user_photos_dir_path(False))


@webapp.route('/api/photo_display', methods=['GET'])
def display_photo():

    return render_template('display_photo.html', \
    photo_name = unquote_plus(request.args.get('file_name')), \
    root_path = directory.get_user_photos_dir_path(False))


# Mock database for photos
# {file_id: (original_filename, user)}
photos = dict()