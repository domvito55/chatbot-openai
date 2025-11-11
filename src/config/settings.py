"""
Settings module: loads configuration from Streamlit secrets (Cloud) or env vars (local).
"""

import os


def get_openai_api_key() -> str:
    # Streamlit Cloud first
    try:
        import streamlit as st

        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

    # Fallback to environment variable
    key = os.getenv("OPENAI_API_KEY", "")
    return key
