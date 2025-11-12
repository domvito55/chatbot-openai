# Customer Support Chatbot — OpenAI + Streamlit

A minimal, portfolio‑ready chatbot that demonstrates how to build a customer‑support assistant with **Streamlit** and the **OpenAI** API. It keeps chat history in `st.session_state`, cleanly separates UI from service code, and is ready for deployment to Streamlit Cloud.

## 📑 Table of Contents

-   [🎯 Project Overview](#-project-overview)
-   [🧩 Versions & Tech Stack](#-versions--tech-stack)
-   [🚀 Installation & Quick Start](#-installation--quick-start)
-   [🔐 Configuration](#-configuration)
-   [▶️ Run Locally](#️-run-locally)
-   [📁 Project Structure](#-project-structure)
-   [🏗️ Architecture](#-architecture)
-   [⚠️ Known Limitations](#️-known-limitations)
-   [🛠️ Customization](#️-customization)
-   [✅ Quality & Tooling](#-quality--tooling)
-   [🚧 Future Enhancements](#-future-enhancements)
-   [🗓️ Changelog](#️-changelog)

## 🎯 Project Overview

**Objective:** Provide a clean, production‑minded template for an AI customer‑support chatbot powered by Streamlit + OpenAI.

**What this template shows**

-   Minimal chat loop with persistent **session state**
-   Separation of concerns (**UI** vs **service integration**)
-   Local secrets via **.env** and Cloud secrets via **Streamlit Secrets**
-   Ready to deploy on **Streamlit Cloud**

**Typical use cases**

-   FAQ assistant and L1 support triage
-   Lead capture and intent classification
-   Internal knowledge base Q&A (RAG add‑on later)

## 🧩 Versions & Tech Stack

> These reflect the versions in `environment.yml` / runtime today.

-   **Python:** 3.12
-   **Streamlit:** 1.51
-   **OpenAI Python SDK:** 2.7.2
-   **python‑dotenv:** 1.1.1
-   **(Dev)** Ruff, Black, Pytest, Pre‑commit

## 🚀 Installation & Quick Start

### Using Conda (recommended)

    conda env create -f environment.yml
    conda activate chatbot-openai

    # optional but recommended for consistent quality checks
    pre-commit install

### Using pip (alternative)

    python -m venv .venv
    # Windows PowerShell
    .\.venv\Scripts\Activate.ps1
    # macOS/Linux
    source .venv/bin/activate

    pip install -r requirements.txt

## 🔐 Configuration

The app reads secrets **first** from Streamlit Secrets and **then** falls back to environment variables (including values loaded from a local `.env`).

**Local (dotenv):** create a `.env` in the project root:

    OPENAI_API_KEY=sk-xxxx

**OR Streamlit local secrets:** create `.streamlit/secrets.toml`:

    OPENAI_API_KEY = "sk-xxxx"

**Streamlit Cloud (deploy):** App → _Settings_ → _Secrets_

    OPENAI_API_KEY = "sk-xxxx"

> Do **not** commit `.env` or `.streamlit/secrets.toml`.

### Advanced configuration (env or Streamlit Secrets)

-   `OPENAI_DEFAULT_MODEL` (default: `gpt-4o-mini`)
-   `OPENAI_TEMPERATURE` (default: `0.2`)
-   `OPENAI_TIMEOUT_SECONDS` (default: `30`)
-   `OPENAI_MAX_RETRIES` (default: `2`)
-   `CHAT_MAX_HISTORY` (default: `12`)

## ▶️ Run Locally

    streamlit run app.py

Open the URL shown in the terminal. You should see a chat UI; messages persist within the browser session.

## 📁 Project Structure

    .
    ├── app.py                      # Streamlit UI and conversation loop
    ├── environment.yml             # Conda environment (dev + runtime)
    ├── requirements.txt            # Runtime deps for Streamlit Cloud
    ├── pyproject.toml              # Black/Ruff/Pytest configuration
    ├── .pre-commit-config.yaml     # Lint/format hooks
    ├── .streamlit/
    │   └── config.toml             # UI/theme (no secrets here)
    ├── src/
    │   ├── config/
    │   │   └── settings.py         # Secrets: st.secrets → env (.env)
    │   ├── services/
    │   │   └── openai_client.py    # OpenAI integration (send_chat)
    │   ├── ui/
    │   │   └── components.py       # (optional) shared UI components
    │   └── utils/
    │       └── formatting.py       # (optional) text/clean helpers
    └── tests/
        ├── test_openai_client.py   # Service unit tests (mock OpenAI)
        └── test_formatting.py      # Utils tests

## 🏗️ Architecture

    Browser (Streamlit UI)
      └── app.py
          ├─ renders chat history from st.session_state["messages"]
          ├─ collects user input (st.chat_input)
          └─ calls send_chat(messages, system_prompt)
                │
                ▼
          src/services/openai_client.py
            ├─ reads key via src/config/settings.get_openai_api_key()
            ├─ builds request for OpenAI chat completions API
            └─ returns assistant text back to UI

**Design principles**

-   Keep UI state in `st.session_state`
-   Isolate vendor API calls in `services/`
-   One source of truth for secrets/config in `config/`

## ⚠️ Known Limitations

-   No token streaming UI (single message response).
-   Session state is in-memory per browser tab (refresh clears history).
-   Costs depend on model usage; monitor with cheaper models in dev.

## 🛠️ Customization

-   **System prompt (sidebar):** edit the high‑level behavior prompt (next step).
-   **Clear chat button:** reset current conversation (next step).
-   **Styling:** via Streamlit theme (`.streamlit/config.toml`) — no custom CSS.

## ✅ Quality & Tooling

-   **Pre‑commit** hooks: end‑of‑file, trailing whitespace, YAML check, Ruff (lint, `--fix`), Black (format)
-   **Ruff / Black** configured via `pyproject.toml`
-   **Pytest** with a starter test suite (`tests/`)

## 🚧 Future Enhancements

-   [ ] Token streaming in the UI
-   [ ] Long-chat management: history **summarization** (beyond the current clamp)
-   [ ] Full unit test suite with OpenAI client mocks; coverage report/badge
-   [ ] CI (GitHub Actions) running Ruff/Black/Pytest + pre-commit on PRs
-   [ ] One-click deployment recipe to Streamlit Cloud + status badges
-   [ ] Model switcher (cheap vs. quality) and per-session parameters
-   [ ] Basic telemetry (session/message counts, optional CSAT) with opt-out
-   [ ] Optional RAG module (vector store + retrieval; local file ingest)

> Delivered in **Step E**: transient-error retries with backoff and context clamp.

## 🗓️ Changelog

-   **v0.2** — Step E: retries with backoff, friendly error messages, history clamp; README aligned.
