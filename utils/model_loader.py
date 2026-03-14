"""
utils/model_loader.py
Loads all trained models at Streamlit startup via @st.cache_resource
"""
import os
import numpy as np
import joblib
import json
import streamlit as st


MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")


@st.cache_resource
def load_font_model():
    """Load trained KNN font classifier."""
    knn_path = os.path.join(MODEL_DIR, "font_knn.pkl")
    enc_path = os.path.join(MODEL_DIR, "font_label_encoder.pkl")
    if os.path.exists(knn_path) and os.path.exists(enc_path):
        knn = joblib.load(knn_path)
        le  = joblib.load(enc_path)
        return knn, le
    return None, None


@st.cache_resource
def load_campaign_models():
    """Load trained campaign prediction models."""
    models = {}
    for target in ["ctr", "roi", "engagement_score"]:
        path = os.path.join(MODEL_DIR, f"campaign_{target}_best.pkl")
        if os.path.exists(path):
            models[target] = joblib.load(path)
    return models


@st.cache_resource
def load_colour_model():
    """Load trained KMeans colour model + industry palette manifest."""
    kmeans_path  = os.path.join(MODEL_DIR, "colour_kmeans.pkl")
    palette_path = os.path.join(MODEL_DIR, "industry_palettes.json")
    kmeans, palettes = None, {}
    if os.path.exists(kmeans_path):
        kmeans = joblib.load(kmeans_path)
    if os.path.exists(palette_path):
        with open(palette_path) as f:
            palettes = json.load(f)
    return kmeans, palettes


def predict_font_family(features_1d: np.ndarray) -> dict:
    """
    Predict font family from a flattened 1024-dim feature vector.
    Returns dict with predicted class and probabilities.
    """
    knn, le = load_font_model()
    if knn is None:
        return {"predicted": "sans-serif", "confidence": 0.0}
    features = features_1d.reshape(1, -1)
    pred_enc = knn.predict(features)[0]
    proba    = knn.predict_proba(features)[0]
    return {
        "predicted":  le.inverse_transform([pred_enc])[0],
        "confidence": float(proba.max()),
        "all_probs":  dict(zip(le.classes_, proba.round(4))),
    }


def predict_campaign_metrics(platform: str, region: str, campaign_type: str,
                              goal: str, budget: float, duration_days: int,
                              audience_size: int) -> dict:
    """
    Predict CTR, ROI, engagement using trained models.
    Returns dict with predicted values.
    """
    import pandas as pd
    models = load_campaign_models()
    if not models:
        return {"ctr": "4.2%", "roi": "3.1x", "engagement": "7.8%"}

    row = pd.DataFrame([{
        "platform":      platform,
        "region":        region,
        "campaign_type": campaign_type,
        "goal":          goal,
        "budget":        float(budget),
        "duration_days": float(duration_days),
        "audience_size": float(audience_size),
    }])

    results = {}
    try:
        if "ctr" in models:
            results["ctr"] = f"{models['ctr'].predict(row)[0]:.1f}%"
        if "roi" in models:
            results["roi"] = f"{models['roi'].predict(row)[0]:.2f}x"
        if "engagement_score" in models:
            results["engagement"] = f"{models['engagement_score'].predict(row)[0]:.1f}%"
    except Exception as e:
        results = {"ctr": "4.2%", "roi": "3.1x", "engagement": "7.8%", "error": str(e)}

    return results


def get_industry_palette(industry: str) -> list:
    """Return hex colour palette for a given industry from trained model."""
    _, palettes = load_colour_model()
    if industry in palettes:
        return palettes[industry]
    # Fallback
    return ["#1a1a18", "#b8975a", "#f5f0e8", "#6b6a65"]
