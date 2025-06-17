# cli/options/validate_metadata.py

"""
SampleMindAI – Validate Metadata
Validate metadata for audio files (e.g., ensure all required fields like genre, mood, and instrument are filled).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

def validate_metadata(file_path: str) -> bool:
    """
    Placeholder function for validating metadata in an audio file.
    Checks that all required fields (e.g., genre, mood, instrument) are present and valid.
    """
    json_path = os.path.splitext(file_path)[0] + ".json"
    if not os.path.exists(json_path):
        console.print(f"[yellow]No metadata file found for {file_path}. Skipping validation.[/yellow]")
        return False
    
    with open(json_path, "r") as f:
        metadata = json.load(f)
    
    # Check for required fields (genre, mood, instrument)
    if not all(metadata.get(field) for field in ["genre", "mood", "instrument"]):
        console.print(f"[red]Missing required metadata in {file_path}[/red]")
        log_event(f"Missing required metadata in {file_path}")
        return False

    console.print(f"[green]Metadata validated successfully for {file_path}[/green]")
    log_event(f"Metadata validated successfully for {file_path}")
    return True

def main() -> None:
    """
    CLI entrypoint for validating metadata in audio files.
    """
    console.print("[bold magenta]SampleMindAI – Validate Metadata[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio file to validate")
    if not file_path or not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/]")
        return

    is_valid = validate_metadata(file_path)

    if is_valid:
        console.print(f"[green]File metadata is valid![/green]")
    else:
        console.print(f"[red]File metadata is invalid. Please review.[/red]")

    log_event(f"Metadata validation complete for {file_path}")

if __name__ == "__main__":
    main()
