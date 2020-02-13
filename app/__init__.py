from flask import Flask
webapp = Flask(__name__)

from app import config
webapp.config.from_object('config.Config')

from app import initialize
initialize.init()