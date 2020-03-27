import os

import logging

from flask import Flask, session, request, render_template,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine, exc, desc
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import *

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Session(app)
db.init_app(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

# default router
@app.route("/")
def index():
    return render_template("index.html")

#register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['pswd']
        logging.debug('print',username,email,password)
        queryResultSet = Users.query.filter_by(email=email).all()

        try:
            user = Users(username = username, email = email, password = password, registerTime = datetime.now())
            db.session.add(user)
            db.session.commit()
            responseMessage = "You registered sucessfully!"
            return render_template("index.html",data=responseMessage)
        except exc.IntegrityError:
            responseMessage = "Your email already exists!"
            return render_template("index.html",data=responseMessage)
        except:
            logging.debug('exception message','something else went wrong')
        
    return render_template("register.html")

#admin page
@app.route("/admin")
def listUsers():
    queryResultSet = Users.query.order_by(desc(Users.registerTime)).all()
    return render_template('admin.html', data=queryResultSet)

