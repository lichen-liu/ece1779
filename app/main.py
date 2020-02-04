from flask import g, redirect, render_template, request, url_for

from app import account, webapp


@webapp.route('/',methods=['GET'])
@webapp.route('/index',methods=['GET'])
@webapp.route('/main',methods=['GET'])
# Display an HTML page with links
def main_handler():
    if account.account_is_logged_in():
        return main_user_welcome()
    else:
        return main_guest_welcome()


def main_guest_welcome(username=None, password=None, error_message=None, title='Hello! NI MA ZHA LE!'):
    return render_template('guest_welcome.html',title=title, username=username, password=password, error_message=error_message)


def main_user_welcome(title='Hello! NI BA ZHA LE!'):
    return render_template('user_welcome.html',title=title,username=account.account_get_logged_in_user())
