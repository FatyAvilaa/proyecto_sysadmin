from flask import Flask, request, render_template, jsonify
import requests
import psycopg2
import os

app = Flask(__name__)

# Función para leer secrets desde /run/secrets/*
def load_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return None

# Cargar secrets de Docker (si existen)
DB_URL = load_secret("/run/secrets/db_url") \
         or os.getenv("DATABASE_URL", "postgresql://fatima:password@db:5432/animalsdb")

CLASSIFIER_URL = os.getenv("CLASSIFIER_URL", "http://classifier:8000/predict")

# Conexión a la base de datos
def get_connection():
    return psycopg2.connect(DB_URL)

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']

    # Enviar imagen al clasificador
    files = {'file': (file.filename, file.read(), file.content_type)}
    response = requests.post(CLASSIFIER_URL, files=files)

    if response.status_code != 200:
        return jsonify({"error": "Classifier error"}), 500

    data = response.json()  # <--- AHORA VIENE JSON

    prediction = data['prediction']
    confidence = data['confidence']

    # Guardar en BD
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clasificaciones (nombre, resultado) VALUES (%s, %s)",
        (file.filename, prediction)
    )
    conn.commit()
    cur.close()
    conn.close()

    # Responder a frontend en JSON
    return jsonify({
        "prediction": prediction,
        "confidence": float(confidence)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
