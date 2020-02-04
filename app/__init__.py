
from datetime import timedelta

from flask import Flask

from app import account, main, photo

webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = 'NIDEMAMAMASHANGJIUYAOBAOZHALE'
webapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 1)
print('SECRET_KEY = ' + str(webapp.config['SECRET_KEY']))
print('PERMANENT_SESSION_LIFETIME = ' + str(webapp.config['PERMANENT_SESSION_LIFETIME']))

# from app import trivial
# from app import courses
# from app import students
# from app import sections
