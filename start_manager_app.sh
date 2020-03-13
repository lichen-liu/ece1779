#!/bin/bash

# This only works on AWS EC2 instance used for deployment.

if [ "$1" = "git" ]; then
    echo "> Update repository"
    git checkout -f
    git pull
    chmod 777 "${0}"
fi
echo "> Initialize virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "> Installing Libraries..."
pip install Flask
pip install mysql-connector-python
pip install awscli
pip install boto3
pip install gunicorn

echo "> Starting the manager app on Port = 5000 ..."
venv/bin/gunicorn --bind 0.0.0.0:5000 --workers=1 run_manager_app:webapp
