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

@webapp.route('/courses',methods=['GET'])
# Display an HTML list of all courses.
def courses_list():
    # cnx = get_db()

    # cursor = cnx.cursor()

    # query = "SELECT * FROM courses"

    # cursor.execute(query)
    
    return render_template("courses/list.html",title="Courses List")#, cursor=cursor)


@webapp.route('/courses/<int:id>',methods=['GET'])
#Display details about a specific student.
def courses_view(id):
















    
    
    return render_template("courses/view.html",title="Course Details",)
    

@webapp.route('/courses/edit/<int:id>',methods=['GET'])
# Display an editable HTML form populated with student data. 
def courses_edit(id):
    cnx = get_db()

    cursor = cnx.cursor()

    query = "SELECT * FROM courses WHERE id = %s"

    cursor.execute(query,(id,))
    
    row = cursor.fetchone()
    
    id = row[0]
    code = row[1]
    title = row[2]
    description = row[3]
    
    return render_template("courses/edit.html",title="Edit Course",id=id,code=code, ctitle=title, description=description)

@webapp.route('/courses/edit/<int:id>',methods=['POST'])
# Save the form changes for a particular student to the database.
def courses_edit_save(id):
    code = request.form.get('code',"")
    title = request.form.get('title',"")
    description = request.form.get('description',"")

    error = False

    if code == "" or title== "" or description == "":
        error=True
        error_msg="Error: All fields are required!"
    
    
    if error:
        return render_template("courses/edit.html",title="New Course",error_msg=error_msg, id=id, code=code, ctitle=title, description=description)


    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' UPDATE courses SET code=%s, title=%s, description=%s
                WHERE id = %s '''
    
    cursor.execute(query,(code,title,description,id))
    cnx.commit()
    
    return redirect(url_for('courses_list'))


@webapp.route('/courses/create',methods=['GET'])
# Display an empty HTML form that allows users to define new student.
def courses_create():
    return render_template("courses/new.html",title="New Course")

@webapp.route('/courses/create',methods=['POST'])
# Create a new student and save them in the database.
def courses_create_save():
    # cnx = get_db()
    # cursor = cnx.cursor()


    # code = 
    # title = 
    # description = 

    # error = False

    # if code == "" or title== "" or description == "":
    #     error=True
    #     error_msg="Error: All fields are required!"
    
   
    # if error:
    #     return render_template("courses/new.html",
    #                            title="New Course",
    #                            error_msg=error_msg, 
    #                            code=code, 
    #                            ctitle=title, 
    #                            description=description)



    # query = ''' INSERT INTO 
            
    #         '''
    

    # cursor.execute(query,(               ))
    # cnx.commit()
    
    return redirect(url_for('courses_list'))



@webapp.route('/courses/delete/<int:id>',methods=['POST'])
# Deletes the specified student from the database.
def courses_delete(id):
    cnx = get_db()
    cursor = cnx.cursor()

    query = "DELETE FROM courses WHERE id = %s"
    
    cursor.execute(query,(id,))
    cnx.commit()

    return redirect(url_for('courses_list'))
