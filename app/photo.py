
import os
from flask import (redirect, render_template, request, url_for)
from PIL import Image
from app import webapp, path

size = (120,120)

@webapp.route('/api/upload', methods=['POST'])
def photo_upload_handler():
   
    photo_file = request.files['file']
    filename = photo_file.filename
    photo_file.save(os.path.join(path.get_user_photo_directory_path(), filename))

    thumbnail = get_thumbnail_for_image(photo_file)
    thumbnail.save(os.path.join(path.get_user_thumbnail_directory_path(), filename))
   
    return redirect('/')
     #return render_template('user_welcome.html',title='Photo Upload Successfully', username=account.account_get_logged_in_user())

def get_thumbnail_for_image(image_file):
    image = Image.open(image_file)
    image.thumbnail(size, Image.ANTIALIAS)
    return image


# Mock database for photos
# {file_id: (original_filename, user)}
photos = dict()