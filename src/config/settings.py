# src/config/settings.py
"""
Settings module: loads configuration from Streamlit secrets (Cloud) or env vars (local).
If a .env file is present in local development, it will be loaded automatically.
"""

import os

# Load .env for local development; harmless if the file is absent.
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass


def get_openai_api_key() -> str:
    """Return the OpenAI API key from st.secrets (Cloud) or environment (.env/local)."""
    # Streamlit Cloud (and local .streamlit/secrets.toml when running via Streamlit)
    try:
        import streamlit as st  # imported only when Streamlit is available

        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        # Streamlit not available or no secrets; fall back to environment
        pass

    # Local/CI: environment variable (possibly loaded from .env)
    return os.getenv("OPENAI_API_KEY", "")
