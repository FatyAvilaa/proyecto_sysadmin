# Imagen oficial de TensorFlow desde Docker Hub
FROM tensorflow/tensorflow:latest

WORKDIR /app

# Copiar los archivos del clasificador (modelo, código, etc.)
COPY . .

# Instalar versiones estables de Flask y Pillow compatibles con TensorFlow
RUN pip install --ignore-installed Flask==2.3.3 pillow

# Exponer el puerto del servidor Flask
EXPOSE 8000

# Ejecutar el servicio de clasificación
CMD ["python", "classifier_service.py"]