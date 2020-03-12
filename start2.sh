# This only works on AWS EC2 instance used for deployment."

git pull
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
