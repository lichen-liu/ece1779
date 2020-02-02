from flask import render_template, redirect, url_for, request, g
from app import webapp

#import mysql.connector

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

@webapp.route('/sections',methods=['GET'])
# Display an HTML list of all sections.
def sections_list():
    cnx = get_db()

    cursor = cnx.cursor()

    query = '''SELECT s.id, c.code, c.title, s.time, s.location, 
                      s.maximum_enrolment, s.current_enrolment 
               FROM courses c, sections s 
               WHERE c.id = s.courses_id'''

    cursor.execute(query)
    
    return render_template("sections/list.html",title="Sections List", cursor=cursor)


@webapp.route('/sections/<int:id>',methods=['GET'])
#Display details about a specific student.
def sections_view(id):
    cnx = get_db()

    cursor = cnx.cursor()

    query = '''SELECT st.name 
               FROM  students st, sections s,  students_has_sections ss
               WHERE ss.sections_id = s.id AND
                     ss.students_id = st.id AND
                     s.id = %s'''

    students = []

    cursor.execute(query,(id,))

    for row in cursor:
        students.append(row)


    query = '''SELECT c.code, c.title, s.time, s.location, s.maximum_enrolment, s.current_enrolment
               FROM  sections s, courses c 
               WHERE s.courses_id = c.id AND
                     s.id = %s'''

    cursor.execute(query,(id,))
    
    row = cursor.fetchone()
    
    course_name = row[0] + ":" + row[1]
    time = row[2]
    location = row[3]
    max_enrolment = row[4]
    cur_enrolment = row[5]
    
    return render_template("sections/view.html",title="Section Details",
                           course_name=course_name,
                           time=time,
                           location=location,
                           max_enrolment=max_enrolment,
                           cur_enrolment=cur_enrolment,
                           students=students)
    



@webapp.route('/sections/create',methods=['GET'])
# Display an empty HTML form that allows users to define new student.
def sections_create():
    cnx = get_db()

    cursor = cnx.cursor()

    query = 'SELECT id, code, title FROM courses'
    
    cursor.execute(query)        
    return render_template("sections/new.html",title="New Section",cursor=cursor)

@webapp.route('/sections/create',methods=['POST'])
# Create a new student and save them in the database.
def sections_create_save():
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    return redirect(url_for('sections_list'))



@webapp.route('/sections/delete/<int:id>',methods=['POST'])
# Deletes the specified student from the database.
def sections_delete(id):
    cnx = get_db()
    cursor = cnx.cursor()

    query = "DELETE FROM sections WHERE id = %s"
    
    cursor.execute(query,(id,))
    cnx.commit()

    return redirect(url_for('sections_list'))

