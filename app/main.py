from flask import render_template, redirect, url_for, request, g
from app import webapp
from app import account


@webapp.route('/',methods=['GET'])
@webapp.route('/index',methods=['GET'])
@webapp.route('/main',methods=['GET'])
# Display an HTML page with links
def main_handler():
    logged_in_user = account.account_is_logged_in()
    if logged_in_user:
        return render_template('user_welcome.html',title='Hello! NI BA ZHA LE!',username=logged_in_user)
    else:
        return main_guest_welcome()


def main_guest_welcome(username=None, password=None, error_message=None):
    return render_template('guest_welcome.html',title='Hello! NI MA ZHA LE!', username=username, password=password, error_message=error_message)
