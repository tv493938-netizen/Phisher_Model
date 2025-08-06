import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import pickle
from src.feature_engineering import extract_features

# Load CSV file with columns: 'url', 'label'
df = pd.read_csv("data/phishing_data.csv")

# Extract 32 lexical features
X = df['url'].apply(extract_features).apply(pd.Series)
y = df['label']
top_features = X.columns.tolist()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define base learners
base_models = [
    ('xgb', xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', verbosity=0)),
    ('lgb', lgb.LGBMClassifier()),
    ('cb', cb.CatBoostClassifier(verbose=0))
]

# Meta learner
meta_model = LogisticRegression(max_iter=10000)

# Stacked model
stacked = StackingClassifier(
    estimators=base_models,
    final_estimator=meta_model,
    passthrough=True
)

# Train model
stacked.fit(X_train_scaled, y_train)

# Save artifacts
with open("model/stacked_model.pkl", "wb") as f:
    pickle.dump(stacked, f)

with open("model/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("model/top_features.pkl", "wb") as f:
    pickle.dump(top_features, f)

print("✅ Model trained and saved successfully.")
