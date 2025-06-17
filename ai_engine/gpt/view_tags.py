from utils.config import config
# ai_engine/gpt/view_tags.py

import os
import json
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def view_tags(file_path):
    json_path = file_path + ".json"
    if not os.path.exists(json_path):
        console.print(f"[yellow]No tag file found for {file_path}.[/yellow]")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        tags = json.load(f)
    console.print(f"[bold green]Tags for {file_path}:[/bold green] {tags}")

def main():
    file_path = Prompt.ask("Enter path to audio file (tags in .json file expected)")
    view_tags(file_path)

if __name__ == "__main__":
    main()