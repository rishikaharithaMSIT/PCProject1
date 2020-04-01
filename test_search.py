import unittest
from models import *
import search_feature

  
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