from utils.config import config
# ai_engine/gpt/tag_analyzer.py

from core.ai_backend import query_ai
from rich.console import Console
from rich.prompt import Prompt
import os
import json

console = Console()

def analyze_tags(file_path, backend="hermes"):
    json_path = file_path + ".json"
    if not os.path.exists(json_path):
        console.print(f"[yellow]No tag file found for {file_path}. Skipping.[/yellow]")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        tags = f.read()

    prompt = (
        f"Analyze and critique the tags for this audio file: {file_path}.\n"
        f"Tags: {tags}\n"
        "Identify any weaknesses, mistakes, or missing info. Suggest improvements. Respond in plain English."
    )
    result = query_ai(prompt, backend=backend)
    console.print(f"[bold green]Tag Analysis:[/bold green] {result}")

def main():
    file_path = Prompt.ask("Enter path to audio file (tags in .json file expected)")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    analyze_tags(file_path, backend=backend)

if __name__ == "__main__":
    main()