import sys
import os
import numpy as np

# Add parent dir to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tflite_infer import predict

def test_tflite_prediction_runs():
    test_image = "test_images/img1.png"
    assert os.path.exists(test_image), f"Test image not found at {test_image}"

    prediction = predict(test_image)

    assert isinstance(prediction, np.ndarray), "Prediction is not a NumPy array"
    assert prediction.shape == (1, 3), f"Expected shape (1, 3), got {prediction.shape}"
    assert np.all(prediction >= 0.0) and np.all(prediction <= 1.0), "Probabilities must be between 0 and 1"
    assert np.isclose(np.sum(prediction), 1.0, atol=0.1), "Probabilities should sum close to 1"

    print(f"✅ Test passed — prediction: {prediction}")
