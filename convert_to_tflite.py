# convert_to_tflite.py

import tensorflow as tf
import os

KERAS_MODEL_PATH = "models/mask_classifier.h5"
TFLITE_MODEL_PATH = "models/mask_classifier.tflite"

def convert_model():
    if not os.path.exists(KERAS_MODEL_PATH):
        raise FileNotFoundError("Keras model not found!")

    # Load Keras model
    model = tf.keras.models.load_model(KERAS_MODEL_PATH)

    # Convert to TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the TFLite model
    with open(TFLITE_MODEL_PATH, "wb") as f:
        f.write(tflite_model)

    print(f"✅ TFLite model saved at: {TFLITE_MODEL_PATH}")

if __name__ == "__main__":
    convert_model()
