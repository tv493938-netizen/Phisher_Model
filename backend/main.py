from fastapi import FastAPI
from pydantic import BaseModel
from src.feature_engineering import extract_features
import numpy as np
import pickle
import requests

app = FastAPI()

# Load model and artifacts
with open("model/stacked_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("model/top_features.pkl", "rb") as f:
    top_features = pickle.load(f)

# ✅ Your real API keys (for local testing)
VIRUSTOTAL_API_KEY = "1cb61b4772f57b54737a55700c648a78fdfa04b101beb25dc85325b382311f5d"
GOOGLE_API_KEY = "AIzaSyB5lPBFOGlIgyAwq1qHEz8Wz2sx6nYLdp0"

class URLInput(BaseModel):
    url: str

def predict_stacked_model(url: str) -> str:
    features = extract_features(url)
    x = np.array([features.get(f, 0) for f in top_features]).reshape(1, -1)
    x_scaled = scaler.transform(x)
    prediction = model.predict(x_scaled)[0]
    return "phishing" if prediction == 1 else "safe"

def check_virustotal(url: str) -> str:
    headers = { "x-apikey": VIRUSTOTAL_API_KEY }
    res = requests.post("https://www.virustotal.com/api/v3/urls", data={ "url": url }, headers=headers)
    if res.status_code != 200:
        return "unknown"
    analysis_id = res.json()["data"]["id"]
    res = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_id}", headers=headers)
    stats = res.json()["data"]["attributes"]["stats"]
    return "phishing" if stats.get("malicious", 0) > 0 else "safe"

def check_google_safe_browsing(url: str) -> str:
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
    payload = {
        "client": {"clientId": "phishing-detector", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{ "url": url }]
        }
    }
    res = requests.post(api_url, json=payload)
    return "phishing" if res.json().get("matches") else "safe"

@app.post("/check_url/")
async def check_url(data: URLInput):
    url = data.url
    model_result = predict_stacked_model(url)
    vt_result = check_virustotal(url)
    gsb_result = check_google_safe_browsing(url)
    external_vote = "phishing" if "phishing" in [vt_result, gsb_result] else "safe"
    final_verdict = model_result if model_result == external_vote else "suspicious"

    return {
        "url": url,
        "model_result": model_result,
        "virustotal": vt_result,
        "google_safe_browsing": gsb_result,
        "final_verdict": final_verdict
    }
