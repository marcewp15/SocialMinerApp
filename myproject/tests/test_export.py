import unittest
import sys, os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flaskr import create_app

class TestExportRoute(unittest.TestCase):
    def setUp(self):
        #Configuración del cliente de prueba en flask
        self.app = create_app({'TESTING':True, 'SECRECT_KEY': 'test'})
        self.client = self.app.test_client()
    
    @patch('os.path.exists', return_value=False)
    def test_export_sin_resultados(self,mock_exist):
        response = self.client.get('/export', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No hay resultados disponibles para exportar', response.data)
    
    @patch('os.path.exists', return_value=True)
    @patch('flaskr.home.send_file')
    def test_export_exitoso(self, mock_send_file, mock_exist):
        mock_response = self.app.response_class(
           "contenido simulado", status=200, headers={"content-Disposition":"attachment; filename=tweets_resultados.txt"})
        mock_send_file.return_value = mock_response
        response = self.client.get('/export')
        
        self.assertAlmostEqual(response.status_code,200)
        mock_send_file.assert_called_once()
        
        content_disposition = response.headers.get("content-Disposition")
        self.assertIn("tweets_resultados.txt", content_disposition)
    
    @patch('os.path.exists', side_effect=Exception('Error simulado'))
    def test_export_error_exception(self, mock_exist):
        response = self.client.get('/export', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No fue posible exportar los resultados', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    