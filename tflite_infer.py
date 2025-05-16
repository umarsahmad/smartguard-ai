import tensorflow as tf
import numpy as np
from PIL import Image
import sys

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="models/mask_classifier.tflite")
interpreter.allocate_tensors()

# Get input & output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load and preprocess image
def preprocess_image(img_path):
    img = Image.open(img_path).convert("RGB")
    img = img.resize((128, 128))  # same as training size
    img_array = np.array(img) / 255.0  # normalize
    img_array = img_array.astype(np.float32)
    img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 224, 224, 3)
    return img_array

# Predict function
def predict(img_path):
    input_data = preprocess_image(img_path)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    return output

# For CLI usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tflite_infer.py path_to_image.jpg")
        sys.exit(1)
    
    img_path = sys.argv[1]
    prediction = predict(img_path)
    class_names = ["Incorrect Mask", "With Mask", "Without Mask"]
    predicted_class = class_names[np.argmax(prediction)]
    print(f"Prediction: {predicted_class} | Confidence: {np.max(prediction):.2f}")

