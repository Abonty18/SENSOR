import dill
import re
import threading  # Add this import

MODEL_PATH = "models\\Hierarchical_SGD_noSVD_8607_121374.dill"

# Sample review for testing
SAMPLE_REVIEW = "The app is great and works perfectly!"

# Preprocessing function (same as in your Flask app)
def preprocess_review(review):
    review = review.lower()  # Convert to lowercase
    review = re.sub(r'@[^\s]+', ' ', review)  # Remove usernames
    review = re.sub(r'http[^\s]+', ' ', review)  # Remove HTML links
    review = re.sub(r'\d+', '', review)  # Remove numbers
    review = re.sub(r'[^a-zA-Z,;.?!:\s]', ' ', review)  # Remove special characters except .,;?!:
    review = re.sub(r'\b\w{1,2}\b', '', review)  # Remove short words of length 1 and 2
    review = re.sub(r'\s+', ' ', review).strip()  # Replace multiple spaces with a single space
    return review

# Load the model from the .dill file
try:
    with open(MODEL_PATH, 'rb') as model_file:
        model = dill.load(model_file)
    print("[INFO] Model loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load the model: {e}")
    exit(1)

# Debug: Print model object and type
print(f"[DEBUG] Model type: {type(model)}")

# Debug: Check if the model has a 'predict' method
if hasattr(model, 'predict'):
    print("[DEBUG] Model has a 'predict' method.")
else:
    print("[ERROR] Model does not have a 'predict' method.")
    exit(1)

# Preprocess the sample review
try:
    processed_review = preprocess_review(SAMPLE_REVIEW)
    print(f"[INFO] Preprocessed review: {processed_review}")
except Exception as e:
    print(f"[ERROR] Failed to preprocess the review: {e}")
    exit(1)

# Debug: Check input length
print(f"[DEBUG] Input length: {len(processed_review)}")

# Debug: Check TfidfVectorizer output
try:
    tfidf_output = model.named_steps['tfidf'].transform([processed_review])
    print(f"[DEBUG] TfidfVectorizer output shape: {tfidf_output.shape}")
    print(f"[DEBUG] TF-IDF transformed input (first few values): {tfidf_output.toarray()[0][:10]}")
except Exception as e:
    print(f"[ERROR] TfidfVectorizer failed: {e}")
    exit(1)

# Check vocabulary of the TfidfVectorizer
print(f"[DEBUG] TfidfVectorizer vocabulary: {model.named_steps['tfidf'].get_feature_names_out()[:20]}")

# Test with a more relevant review based on the vocabulary
simple_review = "app version 10 is great"
print(f"[DEBUG] Input to model.predict for simple review: {simple_review}")
try:
    simple_prediction = model.predict([simple_review])
    if simple_prediction is not None and len(simple_prediction) > 0:
        print(f"[DEBUG] Prediction for simple review: {simple_prediction}")
    else:
        print("[ERROR] Model returned an empty prediction or None.")
except Exception as e:
    print(f"[ERROR] Failed to make a prediction for simple review: {e}")


# Make a prediction using the model with the processed review
try:
    print(f"[DEBUG] Input to model.predict: {[processed_review]}")
    prediction = model.predict([processed_review])  # Direct prediction without timeout
    print(f"[DEBUG] Prediction: {prediction}")
except Exception as e:
    print(f"[ERROR] Failed to make a prediction: {e}")
    exit(1)

print("[INFO] Model test completed successfully!")
