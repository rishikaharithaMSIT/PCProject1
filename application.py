"""
Flask App
"""
import os
import logging
from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, exc, desc
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import *
from passlib.hash import bcrypt

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db.init_app(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))

"""
default router
"""
@app.route("/")
def index():
    try:
        current_user = session['user']
    except:
        return render_template("register.html", data="You must log in continue.")
    return render_template("homePage.html", data=current_user)

"""
login
"""
@app.route("/auth", methods=['POST'])
def auth():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pswd']
        if email == "" or password == "":
            return render_template("register.html", data="Please enter\
             username and password to register")
        queryResultSet = Users.query.filter_by(email=email).first()
        if queryResultSet is not None:
            if bcrypt.verify(password, queryResultSet.password):
                session['user'] = email
                return redirect(url_for('index'))
            else:
                return render_template("register.html", data="Email and\
                 password does not match. Try again!")

        return render_template("register.html", data="Email does not exists.\
         Try to Register")
"""
Logout
"""
@app.route("/logout")
def logout():    
    session.clear()
    return render_template("register.html", data="You logged out sucessfully")

"""
register page
"""
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email'] 
        password = bcrypt.encrypt(request.form['pswd'])       
        if email == "" or bcrypt.verify("", password):
            return render_template("register.html", data="Please enter username\
                and password to register")
        if '@' not in email or '.' not in email:
            return render_template("register.html", data="Please enter a valid email to register")
        try:
            user = Users(email=email, password=password, registerTime=datetime.now())
            db.session.add(user)
            db.session.commit()
            return render_template("register.html", data="You registered\
             sucessfully! Login to continue.")
        except exc.IntegrityError:
            return render_template("register.html", data="The Email you\
             used already exists! Try logging in.")
        except:
            logging.debug('exception message', 'something else went wrong\
             in adding a user')
    return render_template("register.html")

"""
admin page
"""
@app.route("/admin")
def listUsers():
    queryResultSet = Users.query.order_by(desc(Users.registerTime)).all()
    return render_template('admin.html', data=queryResultSet)

