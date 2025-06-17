from utils.config import config
# ai_engine/gpt/tag_confidence_visualizer.py

from core.ai_backend import query_ai
from rich.console import Console
from rich.prompt import Prompt
import os
import json

console = Console()

def visualize_tag_confidence(file_path, backend="hermes"):
    json_path = file_path + ".json"
    if not os.path.exists(json_path):
        console.print(f"[yellow]No tag file found for {file_path}. Skipping.[/yellow]")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        tags = f.read()

    prompt = (
        f"Given the following tags for the audio file {file_path}:\n"
        f"{tags}\n"
        "For each tag, estimate a confidence score from 0 (not confident) to 100 (very confident). "
        "Display the result as a JSON object with each tag and its score."
    )
    result = query_ai(prompt, backend=backend)
    try:
        confidence = json.loads(result)
    except Exception:
        confidence = {"raw": result}
    console.print(f"[bold green]Tag Confidence Scores:[/bold green] {confidence}")

def main():
    file_path = Prompt.ask("Enter path to audio file (tags in .json file expected)")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    visualize_tag_confidence(file_path, backend=backend)

if __name__ == "__main__":
    main()