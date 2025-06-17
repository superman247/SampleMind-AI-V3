# cli/options/clean_metadata.py

"""
SampleMindAI – Clean Metadata
Clean or repair metadata for audio files (e.g., remove invalid tags, fix metadata).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

def clean_metadata(file_path: str) -> None:
    """
    Placeholder function for cleaning or repairing metadata in an audio file.
    """
    try:
        json_path = os.path.splitext(file_path)[0] + ".json"
        if not os.path.exists(json_path):
            console.print(f"[yellow]No metadata file found for {file_path}[/yellow]")
            return

        with open(json_path, "r") as f:
            metadata = json.load(f)
        
        # Placeholder: cleaning logic goes here (e.g., remove empty fields or invalid values)
        cleaned_metadata = {k: v for k, v in metadata.items() if v not in [None, ""]}

        with open(json_path, "w") as f:
            json.dump(cleaned_metadata, f, indent=2)

        console.print(f"[green]Cleaned metadata for {file_path}[/green]")
        log_event(f"Cleaned metadata for {file_path}")
    
    except Exception as e:
        console.print(f"[red]Failed to clean metadata for {file_path}: {e}[/red]")
        log_event(f"Metadata clean failed for {file_path}: {e}")

def main() -> None:
    """
    CLI entrypoint for cleaning metadata in audio files.
    """
    console.print("[bold magenta]SampleMindAI – Clean Metadata[/bold magenta]")

    folder = Prompt.ask("Folder to clean metadata", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
        return

    files = [f for f in os.listdir(folder) if f.endswith(".wav")]
    if not files:
        console.print(f"[yellow]No audio files found in {folder}[/yellow]")
        return

    for file in files:
        file_path = os.path.join(folder, file)
        clean_metadata(file_path)

    console.print("[green]Metadata cleaning complete![/green]")
    log_event(f"Metadata cleaning complete for folder: {folder}")

if __name__ == "__main__":
    main()
