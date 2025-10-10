# Imagen base de Python
FROM python:3.12-slim

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    libnss3 \
    libxss1 \
    libglib2.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo 
WORKDIR /app
COPY . /app

# Instalación de las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exposición del puerto 8000 (usado por Flask/Railway/Render para las pruebas)
EXPOSE 8000

# Iniciar app Flask 
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
