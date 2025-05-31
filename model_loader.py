import os
import dill  # or `import pickle` if you saved with pickle
import logging

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'SVM_noSVD_8651_121374.dill')

model = None

try:
    with open(MODEL_PATH, 'rb') as f:
        model = dill.load(f)
    print("[INFO] Model pipeline loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load model pipeline: {e}")
