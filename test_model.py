import pickle

# 1. Load the model (pipeline with its own vectorizer)
with open("SVM_noSVD_8651_121374.dill", "rb") as f:
    model = pickle.load(f)

print("[INFO] Model loaded successfully.")

# 2. Predict directly using raw text
test_review = "Please add fingerprint lock support."
prediction = model.predict([test_review])  # ✅ Raw text

print(f"Prediction for review: \"{test_review}\"")
print("=> Predicted label:", prediction[0])
