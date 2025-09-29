# Usa la imagen base de Python (3.10 es una buena elección)
FROM python:3.10-slim

# Instala las dependencias del sistema necesarias para pycairo/xhtml2pdf
# Esto es lo que resuelve el error "Dependency 'cairo' not found"
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    pkg-config \
    libcairo2-dev \
    # Limpia la caché para reducir el tamaño final de la imagen
    && \
    rm -rf /var/lib/apt/lists/*

# Configura el directorio de trabajo
WORKDIR /usr/src/app

# Copia los requisitos e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto
COPY . .

# Comando de inicio (Deja este CMD, es el que ejecutaría tu Custom Start Command)
# Reemplaza 'condominioBACK' con el nombre real de tu carpeta WSGI si es diferente.
CMD ["gunicorn", "condominioBACK.wsgi:application"]