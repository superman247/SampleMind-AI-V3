from utils.config import config
# Empty module: smart_tag_rater
# ai_engine/gpt/smart_tag_rater.py

from core.ai_backend import query_ai
import os
import json
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def rate_tags(file_path, backend="hermes"):
    json_path = file_path + ".json"
    if not os.path.exists(json_path):
        console.print(f"[red]No tag file found for {file_path}[/red]")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        tags = f.read()

    prompt = (
        f"Rate and evaluate the following tags for the audio file {file_path}:\n"
        f"Tags: {tags}\n"
        "Respond with an objective score (0-100) for accuracy and a short reason for the rating."
    )
    result = query_ai(prompt, backend=backend)
    console.print(f"[bold green]Tag Rating and Feedback:[/bold green] {result}")

def main():
    file_path = Prompt.ask("Enter path to audio file (tags in .json file expected)")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    rate_tags(file_path, backend=backend)

if __name__ == "__main__":
    main()