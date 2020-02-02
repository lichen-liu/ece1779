from flask import render_template, redirect, url_for, request, g
from app import webapp

#import mysql.connector

import re

from app.config import db_config

def connect_to_database():
    return mysql.connector.connect(user=db_config['user'], 
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
 
@webapp.route('/students',methods=['GET'])
# Display an HTML list of all students.
def students_list():
    cnx = get_db()

    cursor = cnx.cursor()

    query = "SELECT * FROM students"

    cursor.execute(query)
    
    return render_template("students/list.html",title="Students List", cursor=cursor)


@webapp.route('/students/<int:id>',methods=['GET'])
#Display details about a specific student.
def students_view(id):
    cnx = get_db()
    cursor = cnx.cursor()
    query = "SELECT * FROM students WHERE id = %s"
    cursor.execute(query,(id,))
    
    row = cursor.fetchone()
    
    id = row[0]
    name = row[1]
    email = row[2]
    dob = row[3]
    program = row[4]
    
    query = '''SELECT s.id, c.code, c.title, s.time 
               FROM courses c, sections s,  students_has_sections ss
               WHERE c.id = s.courses_id AND
                     ss.sections_id = s.id AND
                     ss.students_id = %s'''

    registered = []

    cursor.execute(query,(id,))
    
    for row in cursor: registered.append(row)
        
    query = '''SELECT s.id, c.code, c.title, s.time 
               FROM courses c, sections s
               WHERE c.id = s.courses_id AND
                     s.id NOT IN (SELECT sections_id 
                                  FROM students_has_sections 
                                  WHERE students_id = %s)'''

    cursor.execute(query,(id,))
    
    available = []
    
    for row in cursor: available.append(row)
    
    return render_template("students/view.html",title="Student Details",
                           registered=registered,
                           available=available,
                           id=id,
                           name=name, email=email, dob=dob, program=program)
    

@webapp.route('/students/edit/<int:id>',methods=['GET'])
# Display an editable HTML form populated with student data. 
def students_edit(id):
    cnx = get_db()

    cursor = cnx.cursor()

    query = "SELECT * FROM students WHERE id = %s"

    cursor.execute(query,(id,))
    
    row = cursor.fetchone()
    
    id = row[0]
    name = row[1]
    email = row[2]
    dob = row[3]
    program = row[4]
    
    return render_template("students/edit.html",title="Edit Student",id=id,name=name, 
                           email=email, dob=dob, program=program)

@webapp.route('/students/edit/<int:id>',methods=['POST'])
# Save the form changes for a particular student to the database.
def students_edit_save(id):
    name = request.form.get('name',"")
    email = request.form.get('email',"")
    dob = request.form.get('dob',"")
    program = request.form.get('program',"")

    error = False

    if name == "" or email== "" or dob == "" or program == "":
        error=True
        error_msg="Error: All fields are required!"
    
    if not error and not re.match('\d{4}-\d{2}-\d{2}', dob):
        error=True
        error_msg="Error: Date of birth most be in format YYYY-MM-DD!"
         
   
    if error:
        return render_template("students/edit.html",title="New Student",error_msg=error_msg, id=id, 
                               name=name, email=email, dob=dob, program=program)


    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' UPDATE students SET name=%s, email=%s, date_of_birth=%s, program_of_study=%s
                WHERE id = %s '''
    
    cursor.execute(query,(name,email,dob,program,id))
    cnx.commit()
    
    return redirect(url_for('students_list'))


@webapp.route('/students/create',methods=['GET'])
# Display an empty HTML form that allows users to define new student.
def students_create():
    return render_template("students/new.html",title="New Student")

@webapp.route('/students/create',methods=['POST'])
# Create a new student and save them in the database.
def students_create_save():
    name = request.form.get('name',"")
    email = request.form.get('email',"")
    dob = request.form.get('dob',"")
    program = request.form.get('program',"")

    error = False

    if name == "" or email== "" or dob == "" or program == "":
        error=True
        error_msg="Error: All fields are required!"
    
    if not error and not re.match('\d{4}-\d{2}-\d{2}', dob):
        error=True
        error_msg="Error: Date of birth most be in format YYYY-MM-DD!"
         
   
    if error:
        return render_template("students/new.html",title="New Student",error_msg=error_msg, 
                               name=name, email=email, dob=dob, program=program)


    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' INSERT INTO students (name,email,date_of_birth,program_of_study)
                       VALUES (%s,%s,date %s,%s)
    '''

    cursor.execute(query,(name,email,dob,program))
    cnx.commit()
    
    return redirect(url_for('students_list'))



@webapp.route('/students/delete/<int:id>',methods=['POST'])
# Deletes the specified student from the database.
def students_delete(id):
    cnx = get_db()
    cursor = cnx.cursor()

    query = "DELETE FROM students WHERE id = %s"
    
    cursor.execute(query,(id,))
    cnx.commit()

    return redirect(url_for('students_list'))


@webapp.route('/students/register/<int:students_id>/<int:sections_id>',methods=['POST'])
# Deletes the specified student from the database.
def students_register(students_id,sections_id):
    cnx = get_db()
    cursor = cnx.cursor()


   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   

    return redirect(url_for('students_view',id=students_id))
