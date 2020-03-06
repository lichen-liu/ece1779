# ece1779_a1
http://www.cs.toronto.edu/~delara/courses/ece1779/projects/ECE1779-a1.pdf


## 1.0 Setup


### 1.1 Flask
Use: Python 3.7.3
```
python -m venv venv
venv\Scripts\activate
pip install Flask
```


### 1.2 MySQL
Use: MySQL Community Server 8.0.19
- https://dev.mysql.com/downloads/mysql/
- "Developer Default"
  
Install Python mysql connector
```
pip install mysql-connector-python
```
Start MySQL Server
```
1. Open MySQL Workbench
2. Conncet to an instance
3. File - Run SQL Script(/app/schema.sql)
```


### 1.3 OpenCV YOLO3
```
pip install opencv-python
pip install cvlib
pip install tensorflow
```
We are now using ```yolov3``` model.  
You can find a variaty of trained yolo3 weights and labels from these website:
1. https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
2. https://pjreddie.com/darknet/yolo/
  
Then move the weights, config and label files to the app/static/yolo/. directory.
If the 'yolo' directory does not exist on you local environment under the static directory, you can manually create it or just start the application as if will check and create the yolo directory for you


## 2.0 To Run
```
python run.py
```

With gunicorn:
```
gunicorn --bind 0.0.0.0:5000 --workers=1 run:webapp
```
On AWS instance:
```
bash start.sh
```

## 3.0 To Reset


### 3.1 Factory Reset
1. Delete the entire directory
2. ```git clone```
3. Run ```schema.sql```
4. Run ```run.py``` or ```run_server.py```


### 3.2 Reset Big All (Including SQL IDs)
1. ```python app/server_helper.py --delete_all```
2. Run ```schema.sql```
3. Run ```run.py``` or ```run_server.py```


### 3.3 Reset Small All
1. ```python app/server_helper.py --delete_all```
2. Run ```run.py``` or ```run_server.py```


### 3.4 Reset Photos
1. ```python app/server_helper.py --delete_data```
2. Run ```run.py``` or ```run_server.py```


## 4.0 Helper Utilities
Use the script to manage filesystem and database
```
cd app
python server_helper.py --help
```


## 5.0 AWS IP

~~[http://52.207.56.96:5000/](http://52.207.56.96:5000/)~~

[http://3.231.61.127:5000/](http://3.231.61.127:5000/)


## 6.0 Testing


### 5.1 gen.py (/api/upload POST)
[http://www.cs.toronto.edu/~delara/courses/ece1779/projects/a1/gen.py](gen.py)

To set up
```
pip install aiofiles
pip install aiohttp
```
To run
```
python gen.py http://127.0.0.1:5000/api/upload user password 0.5 "C:\Users\liuli\Desktop\t"
```


## 7.0 Notes
1. When committing the code, double check to make sure no OS/IDE-dependent temporary files are included!
2. If you want to modify sql database, notify DASHEN first!

# ece1779_a2

## 1.0 Setup ##

### 1.1 Manager App Setup ###
Use: Python 3.7.3
```
python -m venv venv
venv\Scripts\activate
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
