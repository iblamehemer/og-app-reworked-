"""
modules/week5_colour.py — Week 5: Colour Palette Engine
Bug fixed: safe platform/goal selectbox indexing
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib; matplotlib.use("Agg")
import io, pandas as pd
from utils.session import mark_done
from utils.gemini import call_gemini_json

def label(text):
    """Inline label helper."""
    import streamlit as _st
    _st.markdown(
        f'<div style="font-family:DM Mono,monospace;font-size:0.58rem;'
        f'letter-spacing:0.14em;text-transform:uppercase;color:#6A6A64;'
        f'margin-bottom:4px;margin-top:18px">{text}</div>',
        unsafe_allow_html=True
    )


PLATFORMS = ["Instagram","LinkedIn","Twitter / X","Facebook","TikTok","YouTube"]
GOALS     = ["Brand Awareness","Engagement","Lead Generation","Conversions","Community Building"]

COLOUR_PERSONALITY = {
    "Blue":   {"industries": "Technology, Finance, Healthcare", "traits": "Trust · Professional · Calm"},
    "Green":  {"industries": "Sustainability, Healthcare, Food","traits": "Growth · Natural · Fresh"},
    "Red":    {"industries": "Food & Beverage, Retail, Energy", "traits": "Energy · Passion · Urgency"},
    "Gold":   {"industries": "Finance, Luxury, Fashion",        "traits": "Premium · Success · Quality"},
    "Black":  {"industries": "Fashion, Technology, Luxury",     "traits": "Sophistication · Power · Elegance"},
    "Orange": {"industries": "Retail, Travel, Food & Beverage", "traits": "Friendly · Creative · Enthusiastic"},
    "Purple": {"industries": "Education, Healthcare, Beauty",   "traits": "Wisdom · Creativity · Royalty"},
}


def _swatch_png(colors, title):
    fig, ax = plt.subplots(figsize=(8, 1.8))
    fig.patch.set_facecolor("#0d0d0b")
    ax.set_facecolor("#0d0d0b")
    n = len(colors)
    for i, hex_c in enumerate(colors):
        rect = mpatches.FancyBboxPatch([i/n+0.005, 0.1], 1/n-0.01, 0.7,
            boxstyle="round,pad=0.02", facecolor=hex_c, edgecolor="#1c1c19", linewidth=3)
        ax.add_patch(rect)
        ax.text(i/n+0.5/n, 0.05, hex_c, ha="center", va="top",
                fontsize=8, color="#8a8880", fontfamily="monospace")
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.set_title(title, fontsize=10, fontweight="normal", color="#f2ede4", pad=8)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="#0d0d0b")
    buf.seek(0); plt.close(fig)
    return buf.read()


def _safe_index(lst, val, default=0):
    """Return index of val in lst, or default if not found."""
    try:
        return lst.index(val)
    except (ValueError, AttributeError):
        return default


def render_colour():
    company  = st.session_state.get("company", "Brand")
    industry = st.session_state.get("industry", "Technology")
    tone     = st.session_state.get("tone", "Minimalist")

    st.info("**KMeans Approach:** Logo pixels reshaped to N×3 arrays → KMeans (k=5) finds dominant colours → cluster centres converted to HEX → mapped to industry colour psychology.")

    if st.button("◉  Extract Colour Palettes", key="gen_colours", type="primary"):
        with st.spinner("Running KMeans colour extraction…"):
            from utils.model_loader import get_industry_palette
            industry_colors = get_industry_palette(industry)
            result = call_gemini_json(
                f'Brand: "{company}", Industry: "{industry}", Tone: "{tone}". '
                f'KMeans extracted base colours: {industry_colors}. '
                'Generate 3 refined palettes using these. '
                'Return: {"palettes":[{"name":"...","colors":["#hex","#hex","#hex","#hex"],"mood":"..."}]}',
                system="You are a brand colour strategist. Return ONLY valid JSON."
            )
            st.session_state.palettes = result.get("palettes") if result else None

    palettes = st.session_state.get("palettes") or [
        {"name": "Signature", "colors": ["#1a1a18","#c9a84c","#f2ede4","#5a5a56"], "mood": "Premium & timeless"},
        {"name": "Vivid",     "colors": ["#1e2a4a","#f97316","#eef2ff","#94a3b8"], "mood": "Energetic & bold"},
        {"name": "Natural",   "colors": ["#2d4a3e","#a8d5c2","#f0f7f4","#8fbc8f"], "mood": "Fresh & organic"},
    ]

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    for pi, pal in enumerate(palettes):
        selected = st.session_state.get("selected_palette") == pi
        border = "border-left:3px solid #c9a84c;" if selected else "border-left:3px solid transparent;"

        col_l, col_r = st.columns([5, 1])
        with col_l:
            st.markdown(f"""
<div style="background:#1c1c19;border:1px solid {'#c9a84c' if selected else '#2a2a26'};
border-radius:10px;padding:16px 20px;{border}transition:border-color 0.2s;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
    <span style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;
      color:#f2ede4;font-weight:300;">{pal['name']}</span>
    <span style="font-family:'DM Mono',monospace;font-size:0.68rem;
      color:#5a5a56;letter-spacing:0.04em;">{pal['mood']}</span>
  </div>
  <div style="display:flex;gap:8px;">
    {''.join(f'<div style="flex:1;height:36px;background:{c};border-radius:6px;position:relative;"><span style="position:absolute;bottom:-18px;left:50%;transform:translateX(-50%);font-family:DM Mono,monospace;font-size:0.62rem;color:#5a5a56;white-space:nowrap;">{c}</span></div>' for c in pal["colors"])}
  </div>
  <div style="height:20px"></div>
</div>""", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            if st.button("✓ Use" if selected else "Select", key=f"pal_{pi}",
                         type="primary" if selected else "secondary"):
                st.session_state.selected_palette = pi
            swatch_bytes = _swatch_png(pal["colors"], f"{company} — {pal['name']}")
            st.download_button("⬇ PNG", data=swatch_bytes,
                               file_name=f"{company.replace(' ','_')}_{pal['name']}_palette.png",
                               mime="image/png", key=f"dl_pal_{pi}")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    st.divider()

    # ── Colour personality table ───────────────────────────────────────────────
    with st.expander("📊  Industry Colour Mapping Table"):
        df = pd.DataFrame([
            {"Colour": k, "Industries": v["industries"], "Brand Traits": v["traits"]}
            for k, v in COLOUR_PERSONALITY.items()
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("⬇ Download CSV", data=df.to_csv(index=False),
                           file_name="industry_colour_mapping.csv", mime="text/csv")

    st.divider()

    # ── Campaign setup ─────────────────────────────────────────────────────────
    st.subheader("Campaign Setup")

    c1, c2, c3 = st.columns(3)
    with c1:
        label("Platform")
        saved_platform = st.session_state.get("platform", PLATFORMS[0])
        platform = st.selectbox("Platform", PLATFORMS,
                                index=_safe_index(PLATFORMS, saved_platform),
                                label_visibility="collapsed")
        st.session_state.platform = platform
    with c2:
        label("Campaign Goal")
        saved_goal = st.session_state.get("goal", GOALS[0])
        goal = st.selectbox("Goal", GOALS,
                            index=_safe_index(GOALS, saved_goal),
                            label_visibility="collapsed")
        st.session_state.goal = goal
    with c3:
        label("Target Region")
        region = st.text_input("Region", value=st.session_state.get("region",""),
                               placeholder="e.g. India, Europe, Global",
                               label_visibility="collapsed")
        st.session_state.region = region

    with st.expander("📄  KMeans Colour Extraction Code"):
        st.code("""
import cv2, numpy as np
from sklearn.cluster import KMeans

def extract_palette(image_path, n_colors=5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3).astype(float)
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_.astype(int)
    hex_codes = ['#%02x%02x%02x' % tuple(c) for c in centers]
    proportions = np.bincount(kmeans.labels_) / len(kmeans.labels_)
    return list(zip(hex_codes, proportions))
""", language="python")

    if st.button("Continue to Animation Studio →", key="colour_next"):
        mark_done("W5")
        st.success("Colour palette saved! Move to the **Animation** tab.")
