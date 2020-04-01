'''
This file is for running test cases on
book_details feature
'''
import os
import unittest
from flask import Flask
from models import db
import book_details
from flask_sqlalchemy import SQLAlchemy

 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy()
        db.init_app(app)
        app.app_context().push() 
  
###############
#### tests ####
###############
 
    def test_book_page(self):
        # response = self.app.get('/books/0380795272', follow_redirects=True)
        # self.assertEqual(response.status_code, 200)
        res = book_details.get_book_details('0380795272')
        self.assertEqual(res.title,'Krondor: The Betrayal')
        self.assertEquals(res.author, 'Raymond E. Feist')

        res = book_details.get_book_details('1244')
        self.assertEqual(res, None)
    
if __name__ == "__main__":
    unittest.main()
