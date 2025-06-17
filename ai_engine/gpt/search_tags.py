from utils.config import config
# ai_engine/gpt/search_tags.py

from core.ai_backend import query_ai
from rich.console import Console
from rich.prompt import Prompt
import os
import json

console = Console()

def search_tags(folder_path, search_term, backend="hermes"):
    console.print(f"[bold cyan]Searching for '{search_term}' in tags using AI...[/bold cyan]")
    for file in os.listdir(folder_path):
        if file.lower().endswith(".json"):
            json_path = os.path.join(folder_path, file)
            with open(json_path, "r", encoding="utf-8") as f:
                tags = f.read()
            prompt = (
                f"Does the following tag set for an audio file match or relate to the term '{search_term}'?\n"
                f"Tags: {tags}\n"
                "Respond only YES or NO, and if YES, suggest why (short)."
            )
            result = query_ai(prompt, backend=backend)
            if "yes" in result.lower():
                console.print(f"[green]{file}[/green]: [bold]{result}[/bold]")

def main():
    folder_path = Prompt.ask("Enter path to folder with tag JSON files")
    search_term = Prompt.ask("Enter tag or keyword to search for")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    search_tags(folder_path, search_term, backend=backend)

if __name__ == "__main__":
    main()