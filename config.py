"""Configuration manager for ResolveIQ.

Reads environment variables from .env file or system environment.
Never hardcodes credentials or API keys.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Hindsight Cloud configuration
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "").strip()
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "resolveiq-support-bank").strip()
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io").strip()

# Optional LLM provider keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()


def mask_key(key: str) -> str:
    """Safely mask an API key for display in the UI."""
    if not key:
        return "Not Set"
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"


def get_environment_status() -> dict:
    """Returns a dictionary summarizing configuration status."""
    return {
        "hindsight_api_key_configured": bool(HINDSIGHT_API_KEY),
        "hindsight_api_key_masked": mask_key(HINDSIGHT_API_KEY),
        "hindsight_bank_id": HINDSIGHT_BANK_ID,
        "hindsight_base_url": HINDSIGHT_BASE_URL,
        "openai_configured": bool(OPENAI_API_KEY),
        "groq_configured": bool(GROQ_API_KEY),
        "anthropic_configured": bool(ANTHROPIC_API_KEY),
    }
