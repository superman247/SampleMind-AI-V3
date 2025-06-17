from utils.config import config
# ai_engine/gpt/validate_tags.py

from core.ai_backend import query_ai
import os
import json
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def validate_tags(file_path, backend="hermes"):
    json_path = file_path + ".json"
    if not os.path.exists(json_path):
        console.print(f"[yellow]No tag file found for {file_path}. Skipping.[/yellow]")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        tags = f.read()

    prompt = (
        f"Validate the following tags for this audio file: {file_path}.\n"
        f"Tags: {tags}\n"
        "Check for errors, missing fields, or inconsistencies. Respond with 'VALID' if everything is fine, or suggest corrections in JSON."
    )
    result = query_ai(prompt, backend=backend)
    console.print(f"[bold green]Validation result:[/bold green] {result}")

def main():
    file_path = Prompt.ask("Enter path to audio file (tags in .json file expected)")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    validate_tags(file_path, backend=backend)

if __name__ == "__main__":
    main()