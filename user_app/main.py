from flask import render_template
from user_app import account, webapp, photo
from aws_api_helper import put_http_request_count


@webapp.route('/', methods=['GET', 'POST'])
@webapp.route('/index', methods=['GET', 'POST'])
@webapp.route('/main', methods=['GET', 'POST'])
# Display an HTML page with links
def main_handler():
    return main()


@webapp.before_request
def do_something_whenever_a_request_comes_in():
    put_http_request_count(1)


class GuestWelcomeArgs:
    def __init__(self, username=None, password=None, error_message=None, title='Wellcome to Image Gallery!'):
        self.username = username
        self.password = password
        self.error_message = error_message
        self.title = title


class UserWelcomeArgs:
    def __init__(self, error_message=None, title='Wellcome to Image Gallery!'):
        self.error_message = error_message
        self.title = title


def main(guest_welcome_args=GuestWelcomeArgs(), user_welcome_args=UserWelcomeArgs()):
    if account.account_is_logged_in():
        return main_user_welcome(user_welcome_args)
    else:
        return main_guest_welcome(guest_welcome_args)


def main_guest_welcome(args):
    return render_template(
        'guest_welcome.html', title=args.title, username=args.username, password=args.password, error_message=args.error_message)


def main_user_welcome(args):
    return render_template(
        'user_welcome.html', title=args.title, username=account.account_get_logged_in_username(), error_message=args.error_message,
        thumbnails=photo.get_thumbnails())
