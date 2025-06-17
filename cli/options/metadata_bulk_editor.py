# cli/options/metadata_bulk_editor.py

"""
SampleMindAI – Metadata Bulk Editor
Bulk edit metadata for multiple audio files (e.g., genre, mood, instrument).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

def bulk_edit_metadata(folder: str, tag: str, value: str) -> None:
    """
    Placeholder function for bulk editing metadata in audio files.
    In the future, this will allow for batch editing of metadata fields (e.g., genre, mood).
    """
    files = [f for f in os.listdir(folder) if f.endswith(tuple(config.SUPPORTED_EXTENSIONS))]
    if not files:
        console.print(f"[yellow]No audio files found in {folder}[/yellow]")
        return

    for file in files:
        file_path = os.path.join(folder, file)
        json_path = os.path.splitext(file_path)[0] + ".json"
        
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                metadata = json.load(f)
            
            metadata[tag] = value  # Edit the metadata
            with open(json_path, "w") as f:
                json.dump(metadata, f, indent=2)

            console.print(f"[cyan]Updated {file_path} with {tag}: {value}[/cyan]")
            log_event(f"Updated {file_path} with {tag}: {value}")
        else:
            console.print(f"[yellow]No metadata found for {file_path}[/yellow]")

def main() -> None:
    """
    CLI entrypoint for bulk editing metadata in audio files.
    """
    console.print("[bold magenta]SampleMindAI – Metadata Bulk Editor[/bold magenta]")

    folder = Prompt.ask("Enter the folder to bulk edit metadata", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
        return

    tag = Prompt.ask("Enter the metadata tag to edit (e.g., genre, mood, instrument)", default="genre")
    value = Prompt.ask("Enter the new value for the tag")

    bulk_edit_metadata(folder, tag, value)

    console.print(f"[green]Metadata bulk edit complete![/green]")
    log_event(f"Metadata bulk edit complete for folder: {folder} with {tag}: {value}")

if __name__ == "__main__":
    main()
