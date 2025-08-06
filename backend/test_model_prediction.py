import pickle
import numpy as np
from src.feature_engineering import extract_features

# Load model artifacts
with open("model/stacked_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("model/top_features.pkl", "rb") as f:
    top_features = pickle.load(f)

# Test URL (phishing-style)
test_url = "http://secure-update-paypal.com/login"

# Extract & scale
features = extract_features(test_url)
X = np.array([features.get(f, 0) for f in top_features]).reshape(1, -1)
X_scaled = scaler.transform(X)

# Predict
pred = model.predict(X_scaled)[0]
proba = model.predict_proba(X_scaled)[0][1]

# Output
print("✅ Stacked Model Prediction Test")
print(f"Prediction: {'phishing' if pred == 1 else 'safe'}")
print(f"Confidence: {round(proba, 4)}")
