from utils.config import config
# ai_engine/gpt/tag_normalizer.py

from core.ai_backend import query_ai
import os
import json
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def normalize_tags(file_path, backend="hermes"):
    json_path = file_path + ".json"
    if not os.path.exists(json_path):
        console.print(f"[yellow]No tag file found for {file_path}. Skipping.[/yellow]")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        tags = f.read()

    prompt = (
        f"Normalize the following tags for this audio file: {file_path}.\n"
        f"Current tags: {tags}\n"
        "Ensure all tag fields (genre, mood, instrument, bpm) are present, consistent, and use standardized terms. "
        "Respond with the normalized tag set in JSON."
    )
    result = query_ai(prompt, backend=backend)
    try:
        tags = json.loads(result)
    except Exception:
        tags = {"raw": result}
    normalized_path = file_path + ".normalized.json"
    with open(normalized_path, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)
    console.print(f"[green]Normalized tags written to: {normalized_path}[/green]")

def main():
    file_path = Prompt.ask("Enter path to audio file (tags in .json file expected)")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    normalize_tags(file_path, backend=backend)

if __name__ == "__main__":
    main()