# ✦ BrandMind AI
### AI-Powered Automated Branding Assistant
*CRS AI Capstone 2025-26 · Scenario 1*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)

---

## Overview

BrandMind AI is a full-stack, AI-driven branding platform that generates a complete brand identity kit in minutes. It integrates **five core AI modules** across a 10-week development timeline:

| Module | Week | AI Technique |
|--------|------|-------------|
| Logo & Design Studio | W2 | CNN (TensorFlow/Keras) |
| Font Recommendation Engine | W3 | KNN (scikit-learn) |
| Creative Content Hub | W4 | Gemini API + NLTK |
| Colour Palette Engine | W5 | KMeans (OpenCV + scikit-learn) |
| Social Campaign Studio | W7 | Random Forest + Gradient Boosting |
| Animated Visuals Studio | W6 | Matplotlib + PyCairo |
| Multilingual Generator | W8 | Gemini API |
| Feedback Intelligence | W9 | NLTK Sentiment + Pandas |

---

## Project Structure

```
brandmind/
├── app.py                      # Main Streamlit entry point (W10)
├── requirements.txt            # Python dependencies
├── .streamlit/
│   ├── config.toml             # Streamlit theme + server config
│   └── secrets.toml            # API keys (DO NOT COMMIT)
├── modules/
│   ├── week1_eda.py            # Problem definition & EDA
│   ├── week2_logo.py           # CNN logo classification
│   ├── week3_font.py           # KNN font recommendation
│   ├── week4_slogan.py         # NLP slogan generation
│   ├── week5_colour.py         # KMeans colour extraction
│   ├── week6_animation.py      # Brand animation studio
│   ├── week7_campaign.py       # Campaign prediction
│   ├── week8_multilang.py      # Multilingual translation
│   ├── week9_feedback.py       # Feedback intelligence
│   └── week10_kit.py           # Brand kit + deployment
├── utils/
│   ├── gemini.py               # Gemini API wrapper
│   ├── session.py              # Streamlit session state
│   └── styles.py               # CSS injection + components
├── models/                     # Saved model artefacts (see below)
│   ├── logo_cnn.h5             # Trained CNN logo classifier
│   ├── logo_embeddings.npy     # CNN feature embeddings
│   ├── font_knn.pkl            # Serialised KNN font model
│   └── campaign_rf.pkl         # Random Forest campaign model
├── data/                       # Datasets (not committed — see Drive link)
│   ├── logos/                  # Logo image dataset
│   ├── fonts/                  # Font image dataset
│   ├── slogans.csv             # Slogan text dataset
│   ├── startups.csv            # Startup persona dataset
│   └── marketing.csv           # Marketing campaign dataset
├── assets/                     # Static assets (brand exports)
└── notebooks/                  # Google Colab training notebooks
    ├── Week1_EDA.ipynb
    ├── Week2_CNN_Logo.ipynb
    ├── Week3_Font_KNN.ipynb
    ├── Week4_Slogan_NLP.ipynb
    ├── Week5_Colour_KMeans.ipynb
    ├── Week6_Animation.ipynb
    ├── Week7_Campaign_ML.ipynb
    ├── Week8_Multilingual.ipynb
    └── Week9_Feedback.ipynb
```

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/brandmind-ai.git
cd brandmind-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Create `.streamlit/secrets.toml` (already in `.gitignore`):
```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

Get your free API key at [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 4. Run locally
```bash
streamlit run app.py
```

---

## Streamlit Cloud Deployment

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo → set `app.py` as main file
4. Add `GEMINI_API_KEY` in **Secrets** (Settings → Secrets)
5. Deploy — Streamlit Cloud handles the rest

---

## Datasets

Datasets are stored in Google Drive (not committed to GitHub due to size).

📁 [Dataset Drive Link](https://drive.google.com/drive/folders/YOUR_FOLDER_ID)

| Dataset | Records | Used In |
|---------|---------|---------|
| Logo Dataset | 1,360 images | W2, W5, W6 |
| Font Dataset | 2,400 images | W3, W6 |
| Slogan Dataset | 8,500 rows | W4, W8 |
| Startups Dataset | 3,200 rows | W4, W7 |
| Marketing Dataset | 12,000 rows | W7 |

To use locally:
```bash
mkdir data
# Download from Drive and place CSVs/folders inside data/
```

---

## Training the Models

All training notebooks are in `notebooks/`. Run them in **Google Colab** in order:

```
Week2 → Train CNN logo classifier → saves models/logo_cnn.h5
Week3 → Train KNN font classifier → saves models/font_knn.pkl
Week7 → Train RF campaign model   → saves models/campaign_rf.pkl
```

---

## Features

- **Logo Studio** — 5 CNN-classified logo concept directions
- **Font Engine** — KNN-matched typography pairings
- **Tagline Generator** — Gemini API with persona-aware prompting
- **Colour Palette** — KMeans extraction with industry colour psychology
- **Animation Studio** — Matplotlib FuncAnimation + PyCairo export (GIF/MP4)
- **Campaign Studio** — Random Forest CTR/ROI/engagement prediction + Plotly dashboard
- **Multilingual** — 5-language translation with BLEU score validation
- **Feedback Loop** — Star ratings → model refinement → NLTK sentiment analysis
- **Brand Kit** — One-click ZIP download of all assets

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Frontend | Streamlit, Plotly |
| Computer Vision | TensorFlow/Keras, OpenCV |
| Classical ML | scikit-learn (KNN, KMeans, Random Forest, GBM) |
| NLP & GenAI | Gemini API, HuggingFace Transformers, NLTK |
| Animation | Matplotlib animations, PyCairo, MoviePy |
| Data | Pandas, NumPy, Seaborn |
| Deployment | Streamlit Cloud, GitHub |

---

## PRD Document

The full Product Requirements Document (17 pages) covering all 10 weeks is included in:
```
BrandMind_AI_PRD.pdf
```

---

## License

CRS AI Capstone 2025-26. Academic use only.
