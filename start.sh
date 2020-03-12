# This only works on AWS EC2 instance used for deployment."

source ~/anaconda3/etc/profile.d/conda.sh
conda activate base 
cd /home/ubuntu/ece1779
gunicorn --bind 0.0.0.0:5000 --workers=1 run_user_app:webapp
