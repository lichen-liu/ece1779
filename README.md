# ece1779_a1

## Setup
Use latest python: Python 3.8.1

For Windows (Powershell):
```
python -m venv venv
venv\Scripts\activate
pip install Flask

cd app
$env:FLASK_APP = "main.py"
python -m flask run
```


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
```