"""
search
"""
import os
import logging
from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, exc, desc, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import Books
from passlib.hash import bcrypt
from flask_sqlalchemy import SQLAlchemy




"""
search
"""
def getSearchDetails(query):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy()
    db.init_app(app)
    app.app_context().push()    


    query = "%"+query+"%".title()
    data = Books.query.filter(or_(Books.isbn.like(query),Books.title.like(query),Books.author.like(query))).all()
    return data
