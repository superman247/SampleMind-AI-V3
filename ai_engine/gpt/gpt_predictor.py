from utils.config import config
# ai_engine/gpt/gpt_predictor.py

from core.ai_backend import query_ai
import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def main():
    console.print("[bold cyan]AI Predictor – Predict metadata for a single audio file.[/bold cyan]")
    file_path = Prompt.ask("Enter path to audio file")
    backend = Prompt.ask("Choose AI backend ('hermes' for local, 'openai' for cloud)", choices=["hermes", "openai"], default="hermes")

    prompt = (
        f"Predict and return the genre, mood, instrument, bpm, and a short summary for the audio file: {file_path}. "
        "Respond in JSON format: {\"genre\": ..., \"mood\": ..., \"instrument\": ..., \"bpm\": ..., \"summary\": ...}"
    )
    result = query_ai(prompt, backend=backend)
    console.print(f"\n[bold green]AI Prediction:[/bold green] {result}")

if __name__ == "__main__":
    main()