from utils.config import config
# utils/openai_utils.py

import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"  # This is GPT-4.1 (latest as of 2024/2025)

def query_openai(prompt: str, stream: bool = False, **kwargs) -> str:
    # ...your existing logic...
    """
    Query OpenAI's GPT-4.1 model for completions.
    """
    if not OPENAI_API_KEY:
        return "OpenAI API key not set."
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": stream,
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"OpenAI Error: {e}"