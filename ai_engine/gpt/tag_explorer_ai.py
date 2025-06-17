from utils.config import config
# ai_engine/gpt/tag_explorer_ai.py

from core.ai_backend import query_ai
from rich.console import Console
from rich.prompt import Prompt
import os
import json

console = Console()

def explore_tags(folder_path, backend="hermes"):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".json")]
    if not files:
        console.print("[red]No tag JSON files found in the specified folder.[/red]")
        return

    for file in files:
        json_path = os.path.join(folder_path, file)
        with open(json_path, "r", encoding="utf-8") as f:
            tags = f.read()
        prompt = (
            f"Explore and summarize the tags for the audio file represented by {file}:\n"
            f"{tags}\n"
            "Provide a creative description of this file based on its tags. List possible genres, moods, and interesting features. Respond in plain English."
        )
        result = query_ai(prompt, backend=backend)
        console.print(f"[green]{file}:[/green] {result}\n")

def main():
    folder_path = Prompt.ask("Enter path to folder with tag JSON files")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    explore_tags(folder_path, backend=backend)

if __name__ == "__main__":
    main()