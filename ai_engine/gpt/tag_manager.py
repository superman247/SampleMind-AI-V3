from utils.config import config
# ai_engine/gpt/tag_manager.py

from core.ai_backend import query_ai
import os
import json
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def list_tags(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".json")]
    for file in files:
        json_path = os.path.join(folder_path, file)
        with open(json_path, "r", encoding="utf-8") as f:
            tags = json.load(f)
        console.print(f"[bold cyan]{file}:[/bold cyan] {tags}")

def update_tags(file_path, backend="hermes"):
    json_path = file_path + ".json"
    if not os.path.exists(json_path):
        console.print(f"[yellow]No tag file found for {file_path}. Creating new tags.[/yellow]")
        current_tags = ""
    else:
        with open(json_path, "r", encoding="utf-8") as f:
            current_tags = f.read()

    prompt = (
        f"Update or improve the following tags for the audio file {file_path}:\n"
        f"Current tags: {current_tags}\n"
        "Respond with a complete JSON tag set."
    )
    result = query_ai(prompt, backend=backend)
    try:
        tags = json.loads(result)
    except Exception:
        tags = {"raw": result}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)
    console.print(f"[green]Tags updated for: {file_path}[/green]")

def main():
    console.print("[bold cyan]Tag Manager[/bold cyan]")
    action = Prompt.ask("Choose action: [list] tags or [update] tags", choices=["list", "update"], default="list")
    folder_path = Prompt.ask("Enter folder path (for 'list') or file path (for 'update')")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")

    if action == "list":
        list_tags(folder_path)
    else:
        update_tags(folder_path, backend=backend)

if __name__ == "__main__":
    main()