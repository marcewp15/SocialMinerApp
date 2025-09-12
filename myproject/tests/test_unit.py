import unittest
from flaskr import create_app

class UnitTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
    
    def test_home_status(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
