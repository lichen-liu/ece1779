from flask import g, redirect, render_template, request, url_for
from app import account, webapp, prepare_user_data_dir

@webapp.route('/',methods=['GET'])
@webapp.route('/index',methods=['GET'])
@webapp.route('/main',methods=['GET'])
# Display an HTML page with links
def main_handler():
    if account.account_is_logged_in():
        initialize_directory_after_login()
        return main_user_welcome()
    else:
        return main_guest_welcome()


def main_guest_welcome(username=None, password=None, error_message=None, title='Hello! NI MA ZHA LE!'):
    return render_template('guest_welcome.html',title=title, username=username, password=password, error_message=error_message)


def main_user_welcome(title='Hello! NI BA ZHA LE!'):
    return render_template('user_welcome.html',title=title,username=account.account_get_logged_in_user())

def initialize_directory_after_login():
    prepare_user_data_dir.create_user_data_root_directory()
    prepare_user_data_dir.craete_user_thumbnail_directory()
    prepare_user_data_dir.craete_user_photo_directory()
