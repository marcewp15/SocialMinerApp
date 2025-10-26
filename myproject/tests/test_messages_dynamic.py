import unittest
import sys, os
from flaskr import create_app 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestMensajesHTML(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_avisos_presentes_en_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        html = response.data.decode('utf-8')

        # Verifica que los avisos existan en el HTML
        self.assertIn('id="aviso-buscado"', html, "No se encontró el aviso-buscado en el HTML")
        self.assertIn('id="aviso-chrome"', html, "No se encontró el aviso-chrome en el HTML")

        # Verifica que el formulario exista
        self.assertIn('action="/searcher"', html)
        self.assertIn('name="term"', html)
