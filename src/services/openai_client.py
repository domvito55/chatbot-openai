# src/services/openai_client.py
"""
OpenAI service wrapper.

- send_chat(messages, system_prompt, model): returns assistant text content.
- Keeps API access isolated from the UI.
"""
from openai import OpenAI

from src.config.settings import (
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_TIMEOUT_SECONDS,
    get_openai_api_key,
)


def send_chat(
    messages: list[dict[str, str]],
    system_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> str:
    """
    Build and send a chat completion request to OpenAI, returning assistant text.

    messages: list of {"role": "user"|"assistant", "content": str}
    system_prompt: system instruction string
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    # Build the full message sequence
    full_messages = [{"role": "system", "content": system_prompt}] + messages

    resp = client.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        timeout=timeout,  # type: ignore[arg-type]  # SDK may ignore this; safe to keep
    )

    return resp.choices[0].message.content or ""
