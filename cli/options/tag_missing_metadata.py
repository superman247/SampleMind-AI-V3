# cli/options/tag_missing_metadata.py

"""
SampleMindAI – Tag Missing Metadata
Tag missing metadata (e.g., genre, mood, instrument) for audio files.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

def tag_missing_metadata(file_path: str, genre: str = "Unknown", mood: str = "Unknown", instrument: str = "Unknown") -> None:
    """
    Placeholder function for tagging missing metadata in audio files.
    In the future, this could tag missing metadata based on AI or heuristics.
    """
    json_path = os.path.splitext(file_path)[0] + ".json"
    if not os.path.exists(json_path):
        console.print(f"[yellow]No metadata file found for {file_path}. Skipping tagging.[/yellow]")
        return
    
    # Load existing metadata (if any)
    with open(json_path, "r") as f:
        metadata = json.load(f)
    
    # Add missing metadata
    if not metadata.get("genre"):
        metadata["genre"] = genre
    if not metadata.get("mood"):
        metadata["mood"] = mood
    if not metadata.get("instrument"):
        metadata["instrument"] = instrument

    # Save the updated metadata back to the JSON file
    with open(json_path, "w") as f:
        json.dump(metadata, f, indent=2)

    console.print(f"[cyan]Tagged missing metadata for {file_path}[/cyan]")
    log_event(f"Tagged missing metadata for {file_path} with genre: {genre}, mood: {mood}, instrument: {instrument}")

def main() -> None:
    """
    CLI entrypoint for tagging missing metadata in audio files.
    """
    console.print("[bold magenta]SampleMindAI – Tag Missing Metadata[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio file to tag")
    if not file_path or not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/]")
        return

    genre = Prompt.ask("Enter the genre to tag", default="Unknown")
    mood = Prompt.ask("Enter the mood to tag", default="Unknown")
    instrument = Prompt.ask("Enter the instrument to tag", default="Unknown")

    tag_missing_metadata(file_path, genre, mood, instrument)

    console.print(f"[green]Missing metadata tagged for {file_path}[/green]")
    log_event(f"Missing metadata tagged for {file_path} with genre: {genre}, mood: {mood}, instrument: {instrument}")

if __name__ == "__main__":
    main()
