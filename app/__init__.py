
from flask import Flask

webapp = Flask(__name__)

from app import trivial
from app import courses
from app import students
from app import sections

from app import main

