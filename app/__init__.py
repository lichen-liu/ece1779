
from datetime import timedelta

from flask import Flask


webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = 'NIDEMAMAMASHANGJIUYAOBAOZHALE'
webapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 100)
webapp.config['SESSION_REFRESH_EACH_REQUEST'] = True
webapp.config['THUMBNAIL_SIZE'] = (120,120)
webapp.config['MAXIMUM_IMAGE_SIZE'] = 5 * 1024 * 1024
webapp.config['ALLOWED_IMAGE_EXTENSION'] = set(['png', 'jpg', 'jpeg', 'gif'])


print('SECRET_KEY = ' + str(webapp.config['SECRET_KEY']))
print('PERMANENT_SESSION_LIFETIME = ' + str(webapp.config['PERMANENT_SESSION_LIFETIME']))


from app import account ,main, photo, directory, utility


main.init()