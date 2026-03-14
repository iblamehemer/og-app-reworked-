"""utils/session.py — Centralised session state initialisation"""
import streamlit as st


DEFAULTS = {
    # W1 – Brand inputs
    "company": "",
    "industry": "",
    "tone": "",
    "audience": "",
    "description": "",
    "region": "",
    "platform": "",
    "goal": "",

    # W2 – Logo
    "selected_logo": None,
    "logo_embeddings": None,

    # W3 – Font
    "fonts": None,
    "selected_font": None,

    # W4 – Slogans
    "slogans": None,
    "selected_slogan": None,

    # W5 – Colours
    "palettes": None,
    "selected_palette": 0,

    # W6 – Animation
    "animation_ready": False,
    "animation_style": "Fade-in + Typewriter",

    # W7 – Campaign
    "campaign": None,

    # W8 – Multilingual
    "translations": None,

    # W9 – Feedback
    "feedback": {},
    "feedback_saved": False,

    # Progress flags
    "done_W1": False, "done_W2": False, "done_W3": False, "done_W4": False,
    "done_W5": False, "done_W6": False, "done_W7": False, "done_W8": False,
    "done_W9": False, "done_W10": False,
}


def init_session():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v


def mark_done(week: str):
    st.session_state[f"done_{week}"] = True
