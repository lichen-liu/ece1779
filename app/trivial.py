from flask import render_template
from app import webapp

import mysql.connector



@webapp.route('/trivial',methods=['GET'])
# Display an HTML list of all courses.
def trivial():

    cnx = mysql.connector.connect(user='ece1779', 
                                  password='secret',
                                  host='127.0.0.1',
                                  database='ece1779')

    cursor = cnx.cursor()
    query = "SELECT * FROM courses"
    cursor.execute(query)
    view = render_template("trivial.html",title="Courses Table", cursor=cursor)
    cnx.close()
    return view 

