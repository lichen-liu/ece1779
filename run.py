#!venv/bin/python
from app import webapp, directory

def run_app():
    prepare()
    run_flask()

def prepare():
    directory.create_static_and_data_directory_if_necessary()

def run_flask():
    webapp.run(host='0.0.0.0',debug=True)

run_app()