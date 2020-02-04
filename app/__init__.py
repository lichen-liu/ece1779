
from flask import Flask
from datetime import timedelta

webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = 'NIDEMAMAMASHANGJIUYAOBAOZHALE'
webapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 1)
print('SECRET_KEY = ' + str(webapp.config['SECRET_KEY']))
print('PERMANENT_SESSION_LIFETIME = ' + str(webapp.config['PERMANENT_SESSION_LIFETIME']))

# from app import trivial
# from app import courses
# from app import students
# from app import sections

from app import account
from app import main
from app import uploadPhoto
