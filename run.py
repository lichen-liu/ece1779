#!venv/bin/python
from app import webapp, prepare_user_data_dir

def run_app():
    prepare()
    run_flask()

def prepare():
    prepare_user_data_dir.create_photo_root()

def run_flask():
    webapp.run(host='0.0.0.0',debug=True)

run_app()