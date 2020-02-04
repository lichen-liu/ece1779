from flask import render_template, flash, redirect, url_for, request, g, session
from app import webapp
from app import account
import os

currentDir = os.getcwd()
photoDir = currentDir + '/app/uploadedPhotos/'

@webapp.route('/api/handle_photo_upload', methods=['POST'])
def handle_photo_upload():
    file = request.files['file']
    filename = file.filename
    try_create_photo_directory_for_user()
    file.save(os.path.join(photoDir + get_photo_directory_for_user(), filename))
    return render_template('user_welcome.html',title='Photo Upload Successful', username=session.get('username'))

def try_create_photo_directory_for_user():
    userDirName = get_photo_directory_for_user()
    if not os.path.exists(userDirName):
        os.mkdir(photoDir + userDirName)

def get_photo_directory_for_user():
    return account.account_is_logged_in()