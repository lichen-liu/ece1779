
from datetime import timedelta

from flask import Flask



webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = 'NIDEMAMAMASHANGJIUYAOBAOZHALE'
webapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 1)
webapp.config['SESSION_REFRESH_EACH_REQUEST'] = True
webapp.config['THUMBNAIL_SIZE'] = (120,120)

print('SECRET_KEY = ' + str(webapp.config['SECRET_KEY']))
print('PERMANENT_SESSION_LIFETIME = ' + str(webapp.config['PERMANENT_SESSION_LIFETIME']))


# from app import trivial
# from app import courses
# from app import students
# from app import sections

from app import account ,main, photo