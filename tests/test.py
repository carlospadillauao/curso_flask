import unittest

from flask import current_app

from app import create_app
from app import db, User , Task

class DemoTestCase(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_demo(self):
        self.assertTrue(1 == 1)
        self.username="carlos"
        self.encrypted_password="encrypted_password"
        self.email="carlos@correo.com"
        user = User.create_element("carlos","encrypted_password","carlos@correo.com")
        user.get_by_id(user.id)
        


