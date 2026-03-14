"""
models/scripts/train_campaign_model.py
Week 7 Deliverable: Campaign Prediction Model — Standalone Training Script
Tools: Pandas, scikit-learn (Random Forest, GBM, Linear Regression), joblib

Usage:
    python train_campaign_model.py --data data/marketing.csv
    python train_campaign_model.py --demo
"""

import argparse
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

TARGETS   = ["ctr", "roi", "engagement_score"]
CAT_COLS  = ["platform", "region", "campaign_type", "goal"]
NUM_COLS  = ["budget", "duration_days", "audience_size"]
MODEL_DIR = "models"


def generate_synthetic_data(n: int = 2000) -> pd.DataFrame:
    """Generate realistic synthetic marketing dataset."""
    np.random.seed(42)
    platforms  = ["Instagram", "LinkedIn", "Twitter", "Facebook", "TikTok"]
    regions    = ["North America", "Europe", "Asia", "India", "Global"]
    camp_types = ["Image", "Video", "Carousel", "Story", "Reel"]
    goals      = ["awareness", "engagement", "conversion", "lead_gen"]

    df = pd.DataFrame({
        "platform":      np.random.choice(platforms, n),
        "region":        np.random.choice(regions, n),
        "campaign_type": np.random.choice(camp_types, n),
        "goal":          np.random.choice(goals, n),
        "budget":        np.random.randint(500, 50000, n),
        "duration_days": np.random.randint(3, 30, n),
        "audience_size": np.random.randint(1000, 500000, n),
    })

    # Realistic targets with platform/type effects
    is_tiktok   = (df["platform"] == "TikTok").astype(float)
    is_video    = (df["campaign_type"] == "Video").astype(float)
    is_insta    = (df["platform"] == "Instagram").astype(float)
    is_linkedin = (df["platform"] == "LinkedIn").astype(float)

    df["ctr"]              = (np.random.uniform(0.5, 8.0, n) + is_tiktok * 1.5 + is_video * 0.8).clip(0.1, 12)
    df["roi"]              = (np.random.uniform(0.8, 5.5, n) + np.log1p(df["budget"]) * 0.08 + is_linkedin * 0.5).clip(0.3, 8)
    df["engagement_score"] = (np.random.uniform(2, 14, n) + is_insta * 1.2 + is_video * 1.5).clip(0.5, 20)
    return df


def build_pipeline(model) -> Pipeline:
    """Build sklearn Pipeline with OneHotEncoder + regressor."""
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT_COLS),
        ("num", "passthrough", NUM_COLS),
    ])
    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def evaluate(pipeline, X_test, y_test, target_name: str) -> dict:
    preds = pipeline.predict(X_test)
    rmse  = np.sqrt(mean_squared_error(y_test, preds))
    r2    = r2_score(y_test, preds)
    print(f"  {target_name:18s} | RMSE: {rmse:.4f} | R2: {r2:.4f}")
    return {"rmse": round(rmse, 4), "r2": round(r2, 4)}


def train(data_path: str = None, demo: bool = False):
    print("=" * 55)
    print("BrandMind AI — Campaign Prediction Model (Week 7)")
    print("=" * 55)

    # Load data
    if demo or not data_path or not os.path.exists(data_path or ""):
        print("Using synthetic marketing data for demonstration...")
        df = generate_synthetic_data(2000)
    else:
        print(f"Loading: {data_path}")
        df = pd.read_csv(data_path)
        df.dropna(inplace=True)

    print(f"Dataset: {df.shape}")
    print(df.describe().round(2))

    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    X = df[CAT_COLS + NUM_COLS]
    results_summary = {}

    models_to_train = [
        ("LinearRegression",    LinearRegression()),
        ("RandomForest",        RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)),
        ("GradientBoosting",    GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, random_state=42)),
    ]

    for target in TARGETS:
        print(f"\n── Target: {target.upper()} ──")
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        best_pipe, best_rmse = None, float("inf")
        for model_name, model in models_to_train:
            pipe = build_pipeline(model)
            pipe.fit(X_train, y_train)
            metrics = evaluate(pipe, X_test, y_test, model_name)
            if metrics["rmse"] < best_rmse:
                best_rmse = metrics["rmse"]
                best_pipe = pipe
                results_summary[target] = {"best_model": model_name, **metrics}

        # Save best model
        save_path = os.path.join(MODEL_DIR, f"campaign_{target}_best.pkl")
        joblib.dump(best_pipe, save_path)
        print(f"  Best model saved: {save_path}")

    # Feature importance (Random Forest on CTR)
    print("\n── Feature Importance (CTR — Random Forest) ──")
    rf_pipe = build_pipeline(RandomForestRegressor(n_estimators=200, random_state=42))
    rf_pipe.fit(X, df["ctr"])

    enc = rf_pipe.named_steps["preprocessor"]
    cat_feature_names = enc.named_transformers_["cat"].get_feature_names_out(CAT_COLS).tolist()
    all_feature_names = cat_feature_names + NUM_COLS
    importances = rf_pipe.named_steps["model"].feature_importances_

    feat_df = pd.DataFrame({"Feature": all_feature_names, "Importance": importances})
    feat_df = feat_df.sort_values("Importance", ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(feat_df["Feature"][::-1], feat_df["Importance"][::-1], color="#b8975a")
    ax.set_title("Top 15 Feature Importances — CTR Prediction", fontweight="bold")
    ax.set_xlabel("Importance Score")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig("outputs/campaign_feature_importance.png", dpi=150)
    plt.close()
    print("Saved: outputs/campaign_feature_importance.png")

    # Regional engagement chart
    region_stats = df.groupby("region")[["ctr", "roi", "engagement_score"]].mean().round(3)
    print("\nRegional Performance Averages:")
    print(region_stats)
    region_stats.to_csv("outputs/regional_engagement.csv", index=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, col, label, color in zip(
        axes,
        ["ctr", "roi", "engagement_score"],
        ["Avg CTR (%)", "Avg ROI (x)", "Avg Engagement (%)"],
        ["#1a1a18", "#b8975a", "#2d4a3e"],
    ):
        region_stats[col].sort_values().plot(kind="barh", ax=ax, color=color)
        ax.set_title(label, fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
    plt.suptitle("Regional Campaign Performance Insights", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig("outputs/regional_engagement.png", dpi=150)
    plt.close()
    print("Saved: outputs/regional_engagement.png")

    # Results summary
    print("\n── Model Summary ──")
    for target, res in results_summary.items():
        print(f"  {target}: {res['best_model']} | RMSE={res['rmse']} | R2={res['r2']}")

    return results_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BrandMind Campaign Model Trainer (Week 7)")
    parser.add_argument("--data", type=str, default=None, help="Path to marketing.csv")
    parser.add_argument("--demo", action="store_true",    help="Run with synthetic data")
    args = parser.parse_args()
    train(data_path=args.data, demo=args.demo)
