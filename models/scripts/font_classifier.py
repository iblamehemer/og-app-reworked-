"""
models/scripts/font_classifier.py
Week 3 Deliverable: Font Classification Model — Standalone Python Script
Tools: OpenCV, scikit-learn (KNN), NumPy, Pandas, joblib

Usage:
    python font_classifier.py --train           # Train the model
    python font_classifier.py --predict img.png # Predict font family
"""

import argparse
import os
import numpy as np
import pandas as pd
import cv2
import joblib
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns

# ── Config ────────────────────────────────────────────────────────────────────
IMG_SIZE      = (32, 32)
N_NEIGHBORS   = 5
MODEL_PATH    = "models/font_knn.pkl"
ENCODER_PATH  = "models/font_label_encoder.pkl"
MAPPING_PATH  = "data/industry_font_mapping.csv"

FONT_FAMILIES = ["serif", "sans-serif", "script", "monospace", "display"]

# Industry → font family lookup table (W3 deliverable)
INDUSTRY_FONT_MAPPING = {
    "Finance":         {"primary": "serif",      "secondary": "sans-serif", "rationale": "Trust and authority"},
    "Technology":      {"primary": "sans-serif",  "secondary": "monospace",  "rationale": "Modern and clean"},
    "Healthcare":      {"primary": "sans-serif",  "secondary": "serif",      "rationale": "Professional and clear"},
    "Fashion":         {"primary": "display",     "secondary": "serif",      "rationale": "Elegant and editorial"},
    "Education":       {"primary": "serif",       "secondary": "sans-serif", "rationale": "Authoritative and readable"},
    "Food & Beverage": {"primary": "script",      "secondary": "sans-serif", "rationale": "Warm and approachable"},
    "Retail":          {"primary": "sans-serif",  "secondary": "display",    "rationale": "Friendly and bold"},
    "Travel":          {"primary": "display",     "secondary": "sans-serif", "rationale": "Adventurous and inviting"},
    "Sustainability":  {"primary": "sans-serif",  "secondary": "script",     "rationale": "Natural and organic"},
    "Real Estate":     {"primary": "serif",       "secondary": "sans-serif", "rationale": "Trustworthy and established"},
}

# Brand tone → font style mapping
TONE_FONT_MAPPING = {
    "Luxury":       "serif",
    "Professional": "sans-serif",
    "Playful":      "script",
    "Bold":         "display",
    "Minimalist":   "sans-serif",
    "Innovative":   "sans-serif",
    "Trustworthy":  "serif",
    "Creative":     "display",
}


# ── Preprocessing ─────────────────────────────────────────────────────────────
def preprocess_font_image(path: str, size: tuple = IMG_SIZE) -> np.ndarray:
    """Load a font image, convert to grayscale, resize, normalize and flatten."""
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    img = cv2.resize(img, size)
    img = img / 255.0
    return img.flatten()


def load_dataset(data_dir: str):
    """
    Load font images from directory structure:
        data_dir/
            serif/img1.png ...
            sans-serif/img2.png ...
    Returns X (features), y (labels).
    """
    X, y = [], []
    for family in FONT_FAMILIES:
        family_dir = os.path.join(data_dir, family)
        if not os.path.exists(family_dir):
            continue
        for fname in os.listdir(family_dir):
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(family_dir, fname)
                try:
                    features = preprocess_font_image(path)
                    X.append(features)
                    y.append(family)
                except Exception as e:
                    print(f"  Skipping {path}: {e}")
    return np.array(X), np.array(y)


def generate_synthetic_data(n_samples: int = 500) -> tuple:
    """Generate synthetic font data for demonstration when real dataset unavailable."""
    np.random.seed(42)
    X = np.random.rand(n_samples, IMG_SIZE[0] * IMG_SIZE[1])
    y = np.random.choice(FONT_FAMILIES, n_samples)
    return X, y


# ── Training ──────────────────────────────────────────────────────────────────
def train(data_dir: str = None):
    """Train KNN font classifier and save model + lookup tables."""
    print("=" * 55)
    print("BrandMind AI — Font Classifier Training (Week 3)")
    print("=" * 55)

    # Load data
    if data_dir and os.path.exists(data_dir):
        print(f"Loading font images from: {data_dir}")
        X, y = load_dataset(data_dir)
        if len(X) == 0:
            print("No images found — using synthetic data.")
            X, y = generate_synthetic_data()
    else:
        print("No data_dir provided — using synthetic data for demonstration.")
        X, y = generate_synthetic_data()

    print(f"Dataset: {len(X)} samples | Classes: {set(y)}")

    # Encode labels
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    # Train KNN
    print(f"\nTraining KNN (k={N_NEIGHBORS}, metric=cosine)...")
    knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS, metric="cosine", weights="distance")
    knn.fit(X_train, y_train)

    # Evaluate
    y_pred = knn.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Confusion matrix
    os.makedirs("outputs", exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", ax=ax,
                xticklabels=le.classes_, yticklabels=le.classes_, cmap="Blues")
    ax.set_title("Font KNN — Confusion Matrix", fontweight="bold")
    ax.set_ylabel("True"); ax.set_xlabel("Predicted")
    plt.tight_layout()
    plt.savefig("outputs/font_confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/font_confusion_matrix.png")

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(knn, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)
    print(f"Model saved: {MODEL_PATH}")
    print(f"Encoder saved: {ENCODER_PATH}")

    # Save industry mapping table
    mapping_rows = []
    for industry, data in INDUSTRY_FONT_MAPPING.items():
        mapping_rows.append({
            "Industry": industry,
            "Primary Font Family": data["primary"],
            "Secondary Font Family": data["secondary"],
            "Rationale": data["rationale"],
        })
    df_map = pd.DataFrame(mapping_rows)
    os.makedirs("data", exist_ok=True)
    df_map.to_csv(MAPPING_PATH, index=False)
    print(f"Mapping table saved: {MAPPING_PATH}")

    return knn, le


# ── Prediction ────────────────────────────────────────────────────────────────
def predict(image_path: str, industry: str = None, tone: str = None) -> dict:
    """
    Predict font family for a given image.
    Optionally incorporate industry and tone for final recommendation.
    """
    if not os.path.exists(MODEL_PATH):
        print("Model not found — run with --train first.")
        return {}

    knn = joblib.load(MODEL_PATH)
    le  = joblib.load(ENCODER_PATH)

    features = preprocess_font_image(image_path).reshape(1, -1)
    pred_enc  = knn.predict(features)[0]
    predicted_family = le.inverse_transform([pred_enc])[0]
    proba = knn.predict_proba(features)[0]

    result = {
        "predicted_family": predicted_family,
        "confidence": round(float(proba.max()), 4),
        "all_probabilities": dict(zip(le.classes_, proba.round(4))),
    }

    # Industry override
    if industry and industry in INDUSTRY_FONT_MAPPING:
        ind_rec = INDUSTRY_FONT_MAPPING[industry]
        result["industry_recommendation"] = ind_rec["primary"]
        result["industry_rationale"] = ind_rec["rationale"]

    # Tone override
    if tone and tone in TONE_FONT_MAPPING:
        result["tone_recommendation"] = TONE_FONT_MAPPING[tone]

    print(f"\nFont Prediction for: {image_path}")
    print(f"  Predicted Family : {predicted_family}")
    print(f"  Confidence       : {result['confidence']:.1%}")
    if industry:
        print(f"  Industry Rec.    : {result.get('industry_recommendation')} ({industry})")
    if tone:
        print(f"  Tone Rec.        : {result.get('tone_recommendation')} ({tone})")

    return result


def recommend_for_brand(industry: str, tone: str) -> dict:
    """
    Get font recommendations purely from brand metadata
    (no image required — for Streamlit integration).
    """
    rec = {}
    if industry in INDUSTRY_FONT_MAPPING:
        rec.update(INDUSTRY_FONT_MAPPING[industry])
    if tone in TONE_FONT_MAPPING:
        rec["tone_primary"] = TONE_FONT_MAPPING[tone]
    return rec


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BrandMind Font Classifier (Week 3)")
    parser.add_argument("--train",       action="store_true", help="Train the KNN model")
    parser.add_argument("--predict",     type=str,            help="Path to font image to classify")
    parser.add_argument("--data_dir",    type=str, default=None, help="Path to font image dataset")
    parser.add_argument("--industry",    type=str, default=None, help="Industry for recommendation overlay")
    parser.add_argument("--tone",        type=str, default=None, help="Brand tone for recommendation overlay")
    parser.add_argument("--recommend",   action="store_true",  help="Get recommendation from industry + tone only")
    args = parser.parse_args()

    if args.train:
        train(data_dir=args.data_dir)
    elif args.predict:
        predict(args.predict, industry=args.industry, tone=args.tone)
    elif args.recommend:
        if not args.industry:
            print("--recommend requires --industry")
        else:
            result = recommend_for_brand(args.industry, args.tone or "")
            print(f"\nFont Recommendation for {args.industry} / {args.tone}:")
            for k, v in result.items():
                print(f"  {k}: {v}")
    else:
        # Default: train with synthetic data
        train()
