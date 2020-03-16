#!/bin/bash

# This only works on AWS EC2 instance used for deployment.
cd ~/ece1779

if [ "$1" != "nogit" ]; then
    echo "> Update repository"
    git checkout -f
    git pull
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
# For python 3.5, this package is available on python 3.6 by default
pip install python2-secrets

echo "> Starting the manager app on Port = 5000 ..."
venv/bin/gunicorn --bind 0.0.0.0:5000 --workers=1 run_manager_app:webapp
