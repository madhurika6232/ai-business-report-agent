import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


DEFAULT_MODEL = "openai/gpt-oss-20b"


def get_groq_client() -> Groq:
    """Create and return the configured Groq client."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(
        api_key=api_key,
        timeout=30.0,
        max_retries=2,
    )