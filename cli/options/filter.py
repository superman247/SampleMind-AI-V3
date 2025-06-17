# cli/options/filter.py

"""
SampleMindAI – Filter
Filter audio files by metadata tags (e.g., genre, mood, instrument).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

def filter_audio_files(folder: str, tag: str, value: str) -> None:
    """
    Placeholder function for filtering audio files by metadata tags.
    In the future, this would filter based on real metadata (genre, mood, instrument).
    """
    filtered_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(tuple(config.SUPPORTED_EXTENSIONS)):
                json_path = os.path.splitext(file_path)[0] + ".json"
                if os.path.exists(json_path):
                    with open(json_path, "r") as f:
                        metadata = json.load(f)
                        if metadata.get(tag) == value:
                            filtered_files.append(file_path)
                            console.print(f"[cyan]Filtered: {file_path}[/cyan]")
                            log_event(f"Filtered file: {file_path} based on {tag}: {value}")
    
    if filtered_files:
        console.print(f"[green]Found {len(filtered_files)} file(s) matching the filter:[/green]")
        for file in filtered_files:
            console.print(f"[cyan]{file}[/cyan]")
    else:
        console.print(f"[yellow]No files found matching {tag}: {value}[/yellow]")

def main() -> None:
    """
    CLI entrypoint for filtering audio files based on metadata.
    """
    console.print("[bold magenta]SampleMindAI – Filter[/bold magenta]")

    folder = Prompt.ask("Enter the folder to filter", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
        return

    tag = Prompt.ask("Enter the metadata tag to filter by (e.g., genre, mood, instrument)", default="genre")
    value = Prompt.ask("Enter the value to filter by (e.g., Techno, Happy, Piano)")

    filter_audio_files(folder, tag, value)

    console.print("[green]Filter operation complete![/green]")
    log_event(f"Filter operation complete for {folder} by {tag}: {value}")

if __name__ == "__main__":
    main()
