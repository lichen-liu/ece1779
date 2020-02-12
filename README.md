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
```
https://dev.mysql.com/downloads/mysql/
"Developer Default"
```
Install Python mysql connector
```
pip install mysql-connector-python
```


### 1.3 OpenCV YOLO3
```
pip install opencv-python
pip install cvlib
pip install tensorflow
```
We are now using ```yolov3``` model.  
You can find a variaty of trained yolo3 weights and labels from these website:
```
https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
https://pjreddie.com/darknet/yolo/
```
Then move the weights, config and label files to the app/static/yolo/. directory.
If the 'yolo' directory does not exist on you local environment under the static directory, you can manually create it or just start the application as if will check and create the yolo directory for you


## 2.0 To Run

For Windows (Powershell)
```
cd app
$env:FLASK_APP = "main.py"
python -m flask run
```

For Mac:
```
cd app
export FLASK_APP = "main.py"
python -m flask run --host=0.0.0.0
```


## 3.0 AWS IP:

~~[http://52.207.56.96:5000/](http://52.207.56.96:5000/)~~

[http://3.231.61.127:5000/](http://3.231.61.127:5000/)


## 4.0 Notes
When committing the code, double check to make sure no OS/IDE-dependent temporary files are included!
