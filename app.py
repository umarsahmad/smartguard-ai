from flask import Flask, request, jsonify, render_template
import numpy as np
from PIL import Image
import tensorflow as tf
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/mask_classifier.tflite')

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Class labels
class_names = ["Incorrect Mask", "With Mask", "Without Mask"]

# Image preprocessing
def preprocess_image(image):
    img = image.convert("RGB")
    img = img.resize((128, 128))  # same as training size
    img_array = np.array(img) / 255.0  # normalize
    img_array = img_array.astype(np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Prediction function
def predict(image):
    input_data = preprocess_image(image)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = class_names[np.argmax(output)]
    confidence = float(np.max(output))
    return predicted_class, confidence

# Web UI
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence = None

    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400

        file = request.files["file"]

        if file.filename == "":
            return "No selected file", 400

        image = Image.open(file.stream)
        predicted_class, confidence = predict(image)
        return render_template("index.html", prediction=predicted_class, confidence=confidence)

    return render_template("index.html", prediction=prediction, confidence=confidence)


if __name__ == "__main__":
    app.run(debug=True)