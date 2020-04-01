import unittest
from models import *
import search_feature

import os
import logging
from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, exc, desc, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from passlib.hash import bcrypt

  
class TestStringMethods(unittest.TestCase): 
      
    def setUp(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy()
        db.init_app(app)
        app.app_context().push() 

    # Returns True or False.  
    def test(self):         
        self.assertTrue(True) 
  
    # executed after each test
    def tearDown(self):
        pass
 
 
    ###############
    #### tests ####
    ###############

    def test_isbnSearch(self):
        data = search_feature.getSearchDetails("0380795272")
        self.assertEqual(data[0].title, "Krondor: The Betrayal")

    def test_titleSearch(self):
        data = search_feature.getSearchDetails("Dark Is Rising")
        self.assertEqual(data[0].title, "The Dark Is Rising")
    
    def test_authorSearch(self):
        data = search_feature.getSearchDetails("Terry")
        self.assertEqual(data[0].title, "The Black Unicorn ")
    
    def test_NoMatch_Search(self):
        data = search_feature.getSearchDetails("rishika")
        self.assertEqual(str(len(data)), "0")
    




if __name__ == "__main__":
    unittest.main()