from flask import g, redirect, render_template, request, url_for
from app import account, webapp, directory, photo

@webapp.route('/',methods=['GET', 'POST'])
@webapp.route('/index',methods=['GET', 'POST'])
@webapp.route('/main',methods=['GET', 'POST'])
# Display an HTML page with links
def main_handler():
    if account.account_is_logged_in():
        # Not a good practice to do it here
        directory.create_directory_if_necessary()
        return main_user_welcome()
    else:
        return main_guest_welcome()


def main_guest_welcome(username=None, password=None, error_message=None, title='Hello! NI MA ZHA LE!'):
    return render_template(
        'guest_welcome.html',title=title, username=username, password=password, error_message=error_message)


def main_user_welcome(title='Hello! NI BA ZHA LE!'):
    thumbnail_dir_path, thumbnails = photo.get_thumbnails()
    return render_template(
        'user_welcome.html',title=title,username=account.account_get_logged_in_user(),
        thumbnails=thumbnails, thumbnail_dir_path=thumbnail_dir_path)