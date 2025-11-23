from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io

app = Flask(__name__)

MODEL_PATH = "my_model_reconstructed.keras"
model = load_model(MODEL_PATH, compile=False)

class_labels = [
    "dog",
    "horse",
    "elephant",
    "butterfly",
    "chicken",
    "cat",
    "cow",
    "sheep",
    "spider",
    "squirrel"
]

@app.route('/')
def home():
    return "Servicio de Clasificación (TensorFlow) activo."

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No image received"}), 400

    file = request.files['file']
    img_bytes = file.read()

    img = image.load_img(io.BytesIO(img_bytes), target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0

    preds = model.predict(x)
    predicted_class = int(np.argmax(preds))
    confidence = float(np.max(preds))

    label = class_labels[predicted_class]

    # ← AHORA DEVUELVE JSON
    return jsonify({
        "prediction": label,
        "confidence": confidence
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
