# test_train.py

import os
import pytest
from tensorflow.keras.models import load_model

MODEL_PATH = "models/mask_classifier.h5"

# Test 1: Check if the model file exists
def test_model_file_exists():
    assert os.path.exists(MODEL_PATH), f"❌ Model file not found at {MODEL_PATH}"

# Test 2: Check if the model loads successfully
def test_model_load():
    try:
        model = load_model(MODEL_PATH)
    except Exception as e:
        pytest.fail(f"❌ Failed to load model: {e}")

# Test 3: Check if the model has the correct output shape (3 classes)
def test_output_layer_shape():
    model = load_model(MODEL_PATH)
    output_layer = model.layers[-1]
    assert output_layer.output_shape[-1] == 3, "❌ Model does not have 3 output classes"
