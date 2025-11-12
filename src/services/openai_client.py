# src/services/openai_client.py
"""
OpenAI service wrapper.

- send_chat(messages, system_prompt, model): returns assistant text content.
- Keeps API access isolated from the UI.
"""
import time

from openai import OpenAI

# Try to import SDK exception classes; if unavailable, define local fallbacks.
try:
    from openai import (
        APIConnectionError,
        APITimeoutError,
        AuthenticationError,
        BadRequestError,
        RateLimitError,
    )
except Exception:  # compat fallback
    APIConnectionError = RateLimitError = BadRequestError = AuthenticationError = (
        APITimeoutError
    ) = Exception

from src.config.settings import (
    DEFAULT_MAX_HISTORY,
    DEFAULT_MAX_RETRIES,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_TIMEOUT_SECONDS,
    get_openai_api_key,
)


def _is_transient(e: Exception) -> bool:
    text = str(e).lower()
    return (
        isinstance(e, (APIConnectionError, RateLimitError, APITimeoutError))
        or "rate limit" in text
        or "too many requests" in text
        or "timeout" in text
        or "temporar" in text  # temporarily unavailable, etc.
    )


def send_chat(
    messages: list[dict[str, str]],
    system_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    max_retries: int = DEFAULT_MAX_RETRIES,
    max_history: int = DEFAULT_MAX_HISTORY,
) -> str:
    """
    Build and send a chat completion request to OpenAI, returning assistant text.

    messages: list of {"role": "user"|"assistant", "content": str}
    system_prompt: system instruction string
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")

    # Keep only the last N messages to avoid context bloat
    history = messages[-max_history:] if max_history and max_history > 0 else messages
    payload = [{"role": "system", "content": system_prompt}] + history

    client = OpenAI(api_key=api_key)

    attempt = 0
    backoff = 1.0

    while attempt <= max_retries:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=payload,
                temperature=temperature,
                timeout=timeout,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            if attempt < max_retries and _is_transient(e):
                time.sleep(backoff)
                backoff *= 2
                attempt += 1
                continue
            # Non-transient error or retries exhausted: bubble up to the UI
            raise
