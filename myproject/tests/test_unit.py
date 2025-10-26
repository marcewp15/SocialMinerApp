import unittest
import sys, os
from flaskr import create_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class UnitTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
    
    def test_home_status(self):
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__=='_main_':
    unittest.main()
