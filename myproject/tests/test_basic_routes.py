import unittest
import sys, os
from flaskr import create_app 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestBasicRoutes(unittest.TestCase):

    def setUp(self):
        """Crea una instancia de la app para pruebas."""
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()

    def test_app_exists(self):
        """Verifica que la app se creó correctamente."""
        self.assertIsNotNone(self.app)

    def test_home_redirect(self):
        """Comprueba que /home redirige correctamente al blueprint 'home.index'."""
        response = self.client.get('/home', follow_redirects=False)
        self.assertEqual(response.status_code, 302)  # redirección
        self.assertIn('/' , response.headers['Location'])  # redirige al home.index

    def test_home_index_route(self):
        """Valida que la ruta principal del blueprint devuelve 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SocialMiner', response.data)  # contenido esperado del HTML


if __name__ == '__main__':
    unittest.main(verbosity=2)
