# app.py
"""
Streamlit Chatbot (Base)
- Maintains chat history in st.session_state
- Renders chat bubbles
- Calls OpenAI via src.services.openai_client.send_chat()
"""

import streamlit as st

from src.config.settings import get_openai_api_key
from src.services.openai_client import send_chat

# ---------- Page setup ----------
st.set_page_config(
    page_title="Customer Support Chatbot", page_icon="💬", layout="centered"
)

# Load custom CSS (optional, safe if file exists)
try:
    with open("styles/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass


# ---------- Session state ----------
if "messages" not in st.session_state:
    # list of dicts: {"role": "user"|"assistant", "content": "text"}
    st.session_state["messages"]: list[dict[str, str]] = []

# A default system prompt (move this to the sidebar)
DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, concise AI assistant for customer support. "
    "Use clear, friendly language and keep responses brief unless asked otherwise."
)


# ---------- Header ----------
st.title("💬 Customer Support Chatbot")
st.caption("Etapa B — base chat loop with session_state")

# ---------- API key guard ----------
api_key = get_openai_api_key()
if not api_key:
    st.warning(
        "OpenAI API key is missing. Set the `OPENAI_API_KEY` environment"
        " variable locally, or add it under"
        " Streamlit Cloud → App → Settings → Secrets as `OPENAI_API_KEY`."
    )


# ---------- Render history ----------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------- Input + response ----------
user_input = st.chat_input("Type your message...")
if user_input and api_key:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Show user bubble immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = send_chat(
                    messages=st.session_state["messages"],
                    system_prompt=DEFAULT_SYSTEM_PROMPT,
                )
            except Exception as e:
                reply = (
                    "Sorry, I couldn't process your request right now. "
                    "Please try again in a few seconds."
                )
                # Log error (print to server logs)
                print(f"[openai error] {e!r}")

            st.markdown(reply)

    # Append assistant message
    st.session_state["messages"].append({"role": "assistant", "content": reply})
