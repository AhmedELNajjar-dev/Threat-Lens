import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Safely attempt to read from Streamlit secrets first, fallback to os.environ
try:
    import streamlit as st
    _get_secret = lambda k, d: st.secrets.get(k, os.getenv(k, d))
except ImportError:
    _get_secret = lambda k, d: os.getenv(k, d)

GROQ_API_KEY = _get_secret("GROQ_API_KEY", "")
VT_API_KEY   = _get_secret("VT_API_KEY", "")
GROQ_MODEL   = _get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")
YARA_RULES_PATH = os.path.join(BASE_DIR, "rules")
