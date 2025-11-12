# app.py
"""
Streamlit Chatbot — Step E (Error handling & stability)

This app:
- Keeps a minimal chat loop with st.session_state["messages"]
- Stores an editable system prompt in st.session_state["system_prompt"]
- Provides a "Clear chat" button in the sidebar
- Uses a high-contrast Streamlit theme (no custom CSS)
- Disables chat input when the API key is missing
- Adds resilience: history clamp, transient-error retries with backoff,
  and friendly UI messages for rate limits, timeouts, and auth errors
"""


import streamlit as st

from src.config.settings import DEFAULT_MODEL, get_openai_api_key
from src.services.openai_client import send_chat

# ---------- Page setup ----------
st.set_page_config(
    page_title="Customer Support Chatbot", page_icon="💬", layout="centered"
)

# ---------- Session state ----------
if "messages" not in st.session_state:
    # list of dicts: {"role": "user"|"assistant", "content": "text"}
    st.session_state["messages"]: list[dict[str, str]] = []

# A default system prompt
DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, concise AI assistant for customer support. "
    "Use clear, friendly language and keep responses brief unless asked otherwise."
)

# Keep the system prompt in session (so edits persist between reruns)
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = DEFAULT_SYSTEM_PROMPT

# ---------- Header ----------
st.title("💬 Customer Support Chatbot")
st.caption(
    "Step E — error handling (retries, timeouts, rate-limit) + safe history clamp"
)
st.caption(f"Model: `{DEFAULT_MODEL}`")


# ---------- API key guard ----------
api_key = get_openai_api_key()
if not api_key:
    st.warning(
        "OpenAI API key is missing. Set the `OPENAI_API_KEY` environment"
        " variable locally, or add it under"
        " Streamlit Cloud → App → Settings → Secrets as `OPENAI_API_KEY`."
    )

# ---------- Sidebar controls (Step C) ----------
with st.sidebar:
    st.subheader("Settings")

    edited_prompt = st.text_area(
        "System prompt",
        value=st.session_state["system_prompt"],
        help="High-level instructions for the assistant.",
        height=140,
    )

    clear_clicked = st.button(
        "Clear chat",
        type="secondary",
        help="Reset the current conversation.",
    )

# Persist prompt if user edited it
if edited_prompt != st.session_state["system_prompt"]:
    st.session_state["system_prompt"] = edited_prompt

# Clear chat when requested
if clear_clicked:
    st.session_state["messages"].clear()
    st.toast("Chat cleared.")

# ---------- Render history ----------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Input + response ----------
user_input = st.chat_input("Type your message...", disabled=not api_key)

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
                    system_prompt=st.session_state["system_prompt"],
                )

            except Exception as e:
                err = str(e).lower()
                if "rate limit" in err or "too many requests" in err:
                    reply = "We hit a rate limit. Please wait a bit and try again."
                    st.info(
                        "Tip: slow down slightly or switch to a cheaper/smaller"
                        " model for heavy testing."
                    )
                elif "timeout" in err:
                    reply = "The request timed out. Please try again."
                elif "authentication" in err or "invalid api key" in err:
                    reply = "Authentication failed. Check your API key settings."
                else:
                    reply = (
                        "Sorry, I couldn't process your request right now."
                        " Please try again soon."
                    )
                print(f"[openai error] {e!r}")

            st.markdown(reply)

    # Append assistant message
    st.session_state["messages"].append({"role": "assistant", "content": reply})
