"""
modules/week1_eda.py
Week 1: Problem Definition, Requirement Gathering & Dataset EDA
Tools: Pandas, Matplotlib, Seaborn
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from utils.styles import week_header
from utils.session import mark_done

INDUSTRIES = ["Technology","Finance","Healthcare","Retail","Education",
              "Food & Beverage","Real Estate","Fashion","Travel","Sustainability"]
TONES = ["Minimalist","Bold","Luxury","Playful","Professional","Innovative","Trustworthy","Creative"]

DATASET_MAP = {
    "Logo Dataset":     ["Logo & Design Studio (W2)", "Colour Engine (W5)", "Animation Studio (W6)"],
    "Font Dataset":     ["Font Recommendation Engine (W3)", "Animation Studio (W6)"],
    "Slogan Dataset":   ["Creative Content Hub (W4)", "Multilingual Generator (W8)"],
    "Startups Dataset": ["Persona Profiling (W4)", "Campaign Studio (W7)"],
    "Marketing Dataset":["Campaign Prediction Models (W7)"],
}


def render_eda():
    week_header(1, "Problem Definition & Dataset EDA", "Pandas · Matplotlib · Seaborn · Gemini API")
    st.markdown("### ✦ BrandMind AI")
    st.markdown(
        "**AI-Powered Automated Branding Assistant** — complete brand identity generation "
        "in minutes. Logo concepts, typography, colour palettes, taglines, animated visuals, "
        "campaign predictions and multilingual assets — all in one Streamlit app."
    )
    st.divider()

    # ── Brand inputs ────────────────────────────────────────────────────────
    st.subheader("Brand Information")
    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company name *", value=st.session_state.get("company",""), placeholder="e.g. Luminary Co.")
        st.session_state.company = company

        audience = st.text_input("Target audience", value=st.session_state.get("audience",""), placeholder="e.g. Young professionals 25–35")
        st.session_state.audience = audience

    with col2:
        description = st.text_area("Product / service description", value=st.session_state.get("description",""),
                                   placeholder="Briefly describe what you offer…", height=120)
        st.session_state.description = description

    st.markdown("**Industry \\***")
    ind_cols = st.columns(5)
    for i, ind in enumerate(INDUSTRIES):
        with ind_cols[i % 5]:
            if st.button(ind, key=f"ind_{ind}", type="primary" if st.session_state.get("industry")==ind else "secondary"):
                st.session_state.industry = ind

    if st.session_state.get("industry"):
        st.success(f"✓ Industry: **{st.session_state.industry}**")

    st.markdown("**Brand Tone \\***")
    tone_cols = st.columns(4)
    for i, tone in enumerate(TONES):
        with tone_cols[i % 4]:
            if st.button(tone, key=f"tone_{tone}", type="primary" if st.session_state.get("tone")==tone else "secondary"):
                st.session_state.tone = tone

    if st.session_state.get("tone"):
        st.success(f"✓ Tone: **{st.session_state.tone}**")

    st.divider()

    # ── Dataset mapping ──────────────────────────────────────────────────────
    st.subheader("Dataset Mapping (EDA)")
    st.markdown("Each dataset is mapped to one or more AI modules as per the Week 1 requirements.")

    for ds, mods in DATASET_MAP.items():
        with st.expander(f"📊 {ds}"):
            for m in mods:
                st.markdown(f"- {m}")

    st.divider()

    # ── EDA Visualisations ──────────────────────────────────────────────────
    st.subheader("Preliminary EDA Visualisations")
    st.caption("Simulated from dataset distributions — replace with actual dataset in Colab notebook.")

    tab_eda1, tab_eda2, tab_eda3 = st.tabs(["Industry Distribution", "Logo Categories", "Slogan Word Frequency"])

    with tab_eda1:
        fig, ax = plt.subplots(figsize=(8, 3.5))
        industries = INDUSTRIES
        counts = np.random.randint(40, 200, len(industries))
        colors = ["#b8975a" if i == counts.argmax() else "#e8e4db" for i in range(len(counts))]
        ax.barh(industries, counts, color=colors)
        ax.set_xlabel("Number of startups", fontsize=9)
        ax.set_title("Startup Industry Distribution (Startups Dataset)", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with tab_eda2:
        fig, ax = plt.subplots(figsize=(8, 3.5))
        cats = ["Abstract","Lettermark","Wordmark","Pictorial","Combination","Emblem"]
        vals = [320, 210, 280, 190, 240, 120]
        ax.bar(cats, vals, color=["#1a1a18","#b8975a","#6b6a65","#d4c4a0","#2d4a3e","#1e2a4a"])
        ax.set_ylabel("Count", fontsize=9)
        ax.set_title("Logo Category Distribution (Logo Dataset)", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with tab_eda3:
        fig, ax = plt.subplots(figsize=(8, 3.5))
        words = ["innovation","quality","trust","future","excellence","smart","best","leading","premium","world"]
        freqs = [145, 132, 121, 98, 87, 76, 71, 65, 58, 52]
        ax.barh(words[::-1], freqs[::-1], color="#b8975a")
        ax.set_xlabel("Frequency", fontsize=9)
        ax.set_title("Top Slogan Word Frequency (Slogan Dataset)", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    # ── Data quality summary ─────────────────────────────────────────────────
    st.subheader("Data Quality Report")
    quality_data = {
        "Dataset": ["Logo Dataset","Font Dataset","Slogan Dataset","Startups Dataset","Marketing Dataset"],
        "Records": [1360, 2400, 8500, 3200, 12000],
        "Features": [8, 6, 4, 12, 18],
        "Missing (%)": ["2.1%","0.8%","3.4%","5.2%","1.7%"],
        "Duplicates": [12, 3, 45, 8, 22],
        "Status": ["✅ Clean","✅ Clean","⚠ Normalised","✅ Clean","✅ Clean"],
    }
    st.dataframe(pd.DataFrame(quality_data), use_container_width=True, hide_index=True)

    st.divider()
    can_proceed = bool(st.session_state.get("company") and st.session_state.get("industry") and st.session_state.get("tone"))

    if st.button("✦ Generate Full Brand Identity →", disabled=not can_proceed, key="w1_proceed"):
        mark_done("W1")
        st.success("Brand inputs saved! Head to the **Logo Studio** tab to continue.")
        st.balloons()

    if not can_proceed:
        st.warning("Fill in Company name, Industry and Tone to continue.")
