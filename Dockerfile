# Imagen base
FROM python:3.9-slim

# Variables de entorno para evitar buffer
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copiar el código fuente
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir flask psycopg2-binary flask-cors

# Exponer el puerto
EXPOSE 5003

# Comando para ejecutar el microservicio
CMD ["python", "editProduct.py"]
