from flask import render_template, flash, redirect, url_for, request, g, session
from app import webapp
from app import account
from PIL import Image
import os

size = (120,120)
user_photo_dir = ''
user_thumbnail_dir = ''
photo_dir = ''


@webapp.route('/api/handle_photo_upload', methods=['POST'])
def handle_photo_upload():
    global user_photo_dir
    global user_thumbnail_dir
    global photo_dir

    current_dir = os.getcwd()
    photo_dir = current_dir + '/app/uploadedPhotos'
    user_photo_dir = photo_dir + '/' + get_photo_directory_name_for_user()
    user_thumbnail_dir = user_photo_dir + '/thumbNails'

    file = request.files['file']
    filename = file.filename

    try_initialize_directory_for_user()
    file.save(os.path.join(user_photo_dir, filename))

    thumbnail = get_thumbnail_for_image(file)
    thumbnail.save(os.path.join(user_thumbnail_dir, filename))
    return render_template('user_welcome.html',title='Photo Upload Successful', username=session.get('username'))

def try_initialize_directory_for_user():
    if not os.path.exists(user_photo_dir):
        os.mkdir(user_photo_dir)
    if not os.path.exists(user_thumbnail_dir):
        os.mkdir(user_thumbnail_dir)

def get_photo_directory_name_for_user():
    return account.account_get_logged_in_user()

def get_thumbnail_for_image(image_file):
    image = Image.open(image_file)
    image.thumbnail(size, Image.ANTIALIAS)
    return image


