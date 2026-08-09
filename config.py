import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def get_secret(key: str, default_value: str = "") -> str:
    """
    Retrieve a secret from Streamlit secrets (for production)
    or environment variables / .env file (for local development).
    """
    # 1. Try Streamlit Secrets first (Streamlit Cloud Production)
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # Ignore any Streamlit errors (e.g., missing secrets.toml, missing streamlit)
        pass
        
    # 2. Fallback to Environment Variables (Local Machine)
    return os.getenv(key, default_value)

GROQ_API_KEY = get_secret("GROQ_API_KEY", "")
VT_API_KEY   = get_secret("VT_API_KEY", "")
GROQ_MODEL   = get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")
YARA_RULES_PATH = os.path.join(BASE_DIR, "rules")
