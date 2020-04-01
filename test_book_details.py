import os
import unittest
 
from models import db
from application import app
import book_details
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        self.app = app.test_client()
  
###############
#### tests ####
###############
 
    def test_book_page(self):
        response = self.app.get('/books/0380795272', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # res = book_details.get_book_details('0380795272')
        # self.assertEqual(res.title,'Krondor: The Betrayal')
     
if __name__ == "__main__":
    unittest.main()
