"""utils/styles.py — NovaTech AI · minimal helpers (CSS lives in app.py)"""
import streamlit as st

def inject_css():
    """No-op: CSS is injected directly in app.py for single-page layout."""
    pass

def week_header(week_num: int, title: str, tools: str = ""):
    """Compact sub-header for use within scroll sections."""
    st.markdown(f"""
<div style="padding:0 0 24px;margin-bottom:28px;border-bottom:1px solid #1A1A17">
  <div style="font-family:'DM Mono',monospace;font-size:0.56rem;color:#3A3A36;
    letter-spacing:0.14em;text-transform:uppercase;margin-bottom:8px">
    Week {week_num:02d}{(' · '+tools) if tools else ''}
  </div>
  <div style="font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:300;
    color:#F5F2EB;letter-spacing:-0.01em">{title}</div>
</div>""", unsafe_allow_html=True)

def label(text: str):
    st.markdown(f"""
<div style="font-family:'DM Mono',monospace;font-size:0.58rem;font-weight:400;
  color:#6A6A64;letter-spacing:0.12em;text-transform:uppercase;
  margin-bottom:4px;margin-top:18px">{text}</div>
""", unsafe_allow_html=True)
