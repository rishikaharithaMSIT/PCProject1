import os

from flask import Flask, session, request, render_template,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Session(app)
db.init_app(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['pswd']
        registerTime = datetime.now()
        print(username,email,registerTime,password)

        queryResultSet = Users.query.filter_by(email=email).all()

        responseMessage = ""
        if(len(queryResultSet) > 0):
            responseMessage = "The email id you have used already exists!"
        else:
            user = Users(username = username, email = email, password = password, registerTime = registerTime)
            db.session.add(user)
            db.session.commit()
            responseMessage = "You registered sucessfully!"
        return render_template("index.html",data=responseMessage)
    return render_template("register.html")

@app.route("/admin")
def listUsers():
    queryResultSet = Users.query.all()
    # print(queryResultSet[0])
    return render_template('admin.html', data=queryResultSet)