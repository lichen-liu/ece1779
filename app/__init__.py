from flask import Flask
from flask import redirect
from flask import session

def account_is_logged_in():
    return session.get('username') is not None and session.get('userid') is not None

def account_get_logged_in_userid():
    assert(account_is_logged_in())
    return session['userid']

class SecuredStaticFalsk(Flask):
    def send_static_file(self, filename):
        if 'data/' in filename:
            if account_is_logged_in() and 'user_' + str(account_get_logged_in_userid()) in filename:
                return super(SecuredStaticFalsk, self).send_static_file(filename)
            else:
                return redirect('/')
        else:
            return super(SecuredStaticFalsk, self).send_static_file(filename)
webapp = SecuredStaticFalsk(__name__)

from app import config
webapp.config.from_object('app.config.Config')

from app import main

from app import initialize
def init():
    initialize.init()