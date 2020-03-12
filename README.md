# ece1779


## 1.0 User App


### 1.1 Local
Use: Python 3.7.3
```
python -m venv venv
venv\Scripts\activate
source venv/bin/activate
pip install Flask
pip install mysql-connector-python
pip install opencv-python
pip install cvlib
pip install tensorflow
pip install boto3

python run_user_app_local.py
```


### 1.2 EC2
```
chmod 777 start_user_app.sh
./start_user_app.sh
```


### 1.3 Helper Script
Use this script to check and manage S3 and RDS content.
```
python helper.py
```


## 2.0 Manager App
Use: Python 3.7.3
```
python -m venv venv
venv\Scripts\activate
source venv/bin/activate
pip install Flask
pip install awscli
pip install boto3

```
Then type:

```
aws configure
```

Then set ~/.aws/credentials following this format:

```
[default]
aws_access_key_id= Your_aws_access_key_id
aws_secret_access_key= Your_aws_access_key
aws_session_token= Your_session_token
```

To get the above values (key_id, key, token),and for an AWS educate account, it will be at your  AWS Educate Account page -> Account Details.
Now you are able to use AWS SDKs, user mannual: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/index.html
