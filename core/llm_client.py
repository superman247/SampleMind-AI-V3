from utils.config import config
# samplemind/core/llm_client.py

import requests
from rich.console import Console
from typing import Optional, Generator

console = Console()

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "hermes-samplemind"

def query_hermes(prompt: str, system: Optional[str] = None, stream: bool = False) -> str:
    """
    Send a prompt to the locally running Hermes model via Ollama.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": stream}
    if system:
        payload["system"] = system
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.Timeout:
        console.print("[bold red]⚠️ Timeout Error:[/bold red] The request timed out.")
        return "Timeout Error"
    except requests.exceptions.ConnectionError:
        console.print("[bold red]⚠️ Connection Error:[/bold red] Unable to connect to Hermes.")
        return "Connection Error"
    except Exception as e:
        console.print(f"[bold red]⚠️ Unexpected Error:[/bold red] {e}")
        return "Unexpected Error"

def query_hermes_stream(prompt: str, system: Optional[str] = None) -> Generator[str, None, None]:
    """
    Stream responses from the Hermes model.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": True}
    if system:
        payload["system"] = system
    try:
        with requests.post(OLLAMA_ENDPOINT, json=payload, headers=headers, stream=True, timeout=30) as response:
            response.raise_for_status()
            for i, line in enumerate(response.iter_lines()):
                if i > 100:
                    break
                if line:
                    yield line.decode("utf-8")
    except Exception as e:
        console.print(f"[bold red]⚠️ Streaming Error:[/bold red] {e}")
        yield "Streaming Error"

def query_ai(prompt: str, backend: str = 'hermes', **kwargs) -> str:
    """
    Universal AI prompt for SampleMind.
    Choose backend: 'hermes' (local), 'openai' (cloud), more in future.
    """
    if backend == "hermes":
        return query_hermes(prompt, **kwargs)
    elif backend == "openai":
        try:
            from utils.openai_utils import query_openai
            return query_openai(prompt, **kwargs)
        except ImportError:
            return "OpenAI is not available."
    else:
        return "Unknown AI backend selected."

# --- Direct test
if __name__ == "__main__":
    console.print("[bold cyan]🔍 Testing local Hermes model...[/bold cyan]")
    test_prompt = "Give a short description of what SampleMind does."
    reply = query_hermes(test_prompt)
    console.print(f"\n[green]Answer:[/green] {reply}")

# --- Tests (can be moved to a dedicated test file)
import pytest
from unittest.mock import patch

@patch("requests.post")
def test_query_hermes_with_mock(mock_post):
    mock_post.return_value.json.return_value = {"response": "SampleMind is a tool for AI navigation."}
    mock_post.return_value.status_code = 200
    prompt = "What is SampleMind?"
    response = query_hermes(prompt)
    assert response == "SampleMind is a tool for AI navigation."

def test_query_hermes_with_system():
    prompt = "What is SampleMind?"
    system = "You are a helpful assistant."
    response = query_hermes(prompt, system)
    assert isinstance(response, str)
    assert len(response) > 0

def test_query_hermes_without_mock():
    prompt = "What is SampleMind?"
    response = query_hermes(prompt)
    assert isinstance(response, str)
    assert len(response) > 0