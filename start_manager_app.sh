if [ "$1" = "git" ]; then
echo "> Update repository"
git checkout -f
git pull
chmod 777 "${0}"
fi
echo "> Initialize virtual environment... -f"
python3 -m venv venv
source venv/bin/activate
echo "> Installing Flask..."
pip install Flask
echo "> Installing AWS command line interface..."
pip install awscli
echo "> Installing Boto3..."
pip install boto3
echo "> Installing Gunicorn..."
pip install gunicorn
echo "> Starting the manager app on Port = 5000 ..."
venv/bin/gunicorn --bind 0.0.0.0:5000 --workers=1 run_manager_app:webapp
