# Social Miner
Tecnología en Construcción de Software

Social Miner App es una aplicación web construida con Flask (Python) que realiza tareas de scraping para extraer datos de redes sociales o páginas web y presentarlos en una interfaz simple. El proyecto está orientado a fines educativos y de investigación, con un enfoque en automatización y pruebas locales.

# Descripción general

SocialMinerApp es un proyecto de aprendizaje que combina Python, Flask y herramientas de scraping para extraer contenido de la web sin usar APIs oficiales. Es adecuado para fines educativos, prototipos y experimentación. Asegúrate de respetar las políticas de uso de cada sitio web objetivo y las leyes de tu jurisdicción.

# Tecnologías

- Python 3.9+  
- Flask (v2.x o superior)  
- Selenium (opcional, para scraping dinámico)  
- Requests (HTTP requests)  
- BeautifulSoup4 o lxml (parseo HTML)  
- Gunicorn o Waitress (servidor WSGI para despliegue)  
- Docker (opcional, para contenedores)  
- dotenv (gestión de variables de entorno)  
- Flask-CORS (si se requiere interacción entre orígenes)  
- Git y GitHub (control de versiones)  

# Requisitos

## Software

- Sistema operativo: Windows, macOS o Linux compatible con Python 3.9+  
- Python 3.9 o superior  
- Pip y virtualenv (opcional, recomendado)  
- Navegador para Selenium (Chrome/Chromium o Gecko/Firefox) y su driver correspondiente en modo headless  

## Hardware

- CPU multinúcleo (recomendado)  
- 8 GB RAM mínimo; 16 GB recomendado si ejecuta Selenium o contenedores concurrentes  
- ~20 GB de espacio libre para dependencias, datos y logs  

# Instalación

1. Clona el repositorio: git clone https://github.com/marcewp15/SocialMinerApp.git
2. Crear y activar un entorno virtual (recomendado)
python -m venv env
source env/bin/activate # Linux/macOS
env\Scripts\activate # Windows
3. Instalar dependencias
pip install -r requirements.txt

4. Configurar variables de entorno

Crea un archivo `.env` en la raíz con al menos:

FLASK_APP=app.py
FLASK_ENV=development

Opcionales
CHROME_DRIVER_PATH=/path/to/chromedriver
SCRAPER_TARGET_URL=https://example.com

5. Ejecutar localmente

python -m flask run --port 5000

O, para producción con Gunicorn:
gunicorn -w 4 -b 0.0.0.0:8000 app:app


**Notas:**  
- Si usas Selenium, asegúrate de que el driver sea compatible con la versión de Chrome/Chromium instalada.  
- Para entornos sin interfaz, habilita el modo headless en las opciones de Selenium.

# Uso

## Estructura del proyecto

- `app.py` o `main.py`: punto de entrada de la aplicación Flask  
- `templates/`: plantillas HTML (si aplica)  
- `static/`: activos estáticos (CSS, JS, imágenes)  
- `scraping/`: módulos de scraping (pipeline, parsers)  
- `config/`: archivos de configuración  
- `tests/`: pruebas unitarias  

## Endpoints principales (ejemplos)

- `GET /`: página de bienvenida o dashboard  
- `GET /scrape?target=<URL>`: realiza scraping del objetivo y devuelve resultados en JSON  
- `POST /scrape`: recibe payload con parámetros de scraping y devuelve resultados  
- `GET /export`: exporta los datos capturados en formatos descargables (CSV/JSON)  

**Notas:**  
Ajusta los endpoints reales conforme a tu implementación específica.

## Exportación de datos

Opciones: CSV, JSON  

Ejemplos:

/export?format=csv
/export?format=json


# Despliegue

## Despliegue local

- Usa Gunicorn para producción:  
  `gunicorn -w 4 -b 0.0.0.0:8000 app:app`  
- Configura Nginx como proxy inverso si es necesario  
- Asegura variables de entorno sensibles y habilita SSL en producción

## Contenedores con Docker

- Construcción:  
  `docker build -t socialminerapp:latest .`  
- Ejecución:  
  `docker run -d -p 8000:8000 --env-file .env socialminerapp:latest`  

**Notas:**  
Incluye en el Dockerfile la instalación de dependencias y la configuración de Chrome/Chromium para Selenium si aplica.

# Pruebas

- `pytest` para pruebas unitarias  
- Pruebas de integración para endpoints  
- Pruebas de rendimiento para scraping básico (con límites y tiempos de espera)

# Contribución

- Crea una rama:  
  `git checkout -b feature/nueva-funcionalidad`  
- Implementa cambios y añade pruebas  
- Abre un pull request describiendo el cambio  
- Revisa las directrices de código y el estilo del proyecto

# Seguridad y consideraciones éticas

- No realizar scraping de sitios sin permiso o sin cumplir sus términos de servicio.  
- Implementar límites de tasa y manejo responsable de datos.  
- Evitar recolectar información sensible sin consentimiento.

# Registro y logs

- Configura logging en Python (nivel DEBUG durante desarrollo, INFO en producción)  
- Almacena logs en archivos o en un servicio de logs si se despliega en la nube

# Licencia

Este proyecto se distribuye bajo la licencia MIT (o la que corresponda). Sustituye con la licencia elegida.








