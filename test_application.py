import unittest
from models import *
import os
import logging
from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, exc, desc, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from passlib.hash import bcrypt
from application import app

class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        # Check for environment variable
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set")
        # Base.query = db_session.query_property()
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
    ########################
    #### helper methods ####
    ########################
     
    def register(self, email, password):
        return self.app.post('/register',data=dict(email=email, pswd=password),follow_redirects=True)
     
    def login(self, email, password):
        return self.app.post('/auth',data=dict(email=email, pswd=password),follow_redirects=True)
    
 
###############
#### tests ####
###############
 
    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_register(self):
        response = self.register('rishikaharitha@gmail.com', 'pass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'used already exists! Try logging in.', response.data)

    def test_invalid_user_registeremail(self):
        response = self.register('adminmsitprogram.net', 'a1dmin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid email to register', response.data)  

    
    def test_invalid_user_login(self):
        response = self.login('rishika@gmail.com', 'pass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email does not exists.', response.data)

   

if __name__ == "__main__":
    unittest.main()