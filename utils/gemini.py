"""utils/gemini.py — Gemini API wrapper with bulletproof fallbacks"""
import os, json
import streamlit as st

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

MODELS_TO_TRY = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-pro",
]


def get_api_key() -> str:
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


def call_gemini(prompt: str, system: str = "",
                temperature: float = 0.7, max_tokens: int = 1000) -> str:
    """Call Gemini API. Always returns a string — never raises."""
    api_key = get_api_key()
    if not api_key or not GEMINI_AVAILABLE:
        return _fallback(prompt)

    try:
        genai.configure(api_key=api_key)
    except Exception:
        return _fallback(prompt)

    full_prompt = f"{system}\n\n{prompt}" if system else prompt

    for model_name in MODELS_TO_TRY:
        try:
            cfg = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config=cfg,
                    system_instruction=system if system else None,
                )
                response = model.generate_content(prompt)
            except TypeError:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config=cfg,
                )
                response = model.generate_content(full_prompt)

            if response and response.text:
                return response.text
        except Exception:
            continue

    return _fallback(prompt)


def call_gemini_json(prompt: str, system: str = ""):
    """Call Gemini and parse JSON. Always returns dict/list or None — never raises."""
    raw = call_gemini(prompt, system)
    if not raw:
        return None
    try:
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[-1]
        if clean.endswith("```"):
            clean = clean.rsplit("```", 1)[0]
        clean = clean.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception:
        return None


def call_gemini_chat(history: list, system: str = "") -> str:
    """Multi-turn chat. Always returns a string — never raises."""
    if not history:
        return "How can I help?"
    api_key = get_api_key()
    if not api_key or not GEMINI_AVAILABLE:
        return "Add GEMINI_API_KEY to Streamlit secrets to enable the AI assistant."
    try:
        genai.configure(api_key=api_key)
    except Exception:
        return "Could not configure Gemini API."

    for model_name in MODELS_TO_TRY:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system if system else None,
            )
            gemini_history = []
            for msg in history[:-1]:
                role = "model" if msg["role"] == "assistant" else "user"
                gemini_history.append({"role": role, "parts": [msg["content"]]})
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(history[-1]["content"])
            if response and response.text:
                return response.text
        except Exception:
            continue
    return "Could not reach Gemini API. Please check your API key in Streamlit secrets."


def _fallback(prompt: str) -> str:
    """Hard-coded fallback content when API is unavailable."""
    p = prompt.lower()
    if "slogan" in p or "tagline" in p:
        return json.dumps({"slogans": [
            {"text": "Built for what's next.",             "vibe": "Forward-looking"},
            {"text": "Simply brilliant.",                  "vibe": "Minimalist"},
            {"text": "Where excellence meets innovation.", "vibe": "Premium"},
            {"text": "The future, delivered today.",       "vibe": "Bold"},
        ]})
    if "font" in p or "typography" in p:
        return json.dumps({"fonts": [
            {"heading": "Playfair Display",   "body": "Source Sans Pro", "vibe": "Luxury",    "rationale": "Elegant & authoritative"},
            {"heading": "Montserrat",         "body": "Open Sans",       "vibe": "Modern",    "rationale": "Clean and versatile"},
            {"heading": "Cormorant Garamond", "body": "Lato",            "vibe": "Editorial", "rationale": "Refined and literary"},
            {"heading": "DM Sans",            "body": "Inter",           "vibe": "Minimal",   "rationale": "Contemporary and legible"},
        ]})
    if "colour" in p or "palette" in p or "color" in p:
        return json.dumps({"palettes": [
            {"name": "Signature", "colors": ["#1a1a18","#c9a84c","#f2ede4","#5a5a56"], "mood": "Premium & timeless"},
            {"name": "Vibrant",   "colors": ["#1e2a4a","#f97316","#eef2ff","#94a3b8"], "mood": "Energetic & bold"},
            {"name": "Natural",   "colors": ["#2d4a3e","#a8d5c2","#f0f7f4","#8fbc8f"], "mood": "Fresh & organic"},
        ]})
    if "campaign" in p:
        return json.dumps({"campaign": {
            "type": "Carousel post", "bestTime": "Tue–Thu 6–9 PM",
            "hashtags": ["#BrandMind","#Marketing","#Launch","#Brand"],
            "caption": "Redefining excellence — one brand at a time. ✨",
            "tip": "Lead with your strongest visual in frame 1.",
            "postDays": ["Tue","Wed","Thu"], "targetAge": "25–34",
        }})
    if "translat" in p:
        return json.dumps({"translations": [
            {"lang": "Spanish", "flag": "🇪🇸", "slogan": "Construido para lo que viene.",  "caption": "Redefiniendo la excelencia."},
            {"lang": "French",  "flag": "🇫🇷", "slogan": "Conçu pour demain.",             "caption": "Redéfinir l'excellence."},
            {"lang": "German",  "flag": "🇩🇪", "slogan": "Gebaut für das Nächste.",        "caption": "Exzellenz neu definiert."},
            {"lang": "Japanese","flag": "🇯🇵", "slogan": "未来のために。",                  "caption": "卓越性を再定義する。"},
            {"lang": "Arabic",  "flag": "🇸🇦", "slogan": "مبني لما هو قادم.",              "caption": "إعادة تعريف التميز."},
        ]})
    return "I'm your BrandMind AI assistant. How can I help with your brand today?"
