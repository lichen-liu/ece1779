from flask import Flask
webapp = Flask(__name__)

from app import config
webapp.config.from_object('app.config.Config')

from app import main

from app import initialize
def init():
    initialize.init()