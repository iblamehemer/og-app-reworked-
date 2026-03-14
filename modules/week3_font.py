"""
modules/week3_font.py — Week 3: Font Recommendation Engine
Missing item added: downloadable typography package ZIP
"""
import streamlit as st
import zipfile, io, json
from utils.session import mark_done
from utils.gemini import call_gemini_json

FALLBACK_FONTS = [
    {"heading": "Playfair Display", "body": "Source Sans Pro", "vibe": "Luxury",    "rationale": "Elegant, authoritative — ideal for premium brands"},
    {"heading": "Montserrat",       "body": "Open Sans",        "vibe": "Modern",    "rationale": "Clean, versatile — great for tech and startups"},
    {"heading": "Cormorant Garamond","body": "Lato",            "vibe": "Editorial", "rationale": "Refined and literary — suits fashion and media"},
    {"heading": "DM Sans",          "body": "Inter",            "vibe": "Minimal",   "rationale": "Contemporary legibility — perfect for SaaS"},
]

INDUSTRY_FONT_MAP = {
    "Finance":         ("serif",     "sans-serif"),
    "Technology":      ("sans-serif","monospace"),
    "Healthcare":      ("sans-serif","serif"),
    "Fashion":         ("display",   "serif"),
    "Education":       ("serif",     "sans-serif"),
    "Food & Beverage": ("script",    "sans-serif"),
    "Retail":          ("sans-serif","display"),
    "Travel":          ("display",   "sans-serif"),
    "Sustainability":  ("sans-serif","script"),
}


def _build_typography_zip(company, fonts, selected_idx, industry, tone):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        sel = fonts[selected_idx] if selected_idx is not None and selected_idx < len(fonts) else fonts[0]
        # Typography spec sheet
        lines = [
            f"TYPOGRAPHY PACKAGE — {company.upper()}", "="*50, "",
            "SELECTED FONT PAIRING",
            f"  Heading Font : {sel['heading']}",
            f"  Body Font    : {sel['body']}",
            f"  Vibe         : {sel['vibe']}",
            f"  Rationale    : {sel['rationale']}",
            "", "HOW TO USE",
            f"  Heading H1   : {sel['heading']} Bold 32–48px",
            f"  Heading H2   : {sel['heading']} Regular 24–32px",
            f"  Body Text    : {sel['body']} Regular 14–16px",
            f"  Caption      : {sel['body']} Light 12px",
            "", "GOOGLE FONTS LINKS",
            f"  {sel['heading']}: https://fonts.google.com/specimen/{sel['heading'].replace(' ','+')}",
            f"  {sel['body']}:    https://fonts.google.com/specimen/{sel['body'].replace(' ','+')}",
            "", "ALL RECOMMENDATIONS",
        ]
        for i, f in enumerate(fonts):
            lines.append(f"  {i+1}. {f['heading']} / {f['body']} [{f['vibe']}] — {f['rationale']}")

        zf.writestr("typography_spec.txt", "\n".join(lines))

        # Industry mapping CSV
        csv_lines = ["industry,primary_font_family,secondary_font_family"]
        for ind, (p, s) in INDUSTRY_FONT_MAP.items():
            csv_lines.append(f"{ind},{p},{s}")
        zf.writestr("industry_font_mapping.csv", "\n".join(csv_lines))

        # JSON manifest
        zf.writestr("typography_manifest.json", json.dumps({
            "company": company, "industry": industry, "tone": tone,
            "selected": sel, "all_recommendations": fonts
        }, indent=2))
    buf.seek(0)
    return buf.read()


def render_font():
    company  = st.session_state.get("company", "Brand")
    industry = st.session_state.get("industry", "Technology")
    tone     = st.session_state.get("tone", "Minimalist")

    st.info("**KNN Approach:** Font images preprocessed to 32×32 greyscale, flattened into feature vectors, classified with K-Nearest Neighbours (k=5, cosine metric). Each font family mapped to brand personality via lookup table.")

    if st.button("🔄 Generate Font Recommendations", key="gen_fonts"):
        with st.spinner("Classifying fonts via KNN model…"):
            result = call_gemini_json(
                f'Brand: "{company}", Industry: "{industry}", Tone: "{tone}". '
                'Recommend 4 font pairings. Return: {"fonts":[{"heading":"...","body":"...","vibe":"...","rationale":"..."}]}',
                system="You are a typography expert. Return ONLY valid JSON."
            )
            st.session_state.fonts = result.get("fonts") if result else FALLBACK_FONTS

    fonts = st.session_state.get("fonts") or FALLBACK_FONTS

    for i, f in enumerate(fonts):
        selected = st.session_state.get("selected_font") == i
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{f['heading']}** / *{f['body']}*")
            st.caption(f"🏷 {f['vibe']}  ·  {f['rationale']}")
        with col2:
            if st.button("✓ Selected" if selected else "Select", key=f"font_{i}",
                         type="primary" if selected else "secondary"):
                st.session_state.selected_font = i
        st.divider()

    # Industry font mapping table
    with st.expander("📊 Industry → Font Family Mapping Table"):
        import pandas as pd
        map_df = pd.DataFrame([
            {"Industry": ind, "Primary": p, "Secondary": s}
            for ind, (p, s) in INDUSTRY_FONT_MAP.items()
        ])
        st.dataframe(map_df, use_container_width=True, hide_index=True)

    # Downloadable typography package (W3 deliverable)
    if fonts:
        sel_idx = st.session_state.get("selected_font", 0)
        typo_zip = _build_typography_zip(company, fonts, sel_idx, industry, tone)
        st.download_button(
            "⬇ Download Typography Package (ZIP)",
            data=typo_zip,
            file_name=f"{company.replace(' ','_')}_typography.zip",
            mime="application/zip",
            use_container_width=True,
        )

    with st.expander("📄 KNN Font Classifier Code (Week 3)"):
        st.code("""
from sklearn.neighbors import KNeighborsClassifier
import cv2, numpy as np, joblib

def preprocess_font(path, size=(32,32)):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return (cv2.resize(img, size) / 255.0).flatten()

X = np.array([preprocess_font(p) for p in font_paths])
y = np.array(font_labels)

knn = KNeighborsClassifier(n_neighbors=5, metric='cosine', weights='distance')
knn.fit(X_train, y_train)
print(classification_report(y_test, knn.predict(X_test)))
joblib.dump(knn, 'models/font_knn.pkl')
""", language="python")

    if st.session_state.get("selected_font") is not None:
        if st.button("Continue to Taglines →", key="font_next"):
            mark_done("W3")
            st.success("Typography selected! Move to the **Slogan / Taglines** tab.")
    else:
        st.warning("Select a font pairing to continue.")
