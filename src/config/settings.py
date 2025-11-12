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

# Defaults (centralized). Can be overridden by Streamlit secrets or env vars.


def _cfg(name: str, default: str) -> str:
    """
    Return config from Streamlit secrets (if present) or environment variable,
    otherwise the provided default. Safe when no secrets.toml exists.
    """
    # 1) Try Streamlit secrets *for this key only*
    try:
        import streamlit as st  # lazy import; not required in tests/CLI

        try:
            val = st.secrets[name]  # raises if secrets file missing or key absent
            return str(val)
        except Exception:
            pass
    except Exception:
        pass

    # 2) Env var (e.g., set via .env + dotenv)
    return os.getenv(name, default)


# --------- DEFAULT VALUES -------------
DEFAULT_MODEL: str = _cfg("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")
DEFAULT_TEMPERATURE: float = float(_cfg("OPENAI_TEMPERATURE", "0.2"))
DEFAULT_TIMEOUT_SECONDS: int = int(_cfg("OPENAI_TIMEOUT_SECONDS", "30"))
DEFAULT_MAX_RETRIES: int = int(_cfg("OPENAI_MAX_RETRIES", "2"))
DEFAULT_MAX_HISTORY: int = int(_cfg("CHAT_MAX_HISTORY", "12"))


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
