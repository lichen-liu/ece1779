from flask import render_template, redirect, url_for, request, g
from app import webapp


@webapp.route('/',methods=['GET'])
@webapp.route('/index',methods=['GET'])
@webapp.route('/main',methods=['GET'])
# Display an HTML page with links
def main():
    return render_template("main.html",title="Hello! NI MA ZHA LE!")
