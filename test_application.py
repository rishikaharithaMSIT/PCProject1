import unittest
from models import *
import search_feature

import os
import logging
from flask import Flask, session, request, render_template, redirect, url_for, post
from flask_session import Session
from sqlalchemy import create_engine, exc, desc, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from passlib.hash import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
class TestStringMethods(unittest.TestCase): 
      
    def setUp(self):
        pass

    # Returns True or False.  
    def test(self):         
        self.assertTrue(True) 
  
    # executed after each test
    def tearDown(self):
        pass
 
 
    ###############
    #### tests ####
    ###############

    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    




if __name__ == "__main__":
    unittest.main()