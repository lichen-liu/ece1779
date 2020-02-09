# ece1779_a1
http://www.cs.toronto.edu/~delara/courses/ece1779/projects/ECE1779-a1.pdf


## 1.0 Setup


### 1.1 Flask
Use: Python 3.8.1
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


### 1.3 OpenCV YOLO3
Download the trained yolo3 weights and labels from this website given in the handout:
```
https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
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

[http://52.207.56.96:5000/](http://52.207.56.96:5000/)


## 4.0 Notes
When committing the code, double check to make sure no OS/IDE-dependent temporary files are included!


## 5.0 Notes Copied from the Original Course Demo Project
*DON'T PUT THINGS HERE!*
```
All lecture and tutorial examples require the following in order to work:
    - Python 3.5 (or better)
    - A python virtual environment
    - Flask
    - MySQL server
    - MySQL Python connector
    - A database schema called ece1779 which include 4 tables: students, courses, sections and students_has_sections

Perform these steps to run the examples:

1) Install python 3.5 by following the instructions for your respective platform available at https://www.python.org/

2) Install MySQL Server from https://dev.mysql.com/downloads/mysql/

3) Start the MySQL server

4) Install MySQL Workbench from https://dev.mysql.com/downloads/workbench/

5) Create the database schema used by the examples:

   a) Start mysqlworkbench
   b) Connect to the database server
   d) Run the SQL queries in the file ece1779.sql

6) Install the MySQL Python Connector from https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html


8) Download and unpack the example sources:

   a) Download the example sources,
   b) Open a shell and navigate to the location of the tar.gz file
   c) Uncompress and untar (e.g., tar -xzf flask.tar.gz)
   d) Go into the example directory (e.g., cd interactive)

9) Create a new python virtual environment as follows:

      python -m venv venv

      For some platforms substitute python for python3 or python3.5

10) Install Flask

      venv/bin/pip install flask


11) Install the Python MySQL connector bindings:

       venv/bin/pip install mysql-connector==2.1.4

12) Run the example

      run.py

      For some platforms you may need to edit the first line of this file to reflect the correct path to the
      python installation in the virtual environment.  The provided file works for Linux and OS X.

13) Download the trained yolo3 weights and labels from this website given in the handout:

      https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/

      Then move the weights, config and label files to the app/static/yolo/. directory

      If the 'yolo' directory does not exist on you local environment under the static directory, you can manually create it or just start the application as if will check and create the yolo directory for you
```
