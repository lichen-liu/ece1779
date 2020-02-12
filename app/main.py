from flask import g, redirect, render_template, request, url_for
from app import account, webapp, directory, photo, utility, queue, image_batch_runner
import os

@webapp.route('/',methods=['GET', 'POST'])
@webapp.route('/index',methods=['GET', 'POST'])
@webapp.route('/main',methods=['GET', 'POST'])
# Display an HTML page with links
def main_handler():
    batch_runner = image_batch_runner.get_batch_runner()
    batch_runner.run()
    return main()


class GuestWelcomeArgs:
    def __init__(self, username=None, password=None, error_message=None, title='Hello! NI MA ZHA LE!'):
        self.username = username
        self.password = password
        self.error_message = error_message
        self.title = title


class UserWelcomeArgs:
    def __init__(self, error_message=None, title = 'Hello! NI BA ZHA LE!'):
        self.error_message=error_message
        self.title = title


def main(guest_welcome_args=GuestWelcomeArgs(), user_welcome_args=UserWelcomeArgs()):
    if account.account_is_logged_in():
        # Not a good practice to do it here
        directory.create_user_directory_if_necessary()
        return main_user_welcome(user_welcome_args)
    else:
        return main_guest_welcome(guest_welcome_args)


def main_guest_welcome(args):
    return render_template(
        'guest_welcome.html',title=args.title, username=args.username, password=args.password, error_message=args.error_message)


def main_user_welcome(args):
    thumbnail_dir_path, thumbnails = photo.get_thumbnails()
    return render_template(
        'user_welcome.html',title=args.title,username=account.account_get_logged_in_user(), error_message=args.error_message, thumbnails=thumbnails, thumbnail_dir_path=thumbnail_dir_path)


def init():
    # Construct yolov3.weights if necessary
    yolov3_weights_dst_file = os.path.join(directory.get_yolo_dir_path(), 'yolov3.weights')
    if not os.path.exists(yolov3_weights_dst_file):
        yolov3_weights_chunk_files = [os.path.join(directory.get_yolo_dir_path(), 'yolov3.weights.' + str(i)) for i in range(0, 5)]
        utility.combine_files(yolov3_weights_chunk_files, yolov3_weights_dst_file)
    # To split, run:
    # utility.split_file(yolov3_weights_dst_file)