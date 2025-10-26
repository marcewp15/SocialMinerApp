import unittest
import sys, os
from flaskr import create_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SearchFormTextTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_search_form_elements_exist(self):
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        html = response.data.decode('utf-8')

        # Buscar el formulario y sus elementos
        self.assertIn('<form', html, "No se encontró el formulario")
        self.assertIn('name="term"', html, "No se encontró el campo de búsqueda 'term'")
        self.assertIn('<button', html, "No se encontró el botón de búsqueda")
        self.assertIn('Buscar', html, "No se encontró el texto 'Buscar' en el botón")

if __name__ == '__main__':
    unittest.main()


