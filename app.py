"""
NovaTech AI — AI-Powered Branding Platform
CRS AI Capstone 2025-26 | Scenario 1
"""
import streamlit as st
import base64, os

st.set_page_config(
    page_title="NovaTech AI",
    page_icon="\u2726",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from utils.session import init_session
from utils.gemini  import call_gemini_json, call_gemini
init_session()

def _load_logo():
    p = os.path.join(os.path.dirname(__file__), "assets", "novatech-logo.svg")
    if not os.path.exists(p):
        return "", ""
    with open(p) as f:
        raw = f.read()
    white = (raw
        .replace('fill="#1A1A1A"', 'fill="#C8C4BB"')
        .replace("fill='#1A1A1A'", "fill='#C8C4BB'")
        .replace('fill="#F9F9F7"/>', 'fill="none"/>')
        .replace('rect width="400" height="400" fill="#F9F9F7"',
                 'rect width="400" height="400" fill="none"'))
    b64 = base64.b64encode(white.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}", b64

LOGO_URI, LOGO_B64 = _load_logo()

def _img(size, style=""):
    if not LOGO_URI:
        return ""
    return f'<img src="{LOGO_URI}" width="{size}" height="{size}" style="display:block;flex-shrink:0;{style}">'

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;1,300;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');
:root{--bg:#080806;--s1:#0d0d0b;--s2:#111110;--line:#1f1f1d;--l2:#2a2a27;--tx:#C8C4BB;--mute:#565650;--dim:#282825;--gold:#BFA04A;--serif:'Playfair Display',Georgia,serif;--sans:'DM Sans',system-ui,sans-serif;--mono:'DM Mono','Courier New',monospace}
#MainMenu,footer,header,[data-testid="stHeader"],[data-testid="stDecoration"],[data-testid="stToolbar"],[data-testid="stSidebar"],[data-testid="stStatusWidget"]{display:none !important}
html,body,[data-testid="stApp"],[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],[data-testid="stMain"],[data-testid="stMainBlockContainer"],.main,section.main,[data-testid="block-container"],.block-container{background:var(--bg) !important;color:var(--tx) !important;font-family:var(--sans) !important;padding:0 !important;max-width:100% !important;width:100% !important}
[data-testid="stVerticalBlock"]>[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stVerticalBlock"]>div{gap:0 !important}
[data-testid="stVerticalBlockBorderWrapper"]{padding:0 !important}
div[data-testid="stMarkdownContainer"]>p{margin:0 !important}
[data-testid="stButton"]>button{background:transparent !important;color:var(--mute) !important;border:1px solid var(--l2) !important;border-radius:1px !important;font-family:var(--mono) !important;font-size:0.58rem !important;letter-spacing:0.08em !important;text-transform:uppercase !important;padding:0.5rem 0.9rem !important;transition:all 0.4s ease !important}
[data-testid="stButton"]>button:hover{border-color:var(--tx) !important;color:var(--tx) !important}
[data-testid="stButton"]>button[kind="primary"]{background:var(--tx) !important;color:var(--bg) !important;border-color:var(--tx) !important;font-weight:500 !important}
[data-testid="stButton"]>button[kind="primary"]:hover{background:var(--gold) !important;border-color:var(--gold) !important}
[data-testid="stDownloadButton"]>button{background:transparent !important;color:var(--gold) !important;border:1px solid rgba(191,160,74,0.35) !important;border-radius:1px !important;font-family:var(--mono) !important;font-size:0.58rem !important;letter-spacing:0.08em !important;text-transform:uppercase !important}
[data-testid="stDownloadButton"]>button:hover{background:rgba(191,160,74,0.07) !important;border-color:var(--gold) !important}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{background:var(--s1) !important;border:1px solid var(--l2) !important;border-radius:1px !important;color:var(--tx) !important;font-family:var(--sans) !important;font-size:0.88rem !important;font-weight:300 !important}
[data-testid="stTextInput"] input:focus,[data-testid="stTextArea"] textarea:focus{border-color:var(--mute) !important;box-shadow:none !important}
[data-testid="stTextInput"] label,[data-testid="stTextArea"] label,[data-testid="stSelectbox"] label,[data-testid="stSlider"] label,[data-testid="stMultiSelect"] label{color:var(--mute) !important;font-family:var(--mono) !important;font-size:0.52rem !important;letter-spacing:0.12em !important;text-transform:uppercase !important}
[data-testid="stSelectbox"]>div>div{background:var(--s1) !important;border:1px solid var(--l2) !important;border-radius:1px !important;color:var(--tx) !important}
[data-testid="stMultiSelect"]>div>div{background:var(--s1) !important;border:1px solid var(--l2) !important;border-radius:1px !important}
[data-testid="stMultiSelect"] span[data-baseweb="tag"]{background:var(--s2) !important;color:var(--gold) !important;border:1px solid var(--l2) !important;font-family:var(--mono) !important;font-size:0.58rem !important;border-radius:1px !important}
[data-testid="stSlider"]>div>div>div{background:var(--l2) !important}
[data-testid="stSlider"]>div>div>div>div{background:var(--gold) !important}
[data-testid="stMetric"]{background:var(--s1) !important;border:1px solid var(--line) !important;border-radius:1px !important;padding:1.4rem 1.6rem !important}
[data-testid="stMetricLabel"]{color:var(--mute) !important;font-family:var(--mono) !important;font-size:0.52rem !important;letter-spacing:0.12em !important;text-transform:uppercase !important}
[data-testid="stMetricValue"]{color:var(--tx) !important;font-family:var(--serif) !important;font-size:2rem !important;font-weight:300 !important}
[data-testid="stMetricDelta"]{color:var(--mute) !important;font-size:0.62rem !important}
[data-testid="stDataFrame"]{border:1px solid var(--line) !important;border-radius:1px !important}
[data-testid="stAlert"]{background:var(--s1) !important;border-left:2px solid var(--l2) !important;color:var(--mute) !important;font-size:0.82rem !important;border-radius:0 !important}
[data-testid="stSuccess"]{border-left-color:#4a7c5a !important;color:var(--tx) !important}
[data-testid="stWarning"]{border-left-color:var(--gold) !important}
[data-testid="stInfo"]{border-left-color:var(--mute) !important}
pre,[data-testid="stCode"]{background:#050503 !important;border:1px solid var(--line) !important;border-radius:1px !important;font-family:var(--mono) !important}
code{color:var(--gold) !important}
[data-testid="stExpander"]{background:transparent !important;border:1px solid var(--line) !important;border-radius:0 !important}
[data-testid="stExpander"] summary{font-family:var(--mono) !important;font-size:0.56rem !important;letter-spacing:0.1em !important;text-transform:uppercase !important;color:var(--mute) !important}
hr{border:none !important;border-top:1px solid var(--line) !important;margin:0 !important}
h1,h2,h3,h4{font-family:var(--serif) !important;font-weight:300 !important;color:var(--tx) !important}
p{color:var(--tx) !important;font-weight:300 !important;line-height:1.75 !important}
[data-testid="stForm"]{background:var(--s1) !important;border:1px solid var(--line) !important;border-radius:1px !important;padding:1.8rem !important}
[data-testid="stFormSubmitButton"]>button{background:var(--tx) !important;color:var(--bg) !important;border:none !important;font-family:var(--mono) !important;font-size:0.58rem !important;letter-spacing:0.1em !important;text-transform:uppercase !important;padding:0.7rem 2rem !important;border-radius:1px !important;width:100% !important}
[data-testid="stChatMessage"]{background:var(--s1) !important;border:1px solid var(--line) !important;border-radius:1px !important}
[data-testid="stChatInput"] textarea{background:var(--s1) !important;border:1px solid var(--l2) !important;color:var(--tx) !important;border-radius:1px !important}
[data-testid="stImage"] img{border-radius:1px !important}
[data-testid="stPyplot"]{background:transparent !important}
[data-testid="stPyplot"]>div{background:transparent !important}
[data-testid="stHorizontalBlock"]{gap:1.5rem !important}
@keyframes nt-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
@keyframes nt-pulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.07);opacity:0.6}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# NAV
company_name = st.session_state.get("company") or "NovaTech"
st.markdown(f"""
<style>
.nt-nav{{position:fixed !important;top:0 !important;left:0 !important;right:0 !important;z-index:99999 !important;height:56px !important;background:rgba(8,8,6,0.96) !important;backdrop-filter:blur(24px) !important;-webkit-backdrop-filter:blur(24px) !important;border-bottom:1px solid #1f1f1d !important;display:flex !important;align-items:center !important;justify-content:space-between !important;padding:0 52px !important;box-sizing:border-box !important}}
.nt-nav a{{text-decoration:none !important}}
.nt-logo{{display:flex;align-items:center;gap:11px}}
.nt-links{{display:flex;align-items:center;gap:26px}}
.nt-lnk{{font-family:'DM Mono',monospace !important;font-size:0.52rem !important;letter-spacing:0.12em !important;color:#565650 !important;text-transform:uppercase !important;transition:color 0.3s !important}}
.nt-lnk:hover{{color:#C8C4BB !important}}
.nt-cta{{font-family:'DM Mono',monospace !important;font-size:0.52rem !important;letter-spacing:0.12em !important;color:#C8C4BB !important;text-transform:uppercase !important;border:1px solid #2a2a27 !important;padding:0.32rem 0.9rem !important;border-radius:1px !important}}
.nt-sp{{height:56px}}
</style>
<div class="nt-nav">
  <a href="#" class="nt-logo">
    {_img(26)}
    <span style="font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.22em;color:#C8C4BB;text-transform:uppercase">{company_name}</span>
  </a>
  <div class="nt-links">
    <a href="#configure" class="nt-lnk">Configure</a>
    <a href="#logo"      class="nt-lnk">Logo &amp; Font</a>
    <a href="#slogans"   class="nt-lnk">Slogans</a>
    <a href="#colour"    class="nt-lnk">Colour</a>
    <a href="#campaign"  class="nt-lnk">Campaign</a>
    <a href="#kit"       class="nt-cta">Brand Kit &#8595;</a>
  </div>
</div>
<div class="nt-sp"></div>
""", unsafe_allow_html=True)

# HERO
st.markdown(f"""
<div style="position:relative;background:#080806;display:grid;grid-template-columns:1fr 1fr;min-height:92vh;border-bottom:1px solid #1f1f1d;overflow:hidden">
  <div style="position:absolute;bottom:-200px;left:-150px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(80,100,148,0.06) 0%,transparent 65%);pointer-events:none"></div>
  <div style="display:flex;flex-direction:column;justify-content:flex-end;padding:0 52px 88px 72px;position:relative;z-index:2">
    <div style="font-family:'DM Mono',monospace;font-size:0.5rem;letter-spacing:0.22em;color:#282825;text-transform:uppercase;margin-bottom:30px">&#10022; &nbsp; CRS AI Capstone 2025&#8211;26 &middot; Scenario 1</div>
    <div style="font-family:'Playfair Display',Georgia,serif;font-size:88px;font-weight:300;color:#C8C4BB;line-height:0.88;letter-spacing:-0.04em;margin-bottom:44px">Build your<br>brand with<br><em style="color:#BFA04A;font-style:italic">intelligence.</em></div>
    <div style="font-size:0.92rem;font-weight:300;color:#C8C4BB;opacity:0.62;max-width:360px;line-height:1.85;margin-bottom:44px;font-family:'DM Sans',sans-serif">CNN &middot; KNN &middot; KMeans &middot; Random Forest &middot; Gemini API.<br>From identity to launch, in one platform.</div>
    <div style="display:flex;gap:44px;margin-bottom:40px">
      <div><div style="font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:300;color:#C8C4BB;line-height:1">9+</div><div style="font-family:'DM Mono',monospace;font-size:0.42rem;letter-spacing:0.14em;color:#282825;text-transform:uppercase;margin-top:4px">AI Models</div></div>
      <div><div style="font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:300;color:#C8C4BB;line-height:1">5</div><div style="font-family:'DM Mono',monospace;font-size:0.42rem;letter-spacing:0.14em;color:#282825;text-transform:uppercase;margin-top:4px">Datasets</div></div>
      <div><div style="font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:300;color:#C8C4BB;line-height:1">10+</div><div style="font-family:'DM Mono',monospace;font-size:0.42rem;letter-spacing:0.14em;color:#282825;text-transform:uppercase;margin-top:4px">Languages</div></div>
    </div>
    <div style="display:flex;align-items:center;gap:12px"><div style="width:40px;height:1px;background:#282825"></div><span style="font-family:'DM Mono',monospace;font-size:0.44rem;letter-spacing:0.16em;color:#282825;text-transform:uppercase">Scroll to explore</span></div>
  </div>
  <div style="display:flex;align-items:center;justify-content:center;border-left:1px solid #1f1f1d;position:relative;z-index:2">
    <div style="position:absolute;width:560px;height:560px;border-radius:50%;background:radial-gradient(circle,rgba(191,160,74,0.14) 0%,rgba(191,160,74,0.04) 42%,transparent 68%);animation:nt-pulse 5s ease-in-out infinite;pointer-events:none"></div>
    {_img(400,"animation:nt-float 7s ease-in-out infinite;filter:brightness(1.1);opacity:0.92")}
  </div>
</div>
""", unsafe_allow_html=True)

# STRIP
st.markdown("""
<div style="background:#0d0d0b;border-bottom:1px solid #1f1f1d">
  <div style="display:grid;grid-template-columns:repeat(5,1fr)">
    <div style="padding:26px 24px;border-right:1px solid #1f1f1d"><div style="font-family:'DM Mono',monospace;font-size:0.42rem;letter-spacing:0.12em;color:#282825;text-transform:uppercase;margin-bottom:6px">Week 02&#8211;03</div><div style="font-family:'Playfair Display',serif;font-size:0.9rem;font-weight:300;color:#C8C4BB;margin-bottom:3px">Logo &amp; Typography</div><div style="font-size:0.68rem;color:#282825;font-weight:300">CNN &middot; KNN font engine</div></div>
    <div style="padding:26px 24px;border-right:1px solid #1f1f1d"><div style="font-family:'DM Mono',monospace;font-size:0.42rem;letter-spacing:0.12em;color:#282825;text-transform:uppercase;margin-bottom:6px">Week 04</div><div style="font-family:'Playfair Display',serif;font-size:0.9rem;font-weight:300;color:#C8C4BB;margin-bottom:3px">Slogans &amp; Copy</div><div style="font-size:0.68rem;color:#282825;font-weight:300">Gemini API &middot; NLTK</div></div>
    <div style="padding:26px 24px;border-right:1px solid #1f1f1d"><div style="font-family:'DM Mono',monospace;font-size:0.42rem;letter-spacing:0.12em;color:#282825;text-transform:uppercase;margin-bottom:6px">Week 05&#8211;06</div><div style="font-family:'Playfair Display',serif;font-size:0.9rem;font-weight:300;color:#C8C4BB;margin-bottom:3px">Colour &amp; Animation</div><div style="font-size:0.68rem;color:#282825;font-weight:300">KMeans &middot; GIF export</div></div>
    <div style="padding:26px 24px;border-right:1px solid #1f1f1d"><div style="font-family:'DM Mono',monospace;font-size:0.42rem;letter-spacing:0.12em;color:#282825;text-transform:uppercase;margin-bottom:6px">Week 07&#8211;08</div><div style="font-family:'Playfair Display',serif;font-size:0.9rem;font-weight:300;color:#C8C4BB;margin-bottom:3px">Campaign &amp; Global</div><div style="font-size:0.68rem;color:#282825;font-weight:300">Random Forest &middot; 10+ langs</div></div>
    <div style="padding:26px 24px"><div style="font-family:'DM Mono',monospace;font-size:0.42rem;letter-spacing:0.12em;color:#282825;text-transform:uppercase;margin-bottom:6px">Week 10</div><div style="font-family:'Playfair Display',serif;font-size:0.9rem;font-weight:300;color:#C8C4BB;margin-bottom:3px">Brand Kit</div><div style="font-size:0.68rem;color:#282825;font-weight:300">ZIP &middot; Cloud deploy</div></div>
  </div>
</div>
""", unsafe_allow_html=True)


# HELPERS
def sec(anchor, step, headline, sub="", bg="#080806"):
    la = _img(30, "opacity:0.14;margin-bottom:16px") if LOGO_URI else ""
    st.markdown(f"""
<div id="{anchor}" style="background:{bg};border-top:1px solid #1f1f1d;padding:80px 72px 56px">
  {la}
  <div style="font-family:'DM Mono',monospace;font-size:0.48rem;letter-spacing:0.18em;color:#282825;text-transform:uppercase;margin-bottom:14px">{step}</div>
  <div style="font-family:'Playfair Display',Georgia,serif;font-size:52px;font-weight:300;color:#C8C4BB;letter-spacing:-0.02em;line-height:1.0;margin-bottom:16px">{headline}</div>
  {'<div style="font-size:0.9rem;color:#C8C4BB;opacity:0.6;font-weight:300;max-width:520px;line-height:1.82;margin-bottom:44px;font-family:DM Sans,sans-serif">'+sub+'</div>' if sub else '<div style="height:36px"></div>'}
""", unsafe_allow_html=True)

def sec_end():
    st.markdown("</div>", unsafe_allow_html=True)

def fl(text):
    st.markdown(
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.52rem;' +
        f'letter-spacing:0.12em;text-transform:uppercase;color:#565650;' +
        f'margin-bottom:3px;margin-top:18px">{text}</div>',
        unsafe_allow_html=True)


# SECTION 1 — CONFIGURE
sec("configure","Step 01 &middot; Foundation","Configure your brand.",
    "Set your company, industry, tone, and audience. Every AI output is personalised to these inputs.")

INDUSTRIES = ["Technology","Finance","Healthcare","Retail","Education",
              "Food & Beverage","Real Estate","Fashion","Travel","Sustainability"]
TONES = ["Minimalist","Bold","Luxury","Playful","Professional","Innovative","Trustworthy","Creative"]

col1, col2 = st.columns([1,1], gap="large")
with col1:
    fl("Company Name")
    company = st.text_input("co", value=st.session_state.get("company","NovaTech"),
                             placeholder="e.g. NovaTech", label_visibility="collapsed")
    st.session_state.company = company
    fl("Target Audience")
    audience = st.text_input("aud", value=st.session_state.get("audience",""),
                              placeholder="e.g. B2B founders 28-45", label_visibility="collapsed")
    st.session_state.audience = audience
    fl("Target Region")
    region = st.text_input("reg", value=st.session_state.get("region",""),
                            placeholder="e.g. India, Europe, Global", label_visibility="collapsed")
    st.session_state.region = region
with col2:
    fl("Product / Service Description")
    desc = st.text_area("dsc", value=st.session_state.get("description",""),
                         placeholder="Describe what your brand offers...",
                         height=172, label_visibility="collapsed")
    st.session_state.description = desc

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
fl("Industry")
ind_cols = st.columns(5, gap="small")
for i, ind in enumerate(INDUSTRIES):
    with ind_cols[i % 5]:
        active = st.session_state.get("industry") == ind
        if st.button(ind, key=f"ind_{ind}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.industry = ind; st.rerun()

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
fl("Brand Tone")
tone_cols = st.columns(4, gap="small")
for i, tone in enumerate(TONES):
    with tone_cols[i % 4]:
        active = st.session_state.get("tone") == tone
        if st.button(tone, key=f"tn_{tone}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.tone = tone; st.rerun()

if st.session_state.get("company") and st.session_state.get("industry") and st.session_state.get("tone"):
    co = st.session_state.company
    ind_ = st.session_state.get("industry","")
    tn_  = st.session_state.get("tone","")
    rg_  = st.session_state.get("region","Global")
    st.markdown(f"""
<div style="margin-top:32px;padding:18px 22px;background:#0d0d0b;border:1px solid #1f1f1d;display:flex;align-items:center;gap:12px">
  <div style="width:5px;height:5px;background:#C8C4BB;border-radius:50%;flex-shrink:0"></div>
  <div style="font-family:'Playfair Display',serif;font-size:0.95rem;font-weight:300;color:#C8C4BB">
    {co} is configured.
    <span style="font-family:'DM Mono',monospace;font-size:0.48rem;color:#282825;letter-spacing:0.1em;margin-left:12px">{ind_} &middot; {tn_} &middot; {rg_}</span>
  </div>
  <div style="margin-left:auto;font-family:'DM Mono',monospace;font-size:0.46rem;color:#282825;letter-spacing:0.1em">Scroll &#8595;</div>
</div>""", unsafe_allow_html=True)
sec_end()

# SECTION 2 — LOGO & FONT
sec("logo","Step 02&#8211;03 &middot; Identity","Logo &amp; typography.",
    "CNN classification with PCA clusters. KNN font engine trained on 2,400 samples.",bg="#0d0d0b")
from modules.week2_logo import render_logo
from modules.week3_font import render_font
render_logo()
st.markdown("<div style='height:52px'></div>", unsafe_allow_html=True)
render_font()
sec_end()

# SECTION 3 — SLOGANS
sec("slogans","Step 04 &middot; Voice","Slogans &amp; taglines.",
    "Gemini API generation with NLTK preprocessing. Sentiment-scored. Export TXT + JSON.")
from modules.week4_slogan import render_slogan
render_slogan()
sec_end()

# SECTION 4 — COLOUR
sec("colour","Step 05 &middot; Palette","Colour palette engine.",
    "KMeans pixel extraction mapped to industry colour psychology.",bg="#0d0d0b")
from modules.week5_colour import render_colour
render_colour()
sec_end()

# SECTION 5 — ANIMATION
sec("animation","Step 06 &middot; Motion","Animation studio.",
    "Matplotlib FuncAnimation storyboards. One-click GIF export for social media.")
from modules.week6_animation import render_animation
render_animation()
sec_end()

# SECTION 6 — CAMPAIGN + MULTILINGUAL
sec("campaign","Step 07&#8211;08 &middot; Reach","Campaign &amp; global copy.",
    "Trained Random Forest + GBM predict CTR, ROI, engagement. Gemini API translates to 10+ languages.",bg="#0d0d0b")
from modules.week7_campaign  import render_campaign
from modules.week8_multilang import render_multilang
render_campaign()
st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)
render_multilang()
sec_end()

# SECTION 7 — FEEDBACK
sec("feedback","Step 09 &middot; Refinement","Feedback &amp; model tuning.",
    "VADER sentiment analysis on ratings. Radar chart visualisation. Model refinement feedback loop.")
from modules.week9_feedback import render_feedback
render_feedback()
sec_end()

# SECTION 8 — BRAND KIT
sec("kit","Step 10 &middot; Export","Your brand kit.",
    "Logo, palette, slogans, campaign copy — everything in one downloadable ZIP.",bg="#0d0d0b")
if LOGO_URI:
    co_kit = st.session_state.get("company","NovaTech")
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:24px;margin-bottom:44px">
  {_img(88,"opacity:0.9;animation:nt-float 7s ease-in-out infinite")}
  <div>
    <div style="font-family:'Playfair Display',serif;font-size:3rem;font-weight:300;color:#C8C4BB;line-height:1;letter-spacing:-0.03em;margin-bottom:6px">{co_kit} AI</div>
    <div style="font-family:'DM Mono',monospace;font-size:0.5rem;letter-spacing:0.22em;color:#282825;text-transform:uppercase">Brand Identity System</div>
  </div>
</div>
<div style="width:100%;height:1px;background:linear-gradient(90deg,#BFA04A,transparent);opacity:0.35;margin-bottom:40px"></div>
""", unsafe_allow_html=True)
from modules.week10_kit import render_kit
render_kit()
sec_end()

# AI CHAT
sec("chat","Optional &middot; AI Assistant","Ask NovaTech AI.",
    "Gemini-powered assistant with full brand context.")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role":"assistant",
        "content":"Hi — I'm the NovaTech AI assistant. Ask me anything about your brand, AI models, or strategy."}]
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if user_input := st.chat_input("Ask NovaTech AI..."):
    st.session_state.chat_history.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner(""):
            ctx = (f"Brand: {st.session_state.get('company','NovaTech')}, "
                   f"Industry: {st.session_state.get('industry','-')}, "
                   f"Tone: {st.session_state.get('tone','-')}.")
            reply = call_gemini(user_input,
                system=f"You are NovaTech AI, expert branding assistant. Context: {ctx} Be concise.",
                temperature=0.7, max_tokens=400)
            st.markdown(reply)
            st.session_state.chat_history.append({"role":"assistant","content":reply})
sec_end()

# FOOTER
st.markdown(f"""
<div style="background:#050503;border-top:1px solid #1f1f1d;padding:40px 72px;display:flex;align-items:center;justify-content:space-between">
  <div style="display:flex;align-items:center;gap:10px">{_img(20,"opacity:0.22")}<span style="font-family:'DM Mono',monospace;font-size:0.46rem;letter-spacing:0.2em;color:#282825;text-transform:uppercase">NovaTech AI</span></div>
  <span style="font-family:'DM Mono',monospace;font-size:0.44rem;letter-spacing:0.1em;color:#282825;text-transform:uppercase">CRS AI Capstone 2025&#8211;26 &middot; Scenario 1</span>
  <span style="font-family:'DM Mono',monospace;font-size:0.44rem;letter-spacing:0.1em;color:#282825">Streamlit &middot; Gemini API &middot; scikit-learn</span>
</div>
""", unsafe_allow_html=True)
