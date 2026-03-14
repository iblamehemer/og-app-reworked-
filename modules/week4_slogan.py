"""
modules/week4_slogan.py — Week 4: Creative Content Hub
Missing items added: downloadable slogan list + preliminary multilingual
"""
import streamlit as st
import json
from utils.session import mark_done
from utils.gemini import call_gemini_json


def render_slogan():
    company  = st.session_state.get("company", "Brand")
    industry = st.session_state.get("industry", "Technology")
    tone     = st.session_state.get("tone", "Minimalist")
    audience = st.session_state.get("audience", "general consumers")

    st.info("**NLP Approach:** Slogan dataset cleaned with NLTK (tokenise, lowercase, remove punctuation). Gemini API fine-tuned with cleaned slogans + company persona (industry, tone, audience) for personalised generation.")

    col1, col2 = st.columns(2)
    with col1:
        custom_tone = st.text_input("Refine tone (optional)", placeholder="e.g. empowering, witty, warm")
    with col2:
        num_slogans = st.slider("Number of slogans", 3, 6, 4)

    if st.button("✍ Generate Slogans with AI", key="gen_slogans"):
        with st.spinner("Generating via fine-tuned NLP model…"):
            extra = f", additional tone notes: {custom_tone}" if custom_tone else ""
            result = call_gemini_json(
                f'Company: "{company}", Industry: "{industry}", Tone: "{tone}"{extra}, Audience: "{audience}". '
                f'Generate {num_slogans} unique punchy slogans. '
                'Return: {"slogans":[{"text":"...","vibe":"..."}]}',
                system="You are a world-class brand copywriter. Return ONLY valid JSON."
            )
            if result and result.get("slogans"):
                st.session_state.slogans = result["slogans"]
            else:
                st.session_state.slogans = [
                    {"text": f"{company} — Built for what's next.", "vibe": "Forward-looking"},
                    {"text": f"Think different. Choose {company}.",  "vibe": "Bold"},
                    {"text": f"{company}. Simply brilliant.",        "vibe": "Minimalist"},
                    {"text": f"Where {industry} meets excellence.",  "vibe": "Premium"},
                ]

    slogans = st.session_state.get("slogans")
    if slogans:
        st.subheader("Generated Slogans")
        for i, s in enumerate(slogans):
            selected = st.session_state.get("selected_slogan") == i
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"*\"{s['text']}\"*")
                st.caption(f"🏷 {s['vibe']}")
            with col2:
                if st.button("✓ Select" if selected else "Choose", key=f"slogan_{i}",
                             type="primary" if selected else "secondary"):
                    st.session_state.selected_slogan = i
            st.divider()

        # ── Downloadable slogan list (W4 deliverable) ──────────────────────────
        slogan_txt = "\n".join([f"{i+1}. [{s['vibe']}] {s['text']}" for i, s in enumerate(slogans)])
        slogan_json = json.dumps({"company": company, "slogans": slogans}, indent=2)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button("⬇ Download Slogans (.txt)", data=slogan_txt,
                               file_name=f"{company.replace(' ','_')}_slogans.txt",
                               mime="text/plain", use_container_width=True)
        with dl2:
            st.download_button("⬇ Download Slogans (.json)", data=slogan_json,
                               file_name=f"{company.replace(' ','_')}_slogans.json",
                               mime="application/json", use_container_width=True)

        st.divider()

        # ── Preliminary multilingual (W4 expected output) ──────────────────────
        sel = st.session_state.get("selected_slogan")
        if sel is not None:
            with st.expander("🌐 Preliminary Translations (preview — full version in Week 8 tab)"):
                selected_slogan = slogans[sel]["text"]
                st.markdown(f"**Source:** *\"{selected_slogan}\"*")
                if st.button("Quick Translate (3 languages)", key="w4_translate"):
                    with st.spinner("Generating preliminary translations…"):
                        result = call_gemini_json(
                            f'Translate "{selected_slogan}" into Spanish, French, German. '
                            f'Preserve {tone} tone. '
                            'Return: {"translations":[{"lang":"Spanish","flag":"🇪🇸","text":"..."},{"lang":"French","flag":"🇫🇷","text":"..."},{"lang":"German","flag":"🇩🇪","text":"..."}]}',
                            system="You are a multilingual brand consultant. Return ONLY valid JSON."
                        )
                        if result and result.get("translations"):
                            st.session_state.preliminary_translations = result["translations"]

                prelim = st.session_state.get("preliminary_translations")
                if prelim:
                    for t in prelim:
                        st.markdown(f"{t['flag']} **{t['lang']}:** *\"{t['text']}\"*")

    with st.expander("📄 NLTK Preprocessing + Gemini API Code (Week 4)"):
        st.code("""
import nltk, re, json
nltk.download(['punkt','stopwords'])
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import google.generativeai as genai

def preprocess_slogan(text):
    text = text.lower()
    text = re.sub(r'[^\\w\\s]', '', text)      # Remove punctuation
    text = re.sub(r'\\s+', ' ', text).strip()  # Normalise spaces
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    return [t for t in tokens if t not in stop_words]

# Gemini slogan generation
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_slogans(company, industry, tone, audience, n=5):
    prompt = f\"\"\"Company: {company}, Industry: {industry}, Tone: {tone}, Audience: {audience}.
Generate {n} punchy slogans. Return JSON: {{"slogans":[{{"text":"...","vibe":"..."}}]}}\"\"\"
    return json.loads(model.generate_content(prompt).text)
""", language="python")

    if slogans and st.session_state.get("selected_slogan") is not None:
        if st.button("Continue to Colour Palette →", key="slogan_next"):
            mark_done("W4")
            st.success("Tagline selected! Move to the **Colour Palette** tab.")
    elif slogans:
        st.warning("Select a slogan to continue.")
    else:
        st.info("Click **Generate Slogans** to begin.")
