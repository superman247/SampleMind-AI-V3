from utils.config import config
# core/ai_backend.py

import os
import json
from typing import Dict, Any
from core.llm_client import query_hermes

# Try to import OpenAI utilities if available
try:
    from utils.openai_utils import query_openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    def query_openai(prompt: str, stream: bool = False, **kwargs: Any) -> str:
        return '{"error": "OpenAI not available."}'

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def query_ai(file_path: str, backend: str = "hermes") -> Dict[str, str]:
    """
    Query AI backend (Hermes or OpenAI) and return structured metadata.
    Fallback to other engine if primary fails.
    """
    # Use filename or placeholder prompt
    prompt = f"Analyze the audio file and return tags as JSON: genre, mood, instrument."

    # Main AI call
    result = ""

    if backend == "openai":
        if OPENAI_AVAILABLE and OPENAI_API_KEY:
            result = query_openai(prompt)
        else:
            result = query_hermes(prompt)
    else:
        result = query_hermes(prompt)
        if ("error" in result.lower() or result.strip() == "") and OPENAI_AVAILABLE and OPENAI_API_KEY:
            result = query_openai(prompt)

    # Convert result to dict
    try:
        parsed: Dict[str, str] = json.loads(result) if isinstance(result, str) else result
        return parsed
    except (json.JSONDecodeError, TypeError):
        return {
            "genre": "unknown",
            "mood": "unknown",
            "instrument": "unknown"
        }