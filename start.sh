# This only works on AWS EC2 instance used for deployment."
mysql --user=root  --password=ece1779pass < /home/ubuntu/ece1779_a1/app/schema.sql

source ~/anaconda3/etc/profile.d/conda.sh
conda activate base 
cd /home/ubuntu/ece1779_a1
gunicorn --bind 0.0.0.0:5000 --workers=1 run_user_app:webapp
