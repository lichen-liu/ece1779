#!/bin/bash

# This only works on AWS EC2 instance used for deployment."

if [ "$1" = "git" ]; then
    echo "> git checkout -f"
    git checkout -f
    echo "> git pull"
    git pull
    echo "> chmod 777 ${0}"
    chmod 777 "${0}"
fi
python3 -m venv venv
source venv/bin/activate
pip install Flask
pip install mysql-connector-python
pip install opencv-python
pip install cvlib
pip install tensorflow
pip install boto3
pip install gunicorn
venv/bin/gunicorn --bind 0.0.0.0:5000 --workers=1 run_user_app:webapp
