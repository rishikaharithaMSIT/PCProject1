"""
Flask App
"""
import os
import logging
from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine, exc, desc, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import Users, db, Books
from passlib.hash import bcrypt
import book_details
import search_feature
import json


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
    queryResultSet = Books.query.all()
    return render_template("homePage.html", data=queryResultSet)


@app.route("/userhome")
def home():
    try:
        current_user = session['user']
    except:
        return render_template("register.html", data="You must log in continue.")
    # queryResultSet = Books.query.all()
    return render_template("userhome.html")

"""
search
"""
@app.route("/search",methods=['POST'])
def search():
    data = search_feature.getSearchDetails(request.form['search'])
    if len(data) == 0:
        return render_template("homePage.html", noresults="No matching Results Found")
    return render_template("homePage.html", data=data, isSearch="yes")

"""
search api
"""
@app.route("/api/search/", methods = ['POST'])
def searchAPI():
    try:
        if request.is_json:
            searchJson = request.get_json()
            if 'query' in searchJson:
                query = searchJson['query']
                data = search_feature.getSearchDetails(query)
                if len(data) == 0:
                    return jsonify({"result":"no matches found"})
                dBooks = {"books":[]}
                for each in data:
                    d = dict()
                    d["isbn"]= each.isbn
                    d["title"] = each.title
                    d["author"] = each.author
                    d["year"] = each.year
                    dBooks["books"].append(d)
                return jsonify(dBooks)
        return (jsonify({"Error":"Invalid JSON"}),400)
    except:
        return (jsonify({"Error":"Unexpected Failure"}),500)
    


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
book_page
"""
@app.route("/books/<isbn>", methods=["GET"])
def book_detail(isbn):
    # book = Books.query.get(isbn)
    book = book_details.get_book_details(isbn)
    return render_template("bookDetails.html", book=book)

from flask import Flask, render_template, jsonify, request

  # ... other imports, set up code, and routes ...

@app.route("/api/book/<isbn>",methods=['GET'])
def flight_api(isbn):
    """Return details about a single flight."""

    # Make sure flight exists.
    book = book_details.get_book_details(isbn)
    if book is None:
        return jsonify({"error": "Invalid book_id"}), 422

    # Get all passengers.
    return jsonify({
            "isbn" : book.isbn,
            "title": book.title,
            "author": book.author,
            "year": book.year,
        })

"""
admin page
"""
@app.route("/admin")
def listUsers():
    queryResultSet = Users.query.order_by(desc(Users.registerTime)).all()
    return render_template('admin.html', data=queryResultSet)

