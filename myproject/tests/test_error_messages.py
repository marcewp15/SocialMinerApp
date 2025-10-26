import unittest
import sys, os
from unittest.mock import patch
from flaskr import create_app  # Ajusta el import según la ubicación real de tu paquete

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestErrorMessages(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SECRET_KEY': 'test'})
        self.client = self.app.test_client()
    
    def test_busqueda_invalida_muestra_mensaje_error(self):
        response = self.client.post('/searcher', data={'term': 'abc123'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Solo se permiten letras en la busqueda', response.data)
    
    @patch('flaskr.home.search_x', side_effect=Exception('Error simulado'))
    def test_busqueda_falla_interna(self, mock_search):
        response = self.client.post('/searcher', data={'term':'hola'},follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ocurrio un error en la busqueda',response.data)
    
    @patch('flaskr.home.search_x', return_value=[])
    def test_sin_resultados_muestra_mensaje(self,mock_search):
        response = self.client.post('/searcher', data={'term':'vacio'},follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No se encontraron tweets para esta palabra clave', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)