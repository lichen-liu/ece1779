#!/bin/bash

# This only works on AWS EC2 instance used for deployment.
cd /home/ubuntu/ece1779

#if [ "$1" = "git" ]; then
#echo "> Update repository"
#git checkout -f
#git pull
#chmod 777 "${0}"
#fi
echo "> Initialize virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "> Installing Libraries..."
pip install Flask
pip install mysql-connector-python
pip install opencv-python
pip install cvlib
pip install tensorflow
pip install boto3
pip install gunicorn

echo "> Starting the user app on Port = 5000 ..."
venv/bin/gunicorn --bind 0.0.0.0:5000 --workers=1 run_user_app:webapp
