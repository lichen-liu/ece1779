from flask import Flask

webapp = Flask(__name__)

webapp.config.from_object('user_app.config.Config')

from user_app import main

from user_app import initialize
initialize.init()