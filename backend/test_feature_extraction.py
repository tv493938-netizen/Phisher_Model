from src.feature_engineering import extract_features

# ✅ Example URL to test
test_url = "http://login.bankofamerica.security-alerts.com/login"

# Extract features from the test URL
features = extract_features(test_url)

# Print results
print("✅ Feature Extraction Test:")
print(f"Total Features Extracted: {len(features)}\n")
for k, v in features.items():
    print(f"{k:25}: {v}")
