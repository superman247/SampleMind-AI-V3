from utils.config import config
# ai_engine/gpt/tag_explorer_ui.py

from core.ai_backend import query_ai
from rich.console import Console
from rich.prompt import Prompt
import os
import json

console = Console()

def interactive_tag_explorer(folder_path, backend="hermes"):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".json")]
    if not files:
        console.print("[red]No tag JSON files found in the specified folder.[/red]")
        return

    while True:
        console.print("\n[bold cyan]Available files:[/bold cyan]")
        for idx, file in enumerate(files):
            console.print(f"{idx + 1}. {file}")
        choice = Prompt.ask("Select a file to explore (number), or type 'exit' to quit")
        if choice.lower() in ("exit", "quit"):
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                json_path = os.path.join(folder_path, files[idx])
                with open(json_path, "r", encoding="utf-8") as f:
                    tags = f.read()
                prompt = (
                    f"Based on the tags for this audio file ({files[idx]}):\n"
                    f"{tags}\n"
                    "Provide an engaging summary, suggest possible uses for this sample, and recommend additional tags if relevant."
                )
                result = query_ai(prompt, backend=backend)
                console.print(f"[bold green]AI Summary and Suggestions:[/bold green] {result}\n")
            else:
                console.print("[red]Invalid selection.[/red]")
        except Exception:
            console.print("[red]Invalid input.[/red]")

def main():
    folder_path = Prompt.ask("Enter path to folder with tag JSON files")
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    interactive_tag_explorer(folder_path, backend=backend)

if __name__ == "__main__":
    main()